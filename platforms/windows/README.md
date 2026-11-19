# Windows 10 / 11

Reference platform. Everything in the template has been exercised here.

## Install

```powershell
# 1. Prerequisites
winget install --id Git.Git -e
winget install --id OpenJS.NodeJS.LTS -e
winget install --id Ollama.Ollama -e

# 2. Clone (never copy a working tree)
git clone https://github.com/jayprophit/hive-mind-rea-template.git C:\hive
cd C:\hive

# 3. Inspect then apply
python scripts\doctor.py
python scripts\bootstrap.py --apply --scaffold-vault

# 4. One model to start
ollama pull lfm3:1.7b
```

## Paths

| What | Where |
|---|---|
| OpenCode config | `%USERPROFILE%\.config\opencode\opencode.json` |
| OpenCode agents | `%USERPROFILE%\.config\opencode\agents\` |
| Hermes home | `%LOCALAPPDATA%\hermes` |
| Stack data | `%LOCALAPPDATA%\hive-mind` |
| Vault | `<repo>\obsidian-vault` |

OpenCode uses `~/.config` on Windows too — that is deliberate, so the same config
paths work on every OS.

## Maintenance

```powershell
# Elevated. Restore point, WinSxS + WU cache cleanup, DISM/SFC, TRIM,
# page file, power plan, stale driver report.
powershell -ExecutionPolicy Bypass -File .\tools\repair-windows-admin.ps1

# Preview without changing anything
powershell -ExecutionPolicy Bypass -File .\tools\repair-windows-admin.ps1 -ReportOnly
```

## Windows 10 specifics

- PowerShell 5.1 is the default. Both Python scripts avoid PS-only syntax on purpose.
- `winget` may need the App Installer update from the Store first.
- Virtual terminal colours are off on older builds; `doctor.py` degrades to plain text.
- Windows Defender and a third-party AV both running will cost you ~1 GB of RAM.
  Pick one.

## WSL2

The reverse-engineering tools that behave badly on native Windows live here:

```bash
wsl --install -d Ubuntu
sudo apt-get update && sudo apt-get install -y gdb binutils tshark
```

Keep the repo on the Windows filesystem and run `doctor.py` from Windows; run the
Linux tooling inside WSL against the same files.
