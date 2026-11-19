<#
.SYNOPSIS
    Move non-essential auto-start services to Manual so they only run on demand.

.DESCRIPTION
    On an 8 GB machine the boot cost is dominated by services nobody asked for:
    a full PostgreSQL stack, Intel telemetry, CCleaner, Grafana, an EDB web
    server and a browser updater. They hold several GB of commit before you
    open a single application.

    This script moves them to Manual rather than Disabled, so Windows starts
    them the moment something genuinely needs them. Manual is the safe,
    reversible choice.

    Services that are never touched:
      - COMODO security (CmdAgent, CmdAgentProt, isesrv)
      - WSLService
      - Office ClickToRun
      - anything under C:\Windows

.PARAMETER Apply
    Actually change the startup type. Without it, the script only reports.

.PARAMETER IncludeRemoteAccess
    Also set TeamViewer and AnyDesk to Manual. Off by default because you may
    rely on them to reach this machine remotely.

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File tools\trim-services.ps1
    powershell -ExecutionPolicy Bypass -File tools\trim-services.ps1 -Apply
#>

[CmdletBinding()]
param(
    [switch]$Apply,
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
    Write-Warn "Changing services requires Administrator. Re-run from an elevated shell."
    Write-Host "  Reporting only for now." -ForegroundColor Yellow
    $Apply = $false
}

# --------------------------------------------------------------------------
# Services that are safe to start on demand.
# `Why` is shown to the user so the decision is auditable.
# --------------------------------------------------------------------------
$targets = @(
    @{ Name='postgresql-x64-18';                    Why='full DB server at boot; start when a project needs it' }
    @{ Name='pgbouncer';                            Why='connection pooler for postgres; pointless without it' }
    @{ Name='PEMHTTPD-x64';                         Why='EDB Postgres Enterprise Manager web server' }
    @{ Name='CCleaner7';                            Why='duplicate cleaner; the repair script already covers this' }
    @{ Name='Grafana';                              Why='dashboards only; start before a review session' }
    @{ Name='LetsViewService';                      Why='phone screen mirroring, unused' }
    @{ Name='DragonUpdater';                        Why='COMODO Dragon browser updater' }
    @{ Name='Bonjour Service';                      Why='Apple mDNS responder, only needed for iTunes/AirPlay' }
    @{ Name='AdobeARMservice';                      Why='Adobe Reader updater' }
    @{ Name='IntelTelemetryAgent';                  Why='Intel telemetry, no user value' }
    @{ Name='SystemUsageReportSvc_QUEENCREEK';      Why='Intel usage reporting' }
    @{ Name='IntelCollectorService';                Why='Intel data collection' }
    @{ Name='PresentMonSharedService';              Why='frame-time capture for benchmarks' }
    @{ Name='DSAService';                           Why='Intel Driver Assistant; run it manually when updating' }
    @{ Name='DSAUpdateService';                     Why='Intel Driver Assistant updater' }
    @{ Name='CodexSandboxService.OpenAI.Codex';     Why='ChatGPT/Codex sandbox; launches ~15 processes' }
)

$optionalRemote = @(
    @{ Name='TeamViewer'; Why='remote access; keep if you depend on it' }
    @{ Name='AnyDesk';    Why='remote access; keep if you depend on it' }
)

if ($IncludeRemoteAccess) { $targets += $optionalRemote }

# --------------------------------------------------------------------------
Write-Section ("Service startup review" + $(if ($Apply) { ' - APPLYING' } else { ' - report only' }))

$changed = 0
$missing = 0

foreach ($t in $targets) {
    $svc = Get-Service -Name $t.Name -ErrorAction SilentlyContinue
    if (-not $svc) {
        $missing++
        Write-Info ("{0,-38} not installed" -f $t.Name)
        continue
    }

    $wmi = Get-CimInstance Win32_Service -Filter "Name='$($t.Name)'" -ErrorAction SilentlyContinue
    $current = if ($wmi) { $wmi.StartMode } else { '' }

    if ($current -eq 'Manual' -or $current -eq 'Disabled') {
        Write-Info ("{0,-38} already {1}" -f $t.Name, $current)
        continue
    }

    if ($Apply) {
        try {
            Set-Service -Name $t.Name -StartupType Manual -ErrorAction Stop
            Write-Ok ("{0,-38} Auto -> Manual" -f $t.Name)
            Write-Host ("         {0}" -f $t.Why) -ForegroundColor DarkGray
            $changed++
        } catch {
            Write-Warn ("{0,-38} failed: {1}" -f $t.Name, $_.Exception.Message.Split([char]10)[0])
        }
    } else {
        Write-Info ("{0,-38} {1} -> would become Manual" -f $t.Name, $current)
        Write-Host ("         {0}" -f $t.Why) -ForegroundColor DarkGray
    }
}

# --------------------------------------------------------------------------
Write-Section "Untouched (by design)"
foreach ($n in @('CmdAgent','CmdAgentProt','isesrv','WSLService','ClickToRunSvc')) {
    $s = Get-Service -Name $n -ErrorAction SilentlyContinue
    if ($s) { Write-Info ("{0,-38} left as {1}" -f $n, $s.StartType) }
}

# --------------------------------------------------------------------------
Write-Section "Kernel memory settings"
Write-Info "WSL is capped at half of installed RAM by default (~3.8 GB here)."
Write-Info "Creating %USERPROFILE%\.wslconfig with a smaller cap stops it competing."
if ($Apply) {
    $cfg = Join-Path $env:USERPROFILE '.wslconfig'
    if (Test-Path $cfg) {
        Write-Info "$cfg already exists; left alone"
    } else {
        @"
# Added by trim-services.ps1
# Cap the WSL VM so it cannot take half of an 8 GB laptop.
[wsl2]
memory=2GB
processors=2
swap=1GB
"@ | Set-Content -Path $cfg -Encoding ASCII
        Write-Ok "wrote $cfg (memory=2GB, processors=2, swap=1GB)"
        Write-Info "Takes effect after: wsl --shutdown"
    }
}

# --------------------------------------------------------------------------
Write-Section "Summary"
if ($Apply) {
    Write-Ok "$changed service(s) moved to Manual"
    Write-Info "Start any of them again with:  Start-Service <name>"
    Write-Info "Revert with:                   Set-Service <name> -StartupType Automatic"
} else {
    Write-Info "Nothing changed. Re-run with -Apply from an elevated shell."
}
Write-Info "$missing entr(ies) were not installed."
Write-Host ""
Write-Host "  Reboot to measure the difference, then compare:" -ForegroundColor Cyan
Write-Host "    (Get-Counter '\Memory\Committed Bytes').CounterSamples[0].CookedValue/1GB" -ForegroundColor White
Write-Host ""
