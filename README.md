# Hive Mind REA Template

**A local-first AI development and reverse-engineering suite that runs on any desktop OS.**

Windows 10/11 · macOS · Linux · WSL — one configuration, one vault, one command.

[![Status](https://img.shields.io/badge/status-working-brightgreen)](#verified-status)
[![Platforms](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-blue)](#platform-support)
[![License](https://img.shields.io/badge/license-see%20LICENSE-lightgrey)](#)

---

## What this is

A reproducible setup for a **local AI team** that does real work on a normal laptop:
it codes, reviews, researches, drives the desktop, reverse-engineers binaries, and
keeps a written record of every turn in an Obsidian vault.

Nothing here needs a cloud API key. Everything degrades gracefully: run one model on
8 GB of RAM, or ten on 32 GB.

**This repo is configuration, not a running system.** It installs *into* a machine.
Runtime state (databases, locks, logs, session history) is deliberately excluded, so
the same checkout works on your Windows 11 laptop, your Windows 10 desktop, a Mac and
a Linux box without carrying stale state between them.

---

## Platform support

| Platform | Status | Notes |
|---|---|---|
| **Windows 11** | Verified working | Reference build. i3-1005G1, 8 GB, Intel UHD. |
| **Windows 10** | Supported | Same scripts. `scripts/doctor.py` handles PowerShell 5.1. |
| **WSL2 (Ubuntu)** | Supported | Best option for the reverse-engineering toolchain. |
| **macOS** (Intel / Apple silicon) | Supported | Paths resolve to `~/Library/Application Support`. |
| **Linux** (Debian/Ubuntu/Fedora) | Supported | XDG paths. `apt`/`dnf` hints in `core/stack.yaml`. |

The installers are written but only the Windows path has been exercised end to end.
Treat macOS/Linux as *expected to work, not yet proven* — run `scripts/doctor.py`
and open an issue with its output if something is off.

---

## Quick start

```bash
git clone https://github.com/jayprophit/hive-mind-rea-template.git
cd hive-mind-rea-template
python scripts/doctor.py          # what does this machine already have?
python scripts/bootstrap.py       # dry run: show what would change
python scripts/bootstrap.py --apply --scaffold-vault
```

Then pull one small model and start:

```bash
ollama pull lfm3:1.7b             # 1.1 GB, tool calling, fast on CPU
ollama serve
```

Windows users get a one-file maintenance script as well:

```powershell
# In an *Administrator* PowerShell
powershell -ExecutionPolicy Bypass -File .\tools\repair-windows-admin.ps1
```

---

## How it is organised

```
core/
  stack.yaml            Single source of truth: components, ports, models, roles.
                        Nothing OS-specific lives here.
scripts/
  doctor.py             Cross-platform health check. No dependencies.
  bootstrap.py          Cross-platform installer and config writer.
platforms/              Per-OS notes and shims.
  windows/  macos/  linux/
opencode/
  agents/*.md           22 agent prompts, portable markdown.
hermes/
  profiles/             Role configs. State files are git-ignored.
obsidian-vault/         The second brain. Exactly one vault.
grafana/provisioning/   Datasources + work-matrix dashboard.
docker/                 Optional heavy services (OpenProject, Chatwoot, LiveKit).
docs/                   Architecture, integrations, install notes.
tools/                  Windows maintenance and installer scripts.
```

### The one rule that makes this portable

> **Config lives in the repo. State lives on the machine.**

`state.db`, `*.lock`, `logs/`, `cache/`, `sessions/`, `*.db-wal` are all git-ignored.
If you ever see a lock file in a commit, that is a bug — it will be inherited by the
next machine and wedge it.

---

## The stack

| Layer | Component | Port | Role |
|---|---|---|---|
| Models | **Ollama** | 11434 | Local LLM runtime |
| Supervisor | **Hermes** | CLI | Routes work, delegates to roles |
| Coding | **OpenCode** | CLI | Subagents, structured edits, MCP |
| Investigation | **Craft Anything** | stdio/MCP | How does this software actually work |
| Desktop control | **OpenClaw** | 18789 | Files, Office, browser, screen |
| Dashboards | **Grafana** | 3000 | Work matrix over the vault |
| Knowledge | **Obsidian** | vault | The second brain |
| Optional | **Docker** | 2375 | Heavy services, start only when needed |

### Reverse-engineering toolchain

`Craft Anything` (MCP) · `Ghidra` · `JADX` · `Rizin` · `mitmproxy` · `Frida`
· `tshark` · `GDB` · `objdump` · `ffmpeg` · `yt-dlp`

On Windows, the ELF/GDB/packet tools are best run inside **WSL2** rather than
natively. `scripts/doctor.py` reports which are present.

---

## Research and reporting toolkit

Four dependency-free scripts turn "find something out" into a document you can
hand to someone. They exist because hosted search billed per query and stopped
working when the balance ran out, while a script that scrapes Google or Bing
gets a bot challenge instead of results.

| Script | Does | Needs |
|---|---|---|
| `scripts/research.py` | Search, fetch pages as readable text | nothing |
| `scripts/office.py` | Write `.xlsx` `.docx` `.pptx` `.csv` | `pip install openpyxl python-docx python-pptx` |
| `scripts/viz.py` | Charts (SVG/HTML) and Mermaid diagrams | nothing |
| `scripts/doctor.py` | Health check | nothing |

```bash
python -m pip install --user openpyxl python-docx python-pptx

python scripts/research.py "ideapad 3 15iil05 memory upgrade"
python scripts/research.py --url https://download.lenovo.com/consumer/mobiles/emcn60ww.txt
python scripts/research.py --hn "opencode mcp server"

python scripts/viz.py --from samples/ram-options.json --chart bar \
    --x Module --y Price_GBP -o ram.svg --title "RAM options" --html

python scripts/office.py --from samples/ram-options.json --to xlsx ram.xlsx
python scripts/office.py --from samples/ram-options.json --to docx ram.docx
python scripts/office.py --from samples/ram-options.json --to pptx ram.pptx
```

### One file, every office suite

`.docx`, `.xlsx` and `.pptx` are ZIP-based Open XML. Microsoft Office, Google
Workspace, LibreOffice, OnlyOffice and WPS all read them, and Google Drive
converts them on upload. For a native Google file, upload the Microsoft one and
let Drive convert, or hand over the `.csv` for Sheets.

Charts are SVG — vector, so they stay sharp at any zoom, and they open in a
browser, Word, PowerPoint, LibreOffice and Google Slides. Diagrams are Mermaid
source, rendered by GitHub, GitLab, Obsidian, VS Code and the OpenCode Review
pane, so they stay editable as text instead of becoming a picture.

### Why not use a search API

A key works and is the right answer if you have one — Brave (2,000/month free)
and Tavily (1,000/month) both have free tiers. Without one, this toolkit uses
endpoints that answer plain HTTP: Marginalia, Hacker News (Algolia), Wikipedia,
and direct page fetch. Verified on 2026-11-19: Google required JavaScript,
Bing returned unrelated results, DuckDuckGo served a bot challenge, and no
public SearXNG instance answered. The browser reaches all of them, because a
real browser passes the checks a script cannot.

---

## Second brain

One vault. **Exactly one.**

```
obsidian-vault/
  Daily/            one note per day, one row per agent turn
  Work/             PROJECT_MATRIX.md — the master tracker
  Projects/         one note per project
  Templates/        Daily.md, Project.md
  Dashboards/       saved queries, Grafana links
```

Every agent turn writes **one row**, keyed by `requestId`. Replaying the same request
updates the row instead of appending a duplicate. That single constraint is what keeps
the vault readable after a thousand turns.

### About `graphify` and `demobase`

These are listed in `core/stack.yaml` as **optional index layers, disabled by default**:

- `graphify` — a graph export of wikilinks (Obsidian already draws this natively).
- `demobase` — a sample/vector store for demos.

Neither ships with this template and neither exists on the reference machine. If you
want a semantic layer over the vault, pick **one** and point it at `obsidian-vault/`.
Do not let two tools both write an index into the same vault.

For an index that **does** ship and works offline today, use `data/knowledge.db`
(SQLite + FTS5). It is built from the vault, docs and build facts — no graph engine,
no extra service — and is regenerated by `scripts/build_index.py`.

---

## Knowledge base (pull this first)

`data/` is a self-contained, offline index of the repo plus the verified build
facts. It is committed, so a fresh clone on the desktop has it immediately.

| File | Use |
|---|---|
| `data/build-facts.json` | machine, toolchain, MCP, projects, lessons, pending work |
| `data/knowledge.db` | SQLite + FTS5; any language or DB browser can read it |
| `data/index.json` | structured dump for diffs and non-SQL tools |
| `scripts/build_index.py` | rebuild both after editing docs |
| `scripts/query.py` | search and read from the terminal |

```bash
python scripts/query.py --stats
python scripts/query.py --search "bios ram"
python scripts/query.py --facts machine
python scripts/query.py --facts pending
python scripts/query.py --doc docs/MCP-WIRING.md
```

On the desktop, the same commands work after `git clone`; nothing needs a
network connection or an API key. See `data/README.md` for the schema.

---

## REA loop

```
Plan → Design → Build → Check → Research → Recheck → Build → Fix → Amend
  → Compare → Feedback → Fine-tune → Plan → Build → Discovery → Test
  → Compare → Gather data → Weakness/Gaps → Improve → Next version
```

Each pass ends with a written row in `Daily/` and `Work/PROJECT_MATRIX.md`.
The vault is the memory; the loop is the thing that keeps it honest.

---

## Moving to a Windows 10 desktop

1. **Install prerequisites** on the desktop: Git, Python 3.10+, Node LTS, Ollama.
   ```powershell
   winget install --id Git.Git -e
   winget install --id OpenJS.NodeJS.LTS -e
   winget install --id Ollama.Ollama -e
   ```
2. **Clone, don't copy.** Copying a working tree brings stale locks with it.
   ```powershell
   git clone https://github.com/jayprophit/hive-mind-rea-template.git C:\hive
   cd C:\hive
   ```
3. **Check the machine before changing it.**
   ```powershell
   python scripts\doctor.py
   ```
4. **Apply config.**
   ```powershell
   python scripts\bootstrap.py --apply --scaffold-vault
   ```
5. **Pull one model only** until you know the RAM headroom.
   ```powershell
   ollama pull lfm3:1.7b
   ```
6. **Run the maintenance script** once, elevated, to clear caches and check drivers.
7. **Merge your notes.** Copy only `.md` files from the old vault — never `.obsidian/`
   workspace state, which is per-machine.
8. **Wire Craft Anything to every agent, then prove it works.**
   ```powershell
   .\tools\wire-craft-anything.ps1 -Agent opencode,hermes
   .\tools\agent-preflight.ps1 -StartProvider
   ```
   Do this before the first build. It catches a stopped Ollama, a missing MCP entry,
   or a model that returns empty content — the three causes of a silent 15-minute run.
   Details: `docs/MCP-WIRING.md`.

Windows 10 differences that matter:

- PowerShell 5.1 is the default shell. `scripts/doctor.py` and `bootstrap.py` avoid
  PowerShell-only syntax, so they behave the same there.
- `winget` may need the App Installer update from the Store before it works.
- Windows 10 has no `SetConsoleMode` VT by default in older builds; `doctor.py`
  falls back to plain text automatically.

---

## Troubleshooting

### "The agent stops mid-prompt and never finishes"

Check the provider balance, not the MCP server. In the reference build this was
`AI.Error: Insufficient balance` from the hosted provider — the local stack was fine.
Run `python scripts/doctor.py`; if every local check passes, the failure is upstream.
Point the agent at a local model to confirm:

```bash
opencode --model ollama/lfm3:1.7b
```

### A `rea` MCP server closes immediately

Corrupted `npx` cache — the module graph is incomplete. Symptom:

```
ERR_MODULE_NOT_FOUND: Cannot find module '@jridgewell/trace-mapping'
```

Fix:

```bash
rm -rf ~/AppData/Local/npm-cache/_npx/*   # Windows
rm -rf ~/.npm/_npx/*                      # macOS / Linux
npx -y rea-agents@6.7.0 --version         # verify, then restart Hermes
```

`rea` also needs `REA_PWNTOOLS_PYTHON` set to a Python with `pwntools` installed.

### `pip` fails with `No module named 'pip._vendor...'`

A corrupted pip install. Repair in place:

```bash
python -m ensurepip --upgrade
python -m pip install --user pwntools
```

### Craft Anything says "not installed" but it is

GUI installers do not add themselves to `PATH`. `doctor.py` and `bootstrap.py` probe
the conventional install roots (`C:\Program Files\Craft Anything`,
`/Applications/Craft Anything.app/Contents/MacOS`, `~/.local/bin`) before giving up.

### Hermes: `Failed to load plugin 'obsidian-memory': No __init__.py`

v3 of that plugin is dashboard-only. The loader expects an importable package.
Add a one-line `__init__.py` in the plugin directory, or disable the plugin — the
dashboard mounts from `dashboard/api.py` regardless.

### Craft Anything or Hermes sits for 15 minutes with no output

That is a dead run, not slow work. It has three usual causes, in this order:

1. **The model provider is down.** Hermes' `provider: custom` points at
   `http://127.0.0.1:11434/v1`; if Ollama was stopped to save RAM, every call
   times out three times and Hermes exits `2`.
2. **The model cannot act.** A model with no chat template (e.g. `bonsai-2:4b`,
   `TEMPLATE {{ .Prompt }}`) burns hidden tokens and returns empty content.
   Measured here: 57.7 s and ~200 tokens to answer "OK".
3. **Two runs collide.** Craft Anything retries every ~90 s; a manual
   `hermes -z ...` at the same time produces `Gateway disconnected`.

Run the preflight before the build, and only one builder at a time:

```powershell
.\tools\agent-preflight.ps1 -StartProvider
```

It tests the MCP handshake (38 tools), the OpenCode and Hermes entries, the
provider, and a real model reply. Full diagnosis: `docs/MCP-WIRING.md`.

---

## Verified status

Measured on the reference machine (Windows 11 26200, i3-1005G1, 8 GB, WD SN550 250 GB):

| Check | Result |
|---|---|
| `scripts/doctor.py` | 20 pass, 6 warn, 0 fail |
| `tools/agent-preflight.ps1` | 7/7 PASS (MCP, OpenCode, Hermes, provider, model) |
| Craft Anything MCP handshake | OK — `craft-anything 0.6.0`, **38 tools** over stdio |
| Hermes MCP test | Connected in 3.9 s, 38 tools |
| Hermes model | `lfm3:1.7b`, "OK" in 20.8 s |
| `rea-agents@6.7.0` MCP handshake | OK — `rea 6.7.0` |
| Ollama | 0.40.16, 3 models, listening on :11434 |
| Grafana | responding on :3000 |
| SSD | WD Blue SN550, healthy |
| BIOS | `EMCN60WW` (2024-12-04), updated from `EMCN42WW` |
| `data/knowledge.db` | 105 documents, 488 chunks, 123 facts |

Known warnings on that machine, all expected: 7.7 GB usable RAM, ~21 GB free disk,
Docker daemon stopped, `opencode` CLI not on `PATH`, three Obsidian vault copies.

---

## Requirements

| | Minimum | Recommended |
|---|---|---|
| RAM | 8 GB | 16 GB |
| Disk | 20 GB free | 60 GB free |
| CPU | 2 cores, AVX2 | 4 cores |
| GPU | none (CPU inference) | 6 GB+ VRAM |

At 8 GB, run **one** model at a time (1.5B–4B parameters). Close browsers before
starting an agent session. This is the single biggest performance factor, larger than
any driver update.

---

## Related repos

Part of the same build:

- [`jayprophit/Aetherius-OS`](https://github.com/jayprophit/Aetherius-OS) — AI operating system shell
- [`jayprophit/Agent-Bridge`](https://github.com/jayprophit/Agent-Bridge) — unified agent/tool runtime
- [`jayprophit/craft-anything`](https://github.com/jayprophit/craft-anything) — investigation engine (fork)

---

## Contributing

The most useful contribution is a `doctor.py` run from a platform not in the verified
table. Paste the output in an issue.

---

**Local-first. One vault. Any OS.**
