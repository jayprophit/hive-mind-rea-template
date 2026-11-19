<#
.SYNOPSIS
    Move non-essential auto-start services to Manual so they run only on demand.

.DESCRIPTION
    On an 8 GB machine the boot cost is dominated by background services:
    14.9 GB was committed before any application was opened. This script moves
    them to Manual rather than Disabled, so nothing is uninstalled and Windows
    can still start them when something genuinely needs them.

    Services are grouped into tiers so you decide how far to go.

.TIER 1  (default)
    Always safe. No functional tradeoff.
      CCleaner, Grafana, Intel telemetry x4, Adobe updater, Bonjour,
      COMODO Dragon updater, Intel Driver Assistant x2, LetsView.

.TIER 2
    Safe, but you must start them yourself when needed.
      PostgreSQL 18 + pgbouncer + EDB PEM web server,
      Codex sandbox (the 15 ChatGPT processes).

.NEVER TOUCHED
    COMODO security, WSL, Office, anything under C:\Windows.

.PARAMETER Tier
    Which tier to apply. 1 (default) or 2. Tier 2 includes Tier 1.

.PARAMETER Apply
    Actually change the startup type. Without it the script only reports.

.PARAMETER StopNow
    Also stop the services that are running right now, so the memory is
    reclaimed immediately instead of after the next reboot. Stop-Service is
    a graceful service-control request, not a kill.

.PARAMETER IncludeRemoteAccess
    Also set TeamViewer and AnyDesk to Manual. Off by default because you may
    rely on them to reach this machine.

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File tools\trim-services.ps1
    powershell -ExecutionPolicy Bypass -File tools\trim-services.ps1 -Apply
    powershell -ExecutionPolicy Bypass -File tools\trim-services.ps1 -Tier 2 -Apply
#>

[CmdletBinding()]
param(
    [ValidateSet(1, 2)]
    [int]$Tier = 1,
    [switch]$Apply,
    [switch]$StopNow,
    [switch]$IncludeRemoteAccess
)

$ErrorActionPreference = 'Continue'

function Write-Section($t) {
    Write-Host ""
    Write-Host ("=" * 70) -ForegroundColor DarkCyan
    Write-Host "  $t" -ForegroundColor Cyan
    Write-Host ("=" * 70) -ForegroundColor DarkCyan
}
function Write-Ok($t)   { Write-Host "  [ok]   $t" -ForegroundColor Green }
function Write-Info($t) { Write-Host "  [info] $t" -ForegroundColor Gray }
function Write-Warn($t) { Write-Host "  [warn] $t" -ForegroundColor Yellow }

$isAdmin = ([Security.Principal.WindowsPrincipal] `
    [Security.Principal.WindowsIdentity]::GetCurrent()
).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin -and $Apply) {
    Write-Host ""
    Write-Warn "Changing service startup types requires Administrator."
    Write-Host "  Reporting only. Re-run from an elevated shell with -Apply." -ForegroundColor Yellow
    $Apply = $false
}

# --------------------------------------------------------------------------
# Tier 1 - always safe, no functional tradeoff
# --------------------------------------------------------------------------
$tier1 = @(
    @{ Name='CCleaner7';                        Why='duplicate cleaner; the repair script already covers this' }
    @{ Name='Grafana';                          Why='dashboards only; start it before a review session' }
    @{ Name='IntelTelemetryAgent';              Why='Intel telemetry, no user-facing function' }
    @{ Name='SystemUsageReportSvc_QUEENCREEK';  Why='Intel usage reporting' }
    @{ Name='IntelCollectorService';            Why='Intel data collection' }
    @{ Name='PresentMonSharedService';          Why='frame-time capture for benchmarks only' }
    @{ Name='AdobeARMservice';                  Why='Adobe Reader updater' }
    @{ Name='Bonjour Service';                  Why='Apple mDNS responder; only for iTunes/AirPlay' }
    @{ Name='DragonUpdater';                    Why='COMODO Dragon browser updater' }
    @{ Name='DSAService';                       Why='Intel Driver Assistant; run it manually when updating' }
    @{ Name='DSAUpdateService';                 Why='Intel Driver Assistant updater' }
    @{ Name='LetsViewService';                  Why='phone screen mirroring, unused' }
)

# --------------------------------------------------------------------------
# Tier 2 - safe, but you start them yourself
# --------------------------------------------------------------------------
$tier2 = @(
    @{ Name='postgresql-x64-18';                Why='DB engine; start it when a project needs a database' }
    @{ Name='pgbouncer';                        Why='connection pooler; useless without Postgres running' }
    @{ Name='PEMHTTPD-x64';                     Why='EDB Postgres Enterprise Manager web server' }
    @{ Name='CodexSandboxService.OpenAI.Codex'; Why='ChatGPT/Codex sandbox; spawns ~15 processes' }
)

$optionalRemote = @(
    @{ Name='TeamViewer'; Why='remote access; keep if you depend on it' }
    @{ Name='AnyDesk';    Why='remote access; keep if you depend on it' }
)

$targets = @()
$targets += $tier1
if ($Tier -ge 2) { $targets += $tier2 }
if ($IncludeRemoteAccess) { $targets += $optionalRemote }

# --------------------------------------------------------------------------
Write-Section ("Tier $Tier service review" + $(if ($Apply) { ' - APPLYING' } else { ' - report only' }))

$changed = 0
$absent  = 0
$stopped = 0

function Get-CommitGB {
    try { return ((Get-Counter '\Memory\Committed Bytes').CounterSamples[0].CookedValue / 1GB) }
    catch { return $null }
}

$commitBefore = if ($Apply -and $StopNow) { Get-CommitGB } else { $null }
if ($null -ne $commitBefore) {
    Write-Info ("commit before: {0:N1} GB" -f $commitBefore)
}

foreach ($t in $targets) {
    $svc = Get-Service -Name $t.Name -ErrorAction SilentlyContinue
    if (-not $svc) {
        $absent++
        Write-Info ("{0,-38} not installed" -f $t.Name)
        continue
    }

    $wmi = Get-CimInstance Win32_Service -Filter "Name='$($t.Name)'" -ErrorAction SilentlyContinue
    $current = if ($wmi) { $wmi.StartMode } else { '' }

    if ($current -eq 'Manual' -or $current -eq 'Disabled') {
        Write-Info ("{0,-38} already {1}" -f $t.Name, $current)
    }
    elseif (-not $Apply) {
        Write-Info ("{0,-38} {1} -> would become Manual" -f $t.Name, $current)
        Write-Host ("         {0}" -f $t.Why) -ForegroundColor DarkGray
    }
    else {
        try {
            Set-Service -Name $t.Name -StartupType Manual -ErrorAction Stop
            Write-Ok ("{0,-38} {1} -> Manual" -f $t.Name, $current)
            Write-Host ("         {0}" -f $t.Why) -ForegroundColor DarkGray
            $changed++
        } catch {
            Write-Warn ("{0,-38} failed: {1}" -f $t.Name, $_.Exception.Message.Split([char]10)[0])
            continue
        }
    }

    # Reclaim the memory now instead of waiting for a reboot.
    if ($Apply -and $StopNow) {
        $live = Get-Service -Name $t.Name -ErrorAction SilentlyContinue
        if ($live -and $live.Status -eq 'Running') {
            try {
                Stop-Service -Name $t.Name -Force -ErrorAction Stop
                (Get-Service -Name $t.Name).WaitForStatus('Stopped', '00:00:25')
                Write-Ok ("{0,-38} stopped now" -f $t.Name)
                $stopped++
            } catch {
                Write-Warn ("{0,-38} stop failed: {1}" -f $t.Name, $_.Exception.Message.Split([char]10)[0])
            }
        }
    }
}

# --------------------------------------------------------------------------
if ($Tier -lt 2) {
    Write-Section "Deferred to Tier 2 (not touched)"
    foreach ($t in $tier2) {
        $svc = Get-Service -Name $t.Name -ErrorAction SilentlyContinue
        $state = if ($svc) { $svc.StartType } else { 'not installed' }
        Write-Info ("{0,-38} left as {1}" -f $t.Name, $state)
    }
    Write-Host ""
    Write-Host "  Run again with -Tier 2 -Apply to include these." -ForegroundColor DarkGray
}

# --------------------------------------------------------------------------
Write-Section "Never touched"
foreach ($n in @('CmdAgent','CmdAgentProt','isesrv','WSLService','ClickToRunSvc')) {
    $s = Get-Service -Name $n -ErrorAction SilentlyContinue
    if ($s) { Write-Info ("{0,-38} left as {1}" -f $n, $s.StartType) }
}

# --------------------------------------------------------------------------
Write-Section "WSL memory cap"
Write-Info "WSL defaults to half of installed RAM (~3.8 GB here) and does not release it."
if ($Apply) {
    $cfg = Join-Path $env:USERPROFILE '.wslconfig'
    if (Test-Path $cfg) {
        Write-Info "$cfg already exists; left alone"
    } else {
        @"
# Added by trim-services.ps1
# Cap the WSL VM so it cannot claim half of an 8 GB laptop.
[wsl2]
memory=2GB
processors=2
swap=1GB
"@ | Set-Content -Path $cfg -Encoding ASCII
        Write-Ok "wrote $cfg (memory=2GB, processors=2, swap=1GB)"
        Write-Info "Takes effect after: wsl --shutdown"
    }
} else {
    Write-Info "would write %USERPROFILE%\.wslconfig (memory=2GB)"
}

# --------------------------------------------------------------------------
Write-Section "Summary"
if ($Apply) {
    Write-Ok "$changed service(s) moved to Manual"
    if ($StopNow) { Write-Ok "$stopped service(s) stopped now" }
    Write-Info "Start one again:   Start-Service <name>"
    Write-Info "Revert one:        Set-Service <name> -StartupType Automatic"
} else {
    Write-Info "Nothing changed. Re-run with -Apply from an elevated shell."
}
if ($absent -gt 0) { Write-Info "$absent entr(ies) were not installed." }

if ($null -ne $commitBefore) {
    $commitAfter = Get-CommitGB
    if ($null -ne $commitAfter) {
        Write-Host ""
        Write-Host ("  Commit charge: {0:N1} GB -> {1:N1} GB  (freed {2:N1} GB)" -f `
            $commitBefore, $commitAfter, ($commitBefore - $commitAfter)) -ForegroundColor Cyan
    }
}

Write-Host ""
Write-Host "  Reboot, then compare before/after:" -ForegroundColor Cyan
Write-Host "    (Get-Counter '\Memory\Committed Bytes').CounterSamples[0].CookedValue/1GB" -ForegroundColor White
Write-Host ""
