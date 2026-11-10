# Hive Mind REA Template - Windows install helper (run in PowerShell)
# Usage: powershell -ExecutionPolicy Bypass -File tools/install_windows.ps1

param(
    [switch]$InstallCLI,
    [switch]$CloneRepos,
    [switch]$ShowVersions
)

$ErrorActionPreference = "Continue"

function Check-Command($name) {
    $c = Get-Command $name -ErrorAction SilentlyContinue
    if ($c) { Write-Host ("[OK] {0}: {1}" -f $name, $c.Source) } else { Write-Host ("[MISSING] {0}" -f $name) }
}

if ($ShowVersions) {
    foreach ($n in @("git","node","npm","python","pip","docker","ffmpeg","yt-dlp","winget","code")) { Check-Command $n }
    Write-Host "Ollama:"; ollama --version 2>&1 | Select-Object -First 1
    Write-Host "Grafana:"; Get-Service Grafana -ErrorAction SilentlyContinue | Select-Object Name,Status,StartType
}

if ($InstallCLI) {
    Write-Host "Installing lightweight CLI tools (best-effort)..."
    if (Get-Command winget -ErrorAction SilentlyContinue) {
        winget install -e --id Gyan.FFmpeg --accept-package-agreements --accept-source-agreements 2>&1 | Select-Object -Last 5
        winget install -e --id yt-dlp.yt-dlp --accept-package-agreements --accept-source-agreements 2>&1 | Select-Object -Last 5
    } else {
        Write-Host "winget not available; install manually or via choco/scoop"
    }
    python -m pip install -U yt-dlp 2>&1 | Select-Object -Last 5
    python -m pip install faster-whisper 2>&1 | Select-Object -Last 5
}

if ($CloneRepos) {
    $root = Split-Path -Parent $PSScriptRoot
    $repos = Join-Path $root "repos"
    New-Item -ItemType Directory -Force -Path $repos | Out-Null
    Set-Location $repos
    $list = @(
        "https://github.com/livekit/livekit.git",
        "https://github.com/livekit/agents.git",
        "https://github.com/chatwoot/chatwoot.git",
        "https://github.com/calcom/cal.com.git",
        "https://github.com/opf/openproject.git",
        "https://github.com/Tencent/WeKnora.git",
        "https://github.com/CapSoftware/Cap.git"
    )
    foreach ($u in $list) {
        $name = ($u -split "/")[-1] -replace "\.git$",""
        if (Test-Path $name) { Write-Host "[SKIP] $name already exists"; continue }
        Write-Host "Cloning $name ..."
        git clone --depth 1 $u 2>&1 | Select-Object -Last 3
    }
}

Write-Host "Done. Configure MCP servers via mcp/opencode-mcp.example.json and API keys via .env (never commit secrets)."