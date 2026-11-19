# Troubleshooting

Symptom first. Every entry here was hit on a real machine and fixed.

---

## The agent stops mid-prompt and never finishes

**Not an MCP problem.** The local stack is almost always healthy; the failure is upstream.

Check, in order:

1. `python scripts/doctor.py` — if no `[fail]` lines, the local side is fine.
2. Provider balance. The reference failure was:
   ```
   AI.Error: Insufficient balance. Top up at https://opencode.ai/console/...
   ```
   Topping up, or switching to a local model, resolves it.
3. Test with a local model to prove the rest of the chain:
   ```bash
   opencode --model ollama/lfm3:1.7b
   ```

---

## An MCP server closes immediately

### `ERR_MODULE_NOT_FOUND` from `npx`

A corrupted npx cache. The package graph is incomplete, so the child process exits
before the MCP session proves healthy.

```bash
rm -rf ~/AppData/Local/npm-cache/_npx/*   # Windows
rm -rf ~/.npm/_npx/*                      # macOS / Linux
npx -y rea-agents@6.7.0 --version         # must print a version
```

Then restart the host (Hermes / OpenCode).

### `${SOME_VAR}` in a config is never substituted

MCP configs pass `${VAR}` through to the child process environment. If the variable is
unset the child may fail silently. Set it at user scope:

```powershell
[Environment]::SetEnvironmentVariable("REA_PWNTOOLS_PYTHON", (Get-Command python).Source, "User")
```

```bash
export REA_PWNTOOLS_PYTHON="$(which python3)"
```

---

## `pip` is broken

```
ModuleNotFoundError: No module named 'pip._vendor.rich._emoji_codes'
```

Repair in place — no need to reinstall Python:

```bash
python -m ensurepip --upgrade
python -m pip install --user pwntools
```

---

## A tool says "not installed" but it clearly is

GUI installers routinely do not add themselves to `PATH`. Both `doctor.py` and
`bootstrap.py` probe conventional install roots before reporting a miss:

- Windows: `C:\Program Files\Craft Anything`, `C:\Program Files\Ollama`
- macOS: `/Applications/Craft Anything.app/Contents/MacOS`, `/opt/homebrew/bin`
- Linux: `/usr/local/bin`, `~/.local/bin`

If a tool lives somewhere else, put it on `PATH` or symlink it into one of those roots.

---

## Hermes: `No __init__.py` when loading a plugin

Some v3 plugins are dashboard-only and ship no Python package. Either add a minimal
`__init__.py`:

```python
__version__ = "3.0.0"
```

…or disable the plugin. The dashboard mounts from `dashboard/api.py` either way.

---

## Stale locks after moving a checkout

This is why runtime state is git-ignored. If you see `*.lock`, `state.db`,
`gateway.lock` or `ticker_heartbeat` inside a commit, the repo is broken for every
machine that clones it. Remove them from the index, keep them on disk:

```bash
git rm --cached -r $(git ls-files | grep -E '\.lock$|state\.db|/logs/|/cache/')
```

Never delete the working copy — only the index entry.

---

## Two Obsidian vaults, notes going missing

A split second brain. Obsidian cannot merge them for you.

1. Pick the canonical vault (`obsidian-vault/` in the repo by convention).
2. Copy only `*.md` across. Do **not** copy `.obsidian/` — workspace state is per machine.
3. Archive the old vault; do not keep it open in Obsidian.

---

## Out of disk space

Order of operations, largest win first:

1. Docker images — `docker system prune -a` (often 10 GB+). Stop the daemon if unused.
2. WinSxS + Windows Update cache — `tools/repair-windows-admin.ps1`, elevated.
3. Model weights you do not use — `ollama rm <model>`.
4. Temp directories.
5. `hiberfil.sys` — `powercfg /h off` frees roughly your RAM in size, but you lose hibernate.

---

## The laptop is slow with an agent running

On 8 GB of RAM this is expected, and no driver update changes it. In order:

1. Run **one** model at a time.
2. Close browsers before a session (Chrome alone can hold 1.5 GB).
3. Stop Docker unless you need the containers.
4. Check `Get-Process | Sort-Object WorkingSet64 -Descending | Select -First 10`.
5. If `Memory Compression` is above ~500 MB, you are thrashing — nothing else will help
   except adding RAM.

Minimum useful upgrade on this class of laptop: 8 GB SODIMM to reach 12–16 GB.

---

## Commit charge is higher than physical RAM before you open anything

Symptom: right after a reboot, `(Get-Counter '\Memory\Committed Bytes')` reports more
than installed RAM, and every `Get-CimInstance` / `DISM` / `SFC` call fails with
`0x8007000e` (not enough memory resources).

The cause is services that start automatically, not the applications you launch.
Measure before changing anything:

```powershell
Get-Process | Group-Object ProcessName |
  ForEach-Object { [pscustomobject]@{
      Name = $_.Name; N = $_.Count
      MB   = [math]::Round((($_.Group | Measure-Object PrivateMemorySize64 -Sum).Sum)/1MB, 0)
  } } | Sort-Object MB -Descending | Select-Object -First 15
```

Then `tools/trim-services.ps1` — report only, then `-Apply -StopNow`. Tier 1 has no
functional tradeoff; Tier 2 (PostgreSQL stack, Codex sandbox) means starting those
yourself. Real result on an 8 GB laptop: 15 services moved to Manual, 14.9 GB → 9.9 GB.

### Three things that look like startup entries but are not

**Packaged services refuse `Set-Service` even when elevated.** `CodexSandboxService.OpenAI.Codex`
answers `Access is denied`. Its security descriptor grants only Authenticated Users and the
package SID — Administrators are not in it. The registry holds the same value and *is*
writable when elevated:

```powershell
Set-ItemProperty 'HKLM:\SYSTEM\CurrentControlSet\Services\<ServiceName>' -Name Start -Value 3
```

`2` = Automatic, `3` = Manual, `4` = Disabled. `trim-services.ps1` falls back to this
automatically. Restart is not required; `sc.exe stop <name>` applies it now.

**Windows reopens your apps at sign-in.** If processes come back with `sihost.exe` as parent
and there is no `Run` entry, it is app restore, not autostart:

```powershell
Set-ItemProperty 'HKCU:\Software\Microsoft\Windows NT\CurrentVersion\Winlogon' -Name RestartApps -Value 0
```

**`vmmemWSL` is a virtual machine, not a program.** WSL2 defaults to half of physical RAM and
does not return it at idle. Cap it in `%USERPROFILE%\.wslconfig`, then `wsl --shutdown`:

```ini
[wsl2]
memory=2GB
processors=2
swap=1GB
```

On the reference machine that alone released 2.9 GB.

