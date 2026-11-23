#Requires -Version 5.1
<#
.SYNOPSIS
    Register the Craft Anything MCP server with one or more agents.

.DESCRIPTION
    Idempotent: existing entries are left alone unless -Force is passed.
    Always writes a timestamped backup before editing a config file.

    OpenCode  -> ~/.config/opencode/opencode.json
    Hermes    -> `hermes mcp add` (its own config)
    Others    -> prints the exact command; does not guess paths.

.PARAMETER Agent
    all (default), opencode, hermes, or a comma-separated list.

.PARAMETER Cli
    Full path to craft-anything-cli.exe. Auto-detected when omitted.

.PARAMETER Force
    Replace an existing craft-anything entry instead of leaving it.

.PARAMETER DryRun
    Show what would change, touch nothing.

.EXAMPLE
    .\tools\wire-craft-anything.ps1 -DryRun
    .\tools\wire-craft-anything.ps1 -Agent opencode,hermes
#>
[CmdletBinding()]
param(
    [string]$Agent = 'all',
    [string]$Cli,
    [switch]$Force,
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'

function Say([string]$Text, [string]$Color = 'Gray') { Write-Host $Text -ForegroundColor $Color }

if (-not $Cli) {
    $candidates = @(
        'C:\Program Files\Craft Anything\craft-anything-cli.exe',
        (Join-Path $env:LOCALAPPDATA 'Programs\Craft Anything\craft-anything-cli.exe'),
        (Join-Path $env:ProgramFiles 'Craft Anything\craft-anything-cli.exe')
    )
    $Cli = $candidates | Where-Object { Test-Path $_ } | Select-Object -First 1
}

if (-not $Cli -or -not (Test-Path $Cli)) {
    Say 'FAIL: craft-anything-cli.exe not found. Pass -Cli "<full path>".' 'Red'
    exit 1
}

$targets = if ($Agent -eq 'all') { @('opencode', 'hermes') } else { $Agent -split ',' | ForEach-Object { $_.Trim() } }

Say "Craft Anything CLI: $Cli" 'Cyan'
if ($DryRun) { Say 'DRY RUN - no files will be written' 'Yellow' }

# --------------------------------------------------------------------------
# OpenCode
# --------------------------------------------------------------------------
if ($targets -contains 'opencode') {
    $path = Join-Path $env:USERPROFILE '.config\opencode\opencode.json'
    Say ''
    Say 'OpenCode' 'Cyan'

    if (-not (Test-Path $path)) {
        Say "  SKIP: no config at $path" 'Yellow'
    } else {
        try {
            $raw = Get-Content $path -Raw
            $cfg = $raw | ConvertFrom-Json

            $hasMcp = $null -ne $cfg.PSObject.Properties['mcp']
            $existing = if ($hasMcp) { $cfg.mcp.PSObject.Properties['craft-anything'] } else { $null }

            if ($existing -and -not $Force) {
                $cmd = ($existing.Value.command -join ' ')
                Say "  OK: already registered ($cmd)" 'Green'
            } else {
                $entry = [pscustomobject]@{
                    type    = 'local'
                    command = @($Cli, 'mcp')
                    enabled = $true
                }

                if ($DryRun) {
                    Say '  WOULD SET mcp.craft-anything = ' 'Yellow'
                    Say ("    " + ($entry | ConvertTo-Json -Compress)) 'DarkGray'
                } else {
                    $backup = "$path.bak-$((Get-Date).ToString('yyyyMMdd-HHmmss'))"
                    Copy-Item $path $backup
                    Say "  backup: $backup" 'DarkGray'

                    if (-not $hasMcp) {
                        $cfg | Add-Member -NotePropertyName mcp -NotePropertyValue ([pscustomobject]@{})
                    }

                    $cfg.mcp | Add-Member -NotePropertyName 'craft-anything' -NotePropertyValue $entry -Force
                    ($cfg | ConvertTo-Json -Depth 30) | Set-Content -Path $path -Encoding UTF8
                    Say '  WROTE: mcp.craft-anything (enabled)' 'Green'
                    Say '  Restart OpenCode so it reloads MCP servers.' 'Yellow'
                }
            }
        } catch {
            Say "  FAIL: $($_.Exception.Message)" 'Red'
        }
    }
}

# --------------------------------------------------------------------------
# Hermes
# --------------------------------------------------------------------------
if ($targets -contains 'hermes') {
    Say ''
    Say 'Hermes' 'Cyan'

    $hermes = Get-Command hermes -ErrorAction SilentlyContinue
    if (-not $hermes) {
        Say '  SKIP: hermes not on PATH' 'Yellow'
    } else {
        $list = (& hermes mcp list 2>&1 | Out-String)
        $present = $list -match 'craft-anything'

        if ($present -and -not $Force) {
            Say '  OK: already registered (hermes mcp list)' 'Green'
        } elseif ($DryRun) {
            Say '  WOULD RUN: hermes mcp add craft-anything --command "<cli>" --args mcp' 'Yellow'
        } else {
            if ($present -and $Force) {
                & hermes mcp remove craft-anything 2>&1 | Out-Null
                Say '  removed existing entry (-Force)' 'DarkGray'
            }
            $out = & hermes mcp add craft-anything --command $Cli --args mcp 2>&1
            $code = $LASTEXITCODE
            $out | Select-Object -Last 6 | ForEach-Object { Say "  $_" 'DarkGray' }
            if ($code -eq 0) {
                Say '  WROTE: craft-anything MCP server' 'Green'
            } else {
                Say "  FAIL: hermes mcp add exited $code" 'Red'
            }
        }
    }
}

# --------------------------------------------------------------------------
# Other agents: exact commands, no guessing
# --------------------------------------------------------------------------
Say ''
Say 'Other agents (copy the one you use)' 'Cyan'
$quoted = '"' + $Cli + '"'
Say "  Claude Code : claude mcp add craft-anything -- $quoted mcp" 'DarkGray'
Say "  Codex CLI   : codex mcp add craft-anything -- $quoted mcp" 'DarkGray'
Say '  Gemini CLI  : edit ~/.gemini/settings.json -> mcpServers.craft-anything = { "command": "<cli>", "args": ["mcp"] }' 'DarkGray'
Say '  Cursor/Windsurf/VS Code: add the same command/args to their MCP settings JSON.' 'DarkGray'
Say '  Any MCP client: command = the CLI path, args = ["mcp"], transport = stdio.' 'DarkGray'

Say ''
Say 'Verify everything with: .\tools\agent-preflight.ps1 -StartProvider' 'Cyan'
