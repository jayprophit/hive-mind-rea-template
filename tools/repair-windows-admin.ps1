<#
.SYNOPSIS
    Hive Mind REA - Windows administrator repair, cleanup and health check.

.DESCRIPTION
    Written to survive a memory-starved machine. Every expensive probe is
    guarded, and the script refuses to start work it cannot finish.

    Sections, in order:
      1. memory precheck      - aborts early instead of failing everywhere
      2. restore point
      3. disk cleanup
      4. system integrity     - DISM scan + SFC
      5. component store      - OPT-IN, because it needs lots of free memory
      6. storage health / TRIM
      7. page file
      8. power configuration
      9. firmware + driver review

    Why the guards exist: on an 8 GB machine under load, Get-CimInstance and
    DISM fail with HRESULT 0x8007000e ("Not enough memory resources") and
    "Error: 5 - An initialization error occurred". That is resource
    exhaustion, not a permissions problem, and it cascades through a naive
    script. These guards turn that into one clear message.

.PARAMETER Minimal
    Only do the cheap, safe work: cleanup, TRIM, power. Skips DISM/SFC.

.PARAMETER ReportOnly
    Change nothing. Print findings.

.PARAMETER ComponentCleanup
    Run DISM /StartComponentCleanup /ResetBase. Slow (10-30 min) and needs
    several GB free. Off by default.

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File tools\repair-windows-admin.ps1 -Minimal
#>

[CmdletBinding()]
param(
    [switch]$ReportOnly,
    [switch]$Minimal,
    [switch]$ComponentCleanup,
    [switch]$SkipRestorePoint
)

$ErrorActionPreference = 'Continue'
$ProgressPreference    = 'SilentlyContinue'

# ============================================================ output helpers
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
function Write-Step($t) { Write-Host "  >> $t" -ForegroundColor DarkGray }

# ============================================================ safe probing
# CIM is the first thing to die under memory pressure. Fall back to .NET,
# which needs no WMI provider host.
function Get-SafeCim {
    param([string]$Class, [string]$Namespace = 'root\cimv2')
    try   { return Get-CimInstance -ClassName $Class -Namespace $Namespace -ErrorAction Stop }
    catch { return $null }
}

function Get-SafeDrive {
    param([string]$Letter = 'C')
    try {
        $d = [System.IO.DriveInfo]::new("${Letter}:")
        if ($d.IsReady) {
            return [pscustomobject]@{
                Free = $d.AvailableFreeSpace
                Total = $d.TotalSize
                Used  = $d.TotalSize - $d.AvailableFreeSpace
            }
        }
    } catch { }
    try { return Get-PSDrive $Letter -ErrorAction Stop } catch { return $null }
}

function Get-CommitStatus {
    # Commit charge is the number that actually matters. Physical free RAM
    # can look fine while the system is 2x over-committed and thrashing.
    try {
        $os = Get-SafeCim 'Win32_OperatingSystem'
        if ($os) {
            return [pscustomobject]@{
                FreeGB   = $os.FreePhysicalMemory / 1MB
                TotalGB  = $os.TotalVisibleMemorySize / 1MB
                CommitGB = $os.TotalVirtualMemorySize / 1MB
                Source   = 'cim'
            }
        }
    } catch { }

    try {
        $free = [GC]::GetTotalMemory($true)
        $cs   = Get-SafeCim 'Win32_ComputerSystem'
        if ($cs) {
            return [pscustomobject]@{
                FreeGB   = $null
                TotalGB  = $cs.TotalPhysicalMemory / 1GB
                CommitGB = $null
                Source   = 'cim-partial'
            }
        }
    } catch { }
    return $null
}

# ============================================================ elevation
$identity  = [Security.Principal.WindowsIdentity]::GetCurrent()
$principal = New-Object Security.Principal.WindowsPrincipal($identity)
$isAdmin   = $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host ""
    Write-Bad "This script must run as Administrator."
    Write-Host "  Right-click Start -> Terminal (Admin), then re-run." -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

$startDrive = Get-SafeDrive 'C'
$startFree  = if ($startDrive) { [double]$startDrive.Free } else { 0 }

# ============================================================ 1. precheck
Write-Section "Pre-flight"

$mem = Get-CommitStatus
if (-not $mem) {
    Write-Warn "Could not read memory counters at all. The system is likely in bad shape."
    Write-Warn "Reboot, then re-run this script before opening any other application."
} else {
    Write-Info ("RAM: {0:N1} GB visible, {1:N1} GB free" -f $mem.TotalGB, $mem.FreeGB)
    if ($mem.CommitGB) {
        $ratio = $mem.CommitGB / $mem.TotalGB
        Write-Info ("Commit charge: {0:N1} GB ({1:N1}x physical)" -f $mem.CommitGB, $ratio)
        if ($ratio -gt 1.5) {
            Write-Bad  "The system is critically over-committed."
            Write-Warn "WMI, DISM and SFC will fail with 'Not enough memory resources'."
            Write-Warn "That is not a permissions problem."
            Write-Host ""
            Write-Host "  Do this first:" -ForegroundColor Yellow
            Write-Host "    1. Close browsers, editors and agent sessions" -ForegroundColor White
            Write-Host "    2. wsl --shutdown        (releases the WSL VM)" -ForegroundColor White
            Write-Host "    3. Reboot" -ForegroundColor White
            Write-Host "    4. Re-run this script   (it is cheap and fast)" -ForegroundColor White
            Write-Host ""
            if (-not $ReportOnly) {
                Write-Warn "Continuing with cleanup only; skipping integrity work."
                $Minimal = $true
            }
        }
    }
}

if ($startDrive) {
    Write-Info ("Free disk: {0:N1} GB of {1:N1} GB" -f ($startFree/1GB), ($startDrive.Total/1GB))
} else {
    Write-Warn "Could not read disk statistics."
}

$os = Get-SafeCim 'Win32_OperatingSystem'
if ($os) {
    Write-Info "OS: $($os.Caption) $($os.Version) build $($os.BuildNumber)"
}
$cpu = Get-SafeCim 'Win32_Processor' | Select-Object -First 1
if ($cpu) { Write-Info "CPU: $($cpu.Name) ($($cpu.NumberOfCores)C/$($cpu.NumberOfLogicalProcessors)T)" }

# ============================================================ 2. restore point
if (-not $ReportOnly -and -not $SkipRestorePoint) {
    Write-Section "Restore point"
    try {
        Enable-ComputerRestore -Drive "C:\" -ErrorAction SilentlyContinue
        Checkpoint-Computer -Description "HiveMind $(Get-Date -Format yyyy-MM-dd_HHmm)" `
                            -RestorePointType MODIFY_SETTINGS -ErrorAction Stop
        Write-Ok "restore point created"
    } catch {
        Write-Warn "skipped: $($_.Exception.Message.Split([char]10)[0])"
        Write-Info "Windows allows one restore point per 24 hours; not fatal."
    }
}

# ============================================================ 3. disk cleanup
Write-Section "Disk cleanup"
$cleanTargets = @(
    "$env:SystemRoot\Temp",
    "$env:SystemRoot\SoftwareDistribution\Download",
    "$env:SystemRoot\Logs\CBS",
    "$env:LOCALAPPDATA\Temp",
    "$env:SystemRoot\Prefetch"
)
foreach ($t in $cleanTargets) {
    if (-not (Test-Path $t)) { continue }
    $sz = (Get-ChildItem $t -Recurse -Force -EA SilentlyContinue |
           Measure-Object Length -Sum).Sum
    if ($ReportOnly) {
        Write-Info ("{0} -> {1:N1} MB" -f $t, ($sz/1MB))
        continue
    }
    Get-ChildItem $t -Recurse -Force -EA SilentlyContinue |
        Where-Object { -not $_.PSIsContainer } |
        Remove-Item -Force -EA SilentlyContinue
    Get-ChildItem $t -Recurse -Force -EA SilentlyContinue |
        Where-Object { $_.PSIsContainer } |
        Sort-Object { $_.FullName.Length } -Descending |
        Remove-Item -Force -Recurse -EA SilentlyContinue
    Write-Ok ("cleared {0} ({1:N0} MB)" -f $t, ($sz/1MB))
}

if (-not $ReportOnly) {
    try {
        Delete-DeliveryOptimizationCache -Force -EA Stop | Out-Null
        Write-Ok "cleared Delivery Optimisation cache"
    } catch {
        Write-Warn "Delivery Optimisation cache skipped (service or memory unavailable)"
    }
}

# ============================================================ 4. integrity
if (-not $Minimal -and -not $ReportOnly) {
    Write-Section "System integrity"
    Write-Step "DISM /ScanHealth"
    $dismOut = & dism.exe /Online /Cleanup-Image /ScanHealth 2>&1
    $dismCode = $LASTEXITCODE
    $dismOut | Select-Object -Last 8 | ForEach-Object { Write-Info $_ }

    switch ($dismCode) {
        0     { Write-Ok "component store is healthy" }
        3010  { Write-Warn "repair applied; reboot needed" }
        5     { Write-Bad "DISM could not initialise (error 5)."
                Write-Warn "Either not elevated, or the system is out of memory. Check the pre-flight section." }
        default { Write-Warn "DISM returned $dismCode - see C:\Windows\Logs\DISM\dism.log" }
    }

    Write-Step "SFC /scannow"
    $sfcOut = & sfc.exe /scannow 2>&1
    $sfcOut | Select-Object -Last 6 | ForEach-Object { Write-Info $_ }
    if ($LASTEXITCODE -eq 0) { Write-Ok "SFC completed" }
    else { Write-Warn "SFC could not complete (usually memory pressure)" }
}

# ============================================================ 5. component store
if ($ComponentCleanup -and -not $Minimal -and -not $ReportOnly) {
    Write-Section "Component store cleanup (WinSxS)"
    $d = Get-SafeDrive 'C'
    $freeGB = if ($d) { $d.Free / 1GB } else { 0 }
    if ($freeGB -lt 12) {
        Write-Warn ("skipped: needs ~12 GB free, only {0:N1} GB available" -f $freeGB)
    } elseif ($mem -and $mem.CommitGB -and ($mem.CommitGB / $mem.TotalGB) -gt 1.3) {
        Write-Warn "skipped: memory still over-committed"
    } else {
        Write-Info "running DISM /StartComponentCleanup /ResetBase (10-30 minutes)"
        & dism.exe /Online /Cleanup-Image /StartComponentCleanup /ResetBase
        if ($LASTEXITCODE -in 0, 3010) { Write-Ok "component store cleaned" }
        else { Write-Warn "DISM returned $LASTEXITCODE" }
    }
} else {
    Write-Info "component store cleanup not requested (use -ComponentCleanup when disk is tight)"
}

# ============================================================ 6. storage
Write-Section "Storage health"
$disks = Get-SafeCim 'MSFT_PhysicalDisk' -Namespace 'root\Microsoft\Windows\Storage'
if (-not $disks) { $disks = Get-SafeCim 'Win32_DiskDrive' }
if ($disks) {
    foreach ($d in $disks) {
        $name   = $d.FriendlyName; if (-not $name) { $name = $d.Model }
        $health = $d.HealthStatus;  if (-not $health) { $health = $d.Status }
        Write-Info "$name | health=$health"
        if ($health -and $health -notmatch 'Healthy|OK') { Write-Bad "disk reports $health" }
    }
} else {
    Write-Warn "could not enumerate disks (memory pressure)"
}

if (-not $ReportOnly) {
    try {
        Optimize-Volume -DriveLetter C -ReTrim -EA Stop
        Write-Ok "TRIM issued on C:"
    } catch {
        Write-Warn "TRIM skipped: $($_.Exception.Message.Split([char]10)[0])"
    }
}

# ============================================================ 7. page file
Write-Section "Page file"
$cs = Get-SafeCim 'Win32_ComputerSystem'
if ($cs) {
    Write-Info "automatic page file: $($cs.AutomaticManagedPagefile)"
    if (-not $ReportOnly -and -not $cs.AutomaticManagedPagefile) {
        try {
            Set-CimInstance -InputObject $cs -Property @{ AutomaticManagedPagefile = $true } -EA Stop
            Write-Ok "returned to system-managed"
        } catch { Write-Warn "could not change page file" }
    }
} else {
    Write-Info "system-managed (default); could not confirm via CIM"
}

# ============================================================ 8. power
Write-Section "Power"
if (-not $ReportOnly) {
    $schemes = powercfg /list
    $hp = $schemes | Select-String 'High performance'
    if (-not $hp) {
        powercfg /duplicatescheme 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c | Out-Null
        $schemes = powercfg /list
        $hp = $schemes | Select-String 'High performance'
    }
    if ($hp) {
        $guid = ([regex]'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})').Match($hp.Line).Value
        powercfg /setactive $guid | Out-Null
        Write-Ok "active scheme: High performance"
    }
    powercfg /change standby-timeout-ac 0 | Out-Null
    Write-Ok "standby on AC: never"
}

# ============================================================ 9. firmware
Write-Section "Firmware and drivers"
$bios = Get-SafeCim 'Win32_BIOS'
if ($bios -and $bios.ReleaseDate) {
    $age = ((Get-Date) - $bios.ReleaseDate).TotalDays / 365
    Write-Info ("BIOS {0} dated {1:yyyy-MM-dd} ({2:N1} years old)" -f `
        $bios.SMBIOSBIOSVersion, $bios.ReleaseDate, $age)
    if ($age -gt 3) { Write-Warn "check the Lenovo support page for your model" }
} else {
    Write-Warn "BIOS version unavailable (memory pressure)"
}

$drivers = Get-SafeCim 'Win32_PnPSignedDriver'
if ($drivers) {
    $cutoff = (Get-Date).AddYears(-3)
    $stale = $drivers |
        Where-Object { $_.DriverDate -and $_.DriverDate -lt $cutoff -and
                       $_.DeviceClass -in @('DISPLAY','NET','MEDIA','SYSTEM','USB') }
    if ($stale) {
        Write-Warn "$($stale.Count) driver(s) older than 3 years:"
        $stale | Select-Object -First 12 | ForEach-Object {
            Write-Host ("    {0,-50} {1,-16} {2:yyyy-MM-dd}  {3}" -f `
                $_.DeviceName, $_.DriverVersion, $_.DriverDate, $_.DeviceClass) -ForegroundColor Yellow
        }
    } else {
        Write-Ok "no stale drivers in display/net/audio/system/usb"
    }
} else {
    Write-Warn "driver inventory unavailable (memory pressure)"
}

if (-not $Minimal -and -not $ReportOnly) {
    Write-Step "Windows Update driver search"
    try {
        $session  = New-Object -ComObject Microsoft.Update.Session
        $searcher = $session.CreateUpdateSearcher()
        $result   = $searcher.Search("IsInstalled=0 and Type='Driver'")
        if ($result.Updates.Count -eq 0) {
            Write-Ok "no driver updates offered"
        } else {
            Write-Warn "$($result.Updates.Count) driver update(s) available:"
            foreach ($u in $result.Updates) { Write-Host "    - $($u.Title)" -ForegroundColor Yellow }
            Write-Info "Install via Settings > Windows Update > Advanced options > Optional updates"
        }
    } catch {
        Write-Warn "Windows Update query failed (memory or service state)"
    }
}

# ============================================================ summary
Write-Section "Done"
$endDrive = Get-SafeDrive 'C'
if ($startDrive -and $endDrive) {
    Write-Ok ("free space {0:N2} GB -> {1:N2} GB (net +{2:N2} GB)" -f `
        ($startFree/1GB), ($endDrive.Free/1GB), (($endDrive.Free - $startFree)/1GB))
} else {
    Write-Info "free space could not be measured"
}

Write-Host ""
Write-Host "  Still needs you:" -ForegroundColor Cyan
Write-Host "    1. Lenovo Vantage -> System Update   (BIOS, chipset, audio, Wi-Fi)" -ForegroundColor White
Write-Host "    2. Intel Driver & Support Assistant (Wi-Fi AX201, graphics)" -ForegroundColor White
Write-Host "    3. Settings > Windows Update > Advanced options > Optional updates" -ForegroundColor White
Write-Host "    4. Reboot when convenient" -ForegroundColor White
Write-Host ""
Write-Host "  On 8 GB RAM, the single biggest speed win is closing apps and" -ForegroundColor Cyan
Write-Host "  running one model at a time. RAM is the ceiling, not drivers." -ForegroundColor Cyan
Write-Host ""
