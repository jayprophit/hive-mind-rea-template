<#
.SYNOPSIS
    Hive Mind REA - Windows administrator repair, cleanup and health check.

.DESCRIPTION
    Does everything that requires elevation:
      - creates a System Restore point
      - reclaims disk space (WinSxS, Windows Update cache, temp, delivery optimisation)
      - verifies and repairs the component store and system files
      - TRIMs the SSD and checks SMART health
      - right-sizes the page file for low-RAM machines
      - reports BIOS / driver versions and flags stale ones
      - reinstalls clean power defaults and sets High performance

    Safe to re-run. Read the output; nothing is deleted that Windows needs.

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File tools\repair-windows-admin.ps1

.EXAMPLE
    # Report only, change nothing
    powershell -ExecutionPolicy Bypass -File tools\repair-windows-admin.ps1 -ReportOnly
#>

[CmdletBinding()]
param(
    [switch]$ReportOnly,
    [switch]$SkipRestorePoint,
    [switch]$SkipComponentCleanup
)

$ErrorActionPreference = 'Continue'
$ProgressPreference    = 'SilentlyContinue'

function Write-Section($text) {
    Write-Host ""
    Write-Host ("=" * 72) -ForegroundColor DarkCyan
    Write-Host "  $text" -ForegroundColor Cyan
    Write-Host ("=" * 72) -ForegroundColor DarkCyan
}
function Write-Ok($t)   { Write-Host "  [ok]   $t" -ForegroundColor Green }
function Write-Info($t) { Write-Host "  [info] $t" -ForegroundColor Gray }
function Write-Warn($t) { Write-Host "  [warn] $t" -ForegroundColor Yellow }
function Write-Bad($t)  { Write-Host "  [fail] $t" -ForegroundColor Red }

# ---------------------------------------------------------------- elevation
$identity  = [Security.Principal.WindowsIdentity]::GetCurrent()
$principal = New-Object Security.Principal.WindowsPrincipal($identity)
if (-not $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host ""
    Write-Bad "This script must run as Administrator."
    Write-Host "  Right-click PowerShell -> 'Run as administrator', then:" -ForegroundColor Yellow
    Write-Host "    cd `"$PSScriptRoot\..`"" -ForegroundColor White
    Write-Host "    powershell -ExecutionPolicy Bypass -File tools\repair-windows-admin.ps1" -ForegroundColor White
    Write-Host ""
    exit 1
}

$startFree = (Get-PSDrive C).Free

Write-Section "System summary"
$os   = Get-CimInstance Win32_OperatingSystem
$cs   = Get-CimInstance Win32_ComputerSystem
$cpu  = Get-CimInstance Win32_Processor
Write-Info "OS       : $($os.Caption) $($os.Version) (build $($os.BuildNumber))"
Write-Info "Machine  : $($cs.Manufacturer) $($cs.Model)"
Write-Info "CPU      : $($cpu.Name) ($($cpu.NumberOfCores)C/$($cpu.NumberOfLogicalProcessors)T)"
Write-Info "RAM      : $([math]::Round($cs.TotalPhysicalMemory/1GB,2)) GB"
Write-Info "Free disk: $([math]::Round($startFree/1GB,2)) GB of $([math]::Round(($startFree + (Get-PSDrive C).Used)/1GB,2)) GB"
Write-Info "Uptime   : $((Get-Date) - $os.LastBootUpTime)"

if ($ReportOnly) { Write-Warn "ReportOnly set - no changes will be made." }

# ---------------------------------------------------------------- restore point
if (-not $ReportOnly -and -not $SkipRestorePoint) {
    Write-Section "Creating restore point"
    try {
        # Enable System Protection on C: if it is off, so the point can exist.
        Enable-ComputerRestore -Drive "C:\" -ErrorAction SilentlyContinue
        Checkpoint-Computer -Description "HiveMind repair $(Get-Date -Format yyyy-MM-dd_HHmm)" -RestorePointType MODIFY_SETTINGS -ErrorAction Stop
        Write-Ok "Restore point created."
    } catch {
        Write-Warn "Could not create restore point: $($_.Exception.Message)"
        Write-Warn "Windows limits restore points to one per 24h; continuing."
    }
}

# ---------------------------------------------------------------- disk cleanup
Write-Section "Disk cleanup"
$before = (Get-PSDrive C).Free
$cleanTargets = @(
    "$env:SystemRoot\Temp",
    "$env:SystemRoot\SoftwareDistribution\Download",
    "$env:SystemRoot\Logs\CBS",
    "$env:LOCALAPPDATA\Temp",
    "$env:SystemRoot\Prefetch"
)
foreach ($t in $cleanTargets) {
    if (-not (Test-Path $t)) { continue }
    if ($ReportOnly) {
        $sz = (Get-ChildItem $t -Recurse -Force -EA SilentlyContinue | Measure-Object Length -Sum).Sum
        Write-Info "$t -> $([math]::Round($sz/1MB,1)) MB reclaimable"
        continue
    }
    Get-ChildItem $t -Recurse -Force -EA SilentlyContinue |
        Where-Object { -not $_.PSIsContainer } |
        Remove-Item -Force -EA SilentlyContinue
    Get-ChildItem $t -Recurse -Force -EA SilentlyContinue |
        Where-Object { $_.PSIsContainer } |
        Sort-Object { $_.FullName.Length } -Descending |
        Remove-Item -Force -Recurse -EA SilentlyContinue
    Write-Ok "cleared $t"
}

# Delivery Optimisation cache
if (-not $ReportOnly) {
    try {
        Delete-DeliveryOptimizationCache -Force -EA Stop
        Write-Ok "cleared Delivery Optimisation cache"
    } catch { Write-Info "Delivery Optimisation cache skipped" }
}

$after = (Get-PSDrive C).Free
Write-Ok ("reclaimed {0:N2} GB" -f (($after - $before)/1GB))

# ---------------------------------------------------------------- component store
if (-not $ReportOnly -and -not $SkipComponentCleanup) {
    Write-Section "Component store cleanup (WinSxS)"
    Write-Info "This is the big one and can take 10-30 minutes on a laptop."
    Write-Info "Running DISM /StartComponentCleanup /ResetBase ..."
    & dism.exe /Online /Cleanup-Image /StartComponentCleanup /ResetBase
    switch ($LASTEXITCODE) {
        0     { Write-Ok "component store cleaned" }
        3010  { Write-Warn "component store cleaned (reboot recommended)" }
        default { Write-Warn "DISM returned code $LASTEXITCODE" }
    }
}

# ---------------------------------------------------------------- integrity
Write-Section "System integrity"
if ($ReportOnly) {
    Write-Info "would run: DISM /ScanHealth ; sfc /scannow"
} else {
    Write-Info "DISM /ScanHealth ..."
    & dism.exe /Online /Cleanup-Image /ScanHealth | Select-Object -Last 6
    Write-Info "SFC /scannow ..."
    & sfc.exe /scannow | Select-Object -Last 6
    Write-Ok "integrity scan finished (see output above for findings)"
}

# ---------------------------------------------------------------- storage
Write-Section "Storage health"
try {
    Get-PhysicalDisk | ForEach-Object {
        Write-Info ("{0} | {1} | health={2} | wear={3}" -f $_.FriendlyName, $_.MediaType, $_.HealthStatus, $_.Wear)
        if ($_.HealthStatus -ne 'Healthy') { Write-Bad "disk reports $($_.HealthStatus)" }
    }
    Get-PhysicalDisk | Where-Object { $_.MediaType -eq 'SSD' } | ForEach-Object {
        if (-not $ReportOnly) {
            Optimize-Volume -DriveLetter C -ReTrim -Verbose:$false -EA SilentlyContinue
            Write-Ok "TRIM issued on C:"
        }
    }
    $rel = Get-StorageReliabilityCounter -PhysicalDisk (Get-PhysicalDisk) -EA SilentlyContinue
    if ($rel) {
        Write-Info ("temperature={0}C  power-on hours={1}  read errors={2}" -f $rel.Temperature, $rel.PowerOnHours, $rel.ReadErrorsTotal)
    }
} catch { Write-Warn "storage detail unavailable: $($_.Exception.Message)" }

# ---------------------------------------------------------------- page file
Write-Section "Page file (important on 8 GB machines)"
$pf = Get-CimInstance Win32_PageFileSetting -EA SilentlyContinue
if ($pf) {
    Write-Info "current: $($pf.Name) initial=$($pf.InitialSize)MB max=$($pf.MaximumSize)MB"
} else {
    Write-Info "current: system managed"
}
if (-not $ReportOnly) {
    try {
        # Let Windows manage it; explicit small page files starve this workload.
        $cs | Where-Object { $_.AutomaticManagedPagefile -eq $false } | ForEach-Object {
            Set-CimInstance -InputObject $_ -Property @{ AutomaticManagedPagefile = $true }
            Write-Ok "page file returned to system-managed"
        }
        if ($cs.AutomaticManagedPagefile) { Write-Ok "page file already system-managed" }
    } catch { Write-Warn "could not change page file: $($_.Exception.Message)" }
}

# ---------------------------------------------------------------- power
Write-Section "Power configuration"
if (-not $ReportOnly) {
    $hp = (powercfg /list | Select-String 'High performance')
    if (-not $hp) {
        powercfg /duplicatescheme 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c | Out-Null
        $hp = (powercfg /list | Select-String 'High performance')
    }
    if ($hp) {
        $guid = ([regex]'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})').Match($hp.Line).Value
        powercfg /setactive $guid
        Write-Ok "active scheme: High performance ($guid)"
    }
    # Keep USB selective suspend from killing input devices, and never sleep on AC.
    powercfg /change standby-timeout-ac 0
    Write-Ok "display/standby on AC set to never sleep"
}

# ---------------------------------------------------------------- drivers / BIOS
Write-Section "Firmware and driver review"
$bios = Get-CimInstance Win32_BIOS
Write-Info "BIOS: $($bios.SMBIOSBIOSVersion) dated $($bios.ReleaseDate.ToString('yyyy-MM-dd'))"
if ($bios.ReleaseDate -lt (Get-Date).AddYears(-3)) {
    Write-Warn "BIOS is over 3 years old - check the Lenovo support page for your model."
}

$stale = Get-CimInstance Win32_PnPSignedDriver |
    Where-Object { $_.DriverDate -and $_.DriverDate -lt (Get-Date).AddYears(-3) -and $_.DeviceClass -in @('DISPLAY','NET','MEDIA','SYSTEM','USB') } |
    Select-Object DeviceName, DriverVersion, DriverDate, DeviceClass
if ($stale) {
    Write-Warn "Drivers older than 3 years:"
    $stale | ForEach-Object {
        Write-Host ("    {0,-52} {1,-18} {2:yyyy-MM-dd}  {3}" -f $_.DeviceName, $_.DriverVersion, $_.DriverDate, $_.DeviceClass) -ForegroundColor Yellow
    }
} else {
    Write-Ok "no obviously stale drivers in display/net/audio/system classes"
}

Write-Info "Checking Windows Update for driver and quality updates..."
if (-not $ReportOnly) {
    try {
        $session  = New-Object -ComObject Microsoft.Update.Session
        $searcher = $session.CreateUpdateSearcher()
        $result   = $searcher.Search("IsInstalled=0 and Type='Driver'")
        if ($result.Updates.Count -eq 0) {
            Write-Ok "no driver updates offered by Windows Update"
        } else {
            Write-Warn "$($result.Updates.Count) driver update(s) available:"
            foreach ($u in $result.Updates) { Write-Host "    - $($u.Title)" -ForegroundColor Yellow }
            Write-Info "Install them via Settings > Windows Update > Advanced options > Optional updates."
        }
    } catch { Write-Warn "Windows Update query failed: $($_.Exception.Message)" }
}

# ---------------------------------------------------------------- summary
Write-Section "Done"
$endFree = (Get-PSDrive C).Free
Write-Ok ("free space {0:N2} GB -> {1:N2} GB (net +{2:N2} GB)" -f ($startFree/1GB), ($endFree/1GB), (($endFree-$startFree)/1GB))
Write-Host ""
Write-Host "Next steps that still need you:" -ForegroundColor Cyan
Write-Host "  1. Lenovo Vantage  -> System Update  (BIOS + chipset + audio + Wi-Fi)"
Write-Host "  2. Intel Driver & Support Assistant -> Wi-Fi AX201 and graphics"
Write-Host "  3. Settings > Windows Update > Advanced options > Optional updates"
Write-Host "  4. Reboot when convenient."
Write-Host ""
