# Hive Mind REA Template — Local AI Suite for Windows 10/11
### Crouton Alpha deployment — local-first Hive Mind (Hermes + Ollama + OpenClaw + OpenCode + LM Studio + Grafana + Obsidian)

> **GitHub:** https://github.com/jayprophit/hive-mind-rea-template (public, starred)
> **Clone:** `git clone https://github.com/jayprophit/hive-mind-rea-template.git`

---

## What This Is

A complete, local-first AI development suite that runs on a low-spec Windows machine (i3-1005G1, 7.75GB RAM, Intel UHD 1GB). Everything is configured to work together — no cloud keys needed for local operation. Includes a 12-bot AI team, reverse engineering stack, Grafana dashboards, Obsidian second brain, and REA (Revived by AI) loop methodology.

---

## Stack

### Core AI (always running)
| Component | Port | Model/Version | Role |
|---|---|---|---|
| **Ollama** | 11434 | bonsai-2:4b (1.6GB), lfm3:1.7b (1.1GB), laya (844MB) | Primary LLM engine |
| **Hermes** | CLI | bonsai-2:4b (supervisor) | AI supervisor — routes via laya /v1/systemone, delegates to workers |
| **OpenClaw Gateway** | 18789 | ollama/bonsai-2:4b | Windows automation (files, Office, browser, canvas, screen) |
| **OpenCode** | CLI | 22 agents | Subagent delegation (coder, decider, windows, designer, etc.) |
| **Grafana** | 3000 | 13.3.0 | Dashboards (/d/adw9qkn/...), metrics, logs |
| **Obsidian** | Vault | Second brain | Knowledge base (Daily, Work, Projects, Templates) |

### Supporting (on-demand)
| Component | Port | Status | Role |
|---|---|---|---|
| **LM Studio** | 1234 | Server running (gemma-4-e4b) | Spare LLM engine (run ONE at a time) |
| **Bionic** | N/A | Configured (Ollama endpoint) | Cloud reviewer |
| **Docker Desktop** | 2375 | Backend running | Container runtime (selective services) |

### Reverse Engineering Stack
| Tool | Version | Purpose |
|---|---|---|
| **Craft Anything** | Latest (30 MCP tools) | Investigation, triage, reports, rebuild studies. MCP connected to 9 agents. |
| **Ghidra** | 11.4.2 | Deep binary decompilation (C pseudocode from exe/dll/so/firmware) |
| **JADX** | 1.5.3 | Android APK → Java source code |
| **Rizin** | 0.9.1 | CLI disassembler, binary analysis, strings, structure |
| **Java (Temurin)** | 21.0.13 | Runtime for Ghidra/JADX |
| **mitmproxy** | 12.3.1 | HTTPS traffic interception, API reverse-engineering |
| **Frida** | 17.26.2 | Runtime function tracing, hooking, dynamic analysis |
| **tshark** | 4.2.2 (WSL) | Packet capture, 1000+ protocols |
| **GDB** | 15.1 (WSL) | Linux binary debugging |
| **objdump** | 2.42 (WSL) | ELF disassembly |
| **faster-whisper** | Latest | Speech-to-text |
| **ffmpeg** | Gyan.FFmpeg | Media processing, format conversion |
| **yt-dlp** | 2026.10.26 | Media download from URLs |

### Cloud Escalation (free, daily reset)
11 Nous Portal models: beam, crouton-alpha, deepseek-v4.1-flash, flint-40b, glm-5.3-flash, iceman, inkling-2-small, longcat-2.5, mimo-v2.6-flash, nemotron-3.5-lightning, nemotron-3.5-super-vl

### MCP Servers (configured in mcp/opencode-mcp.example.json)
Playwright, Chrome DevTools, Perplexity, Firecrawl, Apify, Craft Anything, Filesystem, Memory, Git, Fetch

### Docker Services (docker/docker-compose.services.yml)
OpenProject (8080), Chatwoot (3001), LiveKit (7880) — stubs, start selectively

### Cloned Repos (repos/, gitignored)
livekit, chatwoot, weknora, cap, cal.com, openproject

---

## Quick Start (Windows 11/10)

### 1. Install core tools
```powershell
# Ollama
winget install Ollama.Ollama
ollama pull bonsai-2:4b
ollama pull lfm3:1.7b
ollama pull laya

# Hermes (install from https://hermes-agent.nousresearch.com/)
# Set HERMES_HOME = %LOCALAPPDATA%\hermes
# Copy hermes/config.yaml and hermes/profiles/* to %LOCALAPPDATA%\hermes\

# OpenCode
# Copy opencode/agents/*.md to ~/.config/opencode/agents/

# Grafana
# Service on :3000, copy grafana/provisioning/* to Grafana conf/provisioning (Admin)
```

### 2. Run the full pipeline
```powershell
# Start services (most should already be running)
ollama serve                    # :11434
# OpenClaw Gateway already on :18789
# Grafana already on :3000

# Hermes supervisor
$env:HERMES_HOME="C:\Users\jpowe\AppData\Local\hermes"
python -m hermes_cli.main -p supervisor --model ollama/bonsai-2:4b chat

# OpenCode (alternative)
opencode --model ollama/bonsai-2:4b
```

### 3. Delegate to workers
```
@coder Fix auth.ts, run npm test
@windows Open Excel and check cell B2
@decider Score risk for deploying v2.0
@researcher Find latest SWE-bench results
@reviewer Review the coder's diff
@beam Design architecture for new feature
```

### 4. Track progress
- Obsidian: Open `obsidian-vault/` as vault
- Grafana: http://127.0.0.1:3000/d/adw9qkn/work-tracking-matrix-e28094-hive-mind
- Daily log: `obsidian-vault/Daily/YYYY-MM-DD.md`
- Project matrix: `obsidian-vault/Work/PROJECT_MATRIX.md`

### 5. Reverse engineer
```powershell
craft-anything-cli triage target.exe
craft-anything-cli report --html
mitmdump  # intercept HTTPS
frida-trace -p <PID> -i "open*"
wsl -d Ubuntu sudo tshark -i any -w capture.pcap
```

### 6. Install script (automated)
```powershell
powershell -ExecutionPolicy Bypass -File tools/install_windows.ps1 -InstallCLI -CloneRepos -ShowVersions
```

---

## Repo Layout
```
hermes/                 Hermes Bot profiles (23: 12 roles + 11 cloud specialists)
grafana/provisioning/   datasources.yaml + dashboards/work-matrix.json + dashboards.yaml
obsidian-vault/         Daily/Work/Project.md + PROJECT_MATRIX.md (requestId dedup, Grafana ingest)
mcp/                    OpenCode MCP config template (10 servers)
docker/                 Docker Compose service stubs (OpenProject, Chatwoot, LiveKit)
docs/                   INTEGRATIONS.md, INSTALL_WINDOWS.md, PIPELINE.md
tools/                  install_windows.ps1 (CLI tools, repo cloning, version checks)
opencode/               OpenCode agent .md files (22 agents)
repos/                  Cloned repos (gitignored: livekit, chatwoot, weknora, cap, cal.com, openproject)
```

## REA Loop (Revived by AI each turn)
```
Plan → Design → Build → Check → Research → Recheck → Build → Fix → Amend → Compare
  → Feedback → Fine-tune → Plan → Build → Discovery → Test → Compare
  → Gather data → Weakness/Gaps → Improve → Next version
```

Every turn writes ONE row to Obsidian Daily + PROJECT_MATRIX.md with requestId dedup.
Grafana scrapes Prometheus (Ollama metrics) + Loki (log tails) + Obsidian frontmatter.

## 2nd Brain (Obsidian Vault)

A "second brain" is a personal knowledge management (PKM) system — a digital repository for capturing, organizing, and retrieving information (Tiago Forte's BASB methodology).

**This repo's Obsidian vault IS the second brain:**
- **Capture:** Daily notes, agent vocabulary, project rows, tool manifests
- **Organize:** Daily/, Work/, Projects/, Dashboards/, Templates/, mcp/, docker/, docs/, tools/, repos/
- **Distill:** Agent_Vocabulary.md, Agent_Vocabulary_GrokBot.md, INTEGRATIONS.md
- **Express:** Grafana dashboards, PROJECT_MATRIX.md, Daily logs, git commits

## Full Suite Documentation
- `docs/PIPELINE.md` — Complete architecture diagram, component status, quick reference, 2nd brain explanation
- `docs/INTEGRATIONS.md` — All integrations with status, install notes, API key requirements
- `docs/INSTALL_WINDOWS.md` — Windows 10/11 install guide with performance tips
- `obsidian-vault/Work/PROJECT_MATRIX.md` — Master project tracker with REA loop

## Top Models for This Machine (i3-1005G1, 7.75GB, UHD 1GB)
- **Top 1:** `bonsai-2:4b` — 1.6GB ternary, vision+tools+thinking 256K, 8-12 tok/s
- **Top 5:** bonsai-2:4b, lfm3:1.7b, laya, d3:2b (3.1GB decision), qwen2.5-coder:1.5b
- **Top 10:** adds qwen3:0.6b, gemma3:1b, qwen3:1.7b, qwen3:4b, OLMoE 7B int8 (22 tok/s CPU)
- **Image/video gen:** impossible locally (FLUX 14.6GB, Wan 21GB) — use cloud FAL.ai via Hermes `image.generate`

## Not Installed (optional)
| Tool | Why skip | Install when |
|---|---|---|
| tshark/Wireshark | Network packets (covered by mitmproxy) | Deep packet forensics |
| LLDB | Apple/macOS debugging | Only if developing for Apple (needs Mac + license) |
| GDB/objdump (Windows) | Covered by Rizin/Ghidra | Specific debugging tasks (available in Ubuntu WSL) |

---

Crouoton Alpha deployment. No cloud keys needed for local operation. Built to 100%+.

**GitHub:** https://github.com/jayprophit/hive-mind-rea-template (public, starred)