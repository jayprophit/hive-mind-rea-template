#Requires -Version 5.1
<#
.SYNOPSIS
    Preflight for Craft Anything + agent wiring (OpenCode, Hermes, others).

.DESCRIPTION
    Catches the failure that looks like "nothing happened for 15 minutes":
      1. the agent's model provider is down (Ollama stopped, wrong URL)
      2. the model returns empty content (wrong chat template / reasoning-only)
      3. the craft-anything MCP server is not reachable or not registered
      4. the agent config points at a missing CLI

    Every check prints PASS / WARN / FAIL and what to do about it.
    Exit code 0 = safe to run the agent, 1 = at least one FAIL.

.PARAMETER StartProvider
    If the configured provider is a local Ollama URL and it is down, start it
    and wait for the API. This is the Tier 2 "start on demand" action.

.PARAMETER Quick
    Skip the model smoke test (checks wiring only).

.PARAMETER Json
    Emit a machine-readable result object.

.EXAMPLE
    .\tools\agent-preflight.ps1 -StartProvider
    .\tools\agent-preflight.ps1 -Quick
#>
[CmdletBinding()]
param(
    [switch]$StartProvider,
    [switch]$Quick,
    [switch]$Json
)

$ErrorActionPreference = 'Continue'
$results = New-Object System.Collections.Generic.List[object]

function Add-Result {
    param([string]$Name, [string]$Status, [string]$Detail, [string]$Fix = '')
    $results.Add([pscustomobject]@{ Check = $Name; Status = $Status; Detail = $Detail; Fix = $Fix })
}

function Get-Prop {
    param($Object, [string]$Name)
    if ($null -eq $Object) { return $null }
    $p = $Object.PSObject.Properties[$Name]
    if ($p) { return $p.Value }
    return $null
}

# --------------------------------------------------------------------------
# 1. Craft Anything CLI
# --------------------------------------------------------------------------
$cliCandidates = @(
    'C:\Program Files\Craft Anything\craft-anything-cli.exe',
    (Join-Path $env:LOCALAPPDATA 'Programs\Craft Anything\craft-anything-cli.exe'),
    (Join-Path $env:ProgramFiles 'Craft Anything\craft-anything-cli.exe')
)
$cli = $cliCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1

if ($cli) {
    $version = (& $cli --version 2>&1 | Select-Object -First 1) -join ''
    Add-Result 'craft-anything CLI' 'PASS' "$version ($cli)"
} else {
    Add-Result 'craft-anything CLI' 'FAIL' 'craft-anything-cli.exe not found' 'Install Craft Anything, or pass the real path when wiring.'
}

# --------------------------------------------------------------------------
# 2. MCP handshake and tool count
# --------------------------------------------------------------------------
function Invoke-McpProbe {
    param([string]$Exe, [int]$TimeoutMs = 45000)

    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = $Exe
    $psi.Arguments = 'mcp'
    $psi.RedirectStandardInput = $true
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $psi.UseShellExecute = $false
    $psi.CreateNoWindow = $true

    try {
        $p = [System.Diagnostics.Process]::Start($psi)
    } catch {
        return [pscustomobject]@{ Ok = $false; Tools = 0; Reason = $_.Exception.Message }
    }

    $init    = '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"preflight","version":"1.0"}}}'
    $ready   = '{"jsonrpc":"2.0","method":"notifications/initialized"}'
    $list    = '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}'

    try {
        $p.StandardInput.WriteLine($init)
        $p.StandardInput.WriteLine($ready)
        $p.StandardInput.WriteLine($list)
        $p.StandardInput.Close()
    } catch { }

    $stdout = $p.StandardOutput.ReadToEnd()
    $stderr = $p.StandardError.ReadToEnd()

    if (-not $p.WaitForExit($TimeoutMs)) {
        try { $p.Kill() } catch { }
        return [pscustomobject]@{ Ok = $false; Tools = 0; Reason = "no exit within $([math]::Round($TimeoutMs/1000))s" }
    }

    $toolCount = 0
    $sawInit = $false
    foreach ($line in ($stdout -split "`r?`n")) {
        $line = $line.Trim()
        if (-not $line.StartsWith('{')) { continue }
        try { $msg = $line | ConvertFrom-Json } catch { continue }
        if ((Get-Prop $msg 'id') -eq 1 -and (Get-Prop $msg 'result')) { $sawInit = $true }
        if ((Get-Prop $msg 'id') -eq 2 -and (Get-Prop $msg 'result')) {
            $tools = Get-Prop $msg.result 'tools'
            if ($tools) { $toolCount = @($tools).Count }
        }
    }

    if (-not $sawInit) {
        $why = if ($stderr) { ($stderr -split "`r?`n" | Select-Object -First 1) } else { 'no initialize response' }
        return [pscustomobject]@{ Ok = $false; Tools = 0; Reason = $why }
    }
    if ($toolCount -eq 0) {
        return [pscustomobject]@{ Ok = $false; Tools = 0; Reason = 'initialize ok but tools/list returned nothing' }
    }
    return [pscustomobject]@{ Ok = $true; Tools = $toolCount; Reason = '' }
}

if ($cli) {
    $probe = Invoke-McpProbe -Exe $cli
    if ($probe.Ok) {
        Add-Result 'MCP server' 'PASS' "$($probe.Tools) tools discovered over stdio"
    } else {
        Add-Result 'MCP server' 'FAIL' "handshake failed: $($probe.Reason)" 'Run: & "C:\Program Files\Craft Anything\craft-anything-cli.exe" mcp --help'
    }
}

# --------------------------------------------------------------------------
# 3. OpenCode registration
# --------------------------------------------------------------------------
$ocPath = Join-Path $env:USERPROFILE '.config\opencode\opencode.json'
if (Test-Path $ocPath) {
    try {
        $oc = Get-Content $ocPath -Raw | ConvertFrom-Json
        $entry = Get-Prop (Get-Prop $oc 'mcp') 'craft-anything'
        if ($entry -and (Get-Prop $entry 'enabled') -ne $false) {
            $cmd = (Get-Prop $entry 'command') -join ' '
            Add-Result 'OpenCode wiring' 'PASS' "mcp.craft-anything enabled: $cmd"
        } else {
            Add-Result 'OpenCode wiring' 'FAIL' 'mcp.craft-anything missing or disabled' 'Run: .\tools\wire-craft-anything.ps1 -Agent opencode'
        }
    } catch {
        Add-Result 'OpenCode wiring' 'WARN' "could not parse $ocPath : $($_.Exception.Message)" 'Fix the JSON, then rerun.'
    }
} else {
    Add-Result 'OpenCode wiring' 'WARN' "no config at $ocPath" 'Only needed if OpenCode is installed.'
}

# --------------------------------------------------------------------------
# 4. Hermes registration (MCP + model)
# --------------------------------------------------------------------------
$hermes = Get-Command hermes -ErrorAction SilentlyContinue
if ($hermes) {
    $mcpList = (& hermes mcp list 2>&1 | Out-String)
    if ($mcpList -match 'craft-anything') {
        $enabled = if ($mcpList -match 'craft-anything.*enabled') { 'enabled' } else { 'listed' }
        Add-Result 'Hermes MCP' 'PASS' "craft-anything $enabled"
    } else {
        Add-Result 'Hermes MCP' 'FAIL' 'craft-anything not registered' 'Run: .\tools\wire-craft-anything.ps1 -Agent hermes'
    }
} else {
    Add-Result 'Hermes MCP' 'WARN' 'hermes not on PATH' 'Only needed if Hermes is installed.'
}

# --------------------------------------------------------------------------
# 5. Model provider + smoke test
# --------------------------------------------------------------------------
$modelName = $null
$baseUrl = $null
$cfgPath = Join-Path $env:LOCALAPPDATA 'hermes\config.yaml'

if (Test-Path $cfgPath) {
    $inModel = $false
    foreach ($line in (Get-Content $cfgPath)) {
        if ($line -match '^model:\s*$') { $inModel = $true; continue }
        if ($inModel -and $line -match '^\S') { $inModel = $false }
        if ($inModel -and $line -match '^\s+default:\s*(.+)$')   { $modelName = $Matches[1].Trim().Trim('"') }
        if ($inModel -and $line -match '^\s+base_url:\s*(.+)$')  { $baseUrl = $Matches[1].Trim().Trim('"') }
    }
}

if (-not $modelName) {
    Add-Result 'Model config' 'WARN' 'no Hermes model.default found' 'Set one: hermes config set model.default <model>'
} else {
    Add-Result 'Model config' 'PASS' "$modelName @ $baseUrl"
}

if ($baseUrl -and $baseUrl -match '127\.0\.0\.1|localhost') {
    $modelsUri = ($baseUrl.TrimEnd('/')) + '/models'
    $up = $false
    try {
        $null = Invoke-RestMethod -Uri $modelsUri -TimeoutSec 5
        $up = $true
    } catch { $up = $false }

    if (-not $up -and $StartProvider) {
        $ollamaApp = Join-Path $env:LOCALAPPDATA 'Programs\Ollama\ollama app.exe'
        if (Test-Path $ollamaApp) {
            Start-Process -FilePath $ollamaApp -WindowStyle Hidden | Out-Null
            for ($i = 0; $i -lt 30; $i++) {
                Start-Sleep -Seconds 2
                try { $null = Invoke-RestMethod -Uri $modelsUri -TimeoutSec 3; $up = $true; break } catch { }
            }
        }
    }

    if ($up) {
        Add-Result 'Provider' 'PASS' "reachable: $modelsUri"
    } else {
        Add-Result 'Provider' 'FAIL' "not reachable: $modelsUri" 'Start it (.\tools\agent-preflight.ps1 -StartProvider) or run: ollama serve'
    }

    if ($up -and -not $Quick -and $modelName) {
        $body = @{
            model    = $modelName
            messages = @(@{ role = 'user'; content = 'Reply with exactly: OK' })
            max_tokens = 256
            stream   = $false
        } | ConvertTo-Json -Depth 6

        $sw = [Diagnostics.Stopwatch]::StartNew()
        try {
            $r = Invoke-RestMethod -Uri ($baseUrl.TrimEnd('/') + '/chat/completions') -Method Post `
                 -Body $body -ContentType 'application/json' -TimeoutSec 180
            $sw.Stop()
            $content = (Get-Prop (Get-Prop (@($r.choices)[0]) 'message') 'content')
            $finish  = Get-Prop (@($r.choices)[0]) 'finish_reason'

            if ([string]::IsNullOrWhiteSpace($content)) {
                Add-Result 'Model smoke test' 'FAIL' "empty response after $([math]::Round($sw.Elapsed.TotalSeconds,1))s (finish=$finish). The model burns tokens on hidden reasoning or has no chat template." 'Switch model: hermes config set model.default lfm3:1.7b'
            } elseif ($sw.Elapsed.TotalSeconds -gt 60) {
                Add-Result 'Model smoke test' 'WARN' "replied '$($content.Trim())' but took $([math]::Round($sw.Elapsed.TotalSeconds,1))s. Long builds will be slow." 'Use a smaller/faster model for the builder.'
            } else {
                Add-Result 'Model smoke test' 'PASS' "replied '$($content.Trim())' in $([math]::Round($sw.Elapsed.TotalSeconds,1))s"
            }
        } catch {
            $sw.Stop()
            Add-Result 'Model smoke test' 'FAIL' "request failed: $($_.Exception.Message)" 'Check the model exists: ollama list'
        }
    }
} elseif ($baseUrl) {
    Add-Result 'Provider' 'WARN' "remote provider, not probed: $baseUrl" 'Check the endpoint and key manually.'
}

# --------------------------------------------------------------------------
# Report
# --------------------------------------------------------------------------
$fails = @($results | Where-Object { $_.Status -eq 'FAIL' })
$warns = @($results | Where-Object { $_.Status -eq 'WARN' })

if ($Json) {
    [pscustomobject]@{
        ok      = ($fails.Count -eq 0)
        results = $results
        fails   = $fails.Count
        warns   = $warns.Count
    } | ConvertTo-Json -Depth 5
} else {
    Write-Host ''
    Write-Host 'Craft Anything / agent preflight' -ForegroundColor Cyan
    Write-Host ('-' * 64)
    foreach ($r in $results) {
        $color = switch ($r.Status) { 'PASS' { 'Green' } 'WARN' { 'Yellow' } default { 'Red' } }
        Write-Host ("{0,-6} {1,-20} {2}" -f $r.Status, $r.Check, $r.Detail) -ForegroundColor $color
        if ($r.Fix) { Write-Host ("       -> {0}" -f $r.Fix) -ForegroundColor DarkGray }
    }
    Write-Host ('-' * 64)
    if ($fails.Count -eq 0) {
        Write-Host "READY ($($warns.Count) warning(s))" -ForegroundColor Green
    } else {
        Write-Host "NOT READY: $($fails.Count) failure(s)" -ForegroundColor Red
    }
}

if ($fails.Count -gt 0) { exit 1 } else { exit 0 }
