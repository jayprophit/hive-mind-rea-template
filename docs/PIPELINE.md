# Hive Mind REA Pipeline - Full Suite Configuration
Updated: 2026-11-11

## Architecture: Everything Connected

```
┌─────────────────────────────────────────────────────────────────────┐
│                        HIVE MIND REA PIPELINE                       │
│                                                                     │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐      │
│  │ Obsidian │◄──►│  Grafana  │◄──►│ Prometheus│◄──►│  Loki    │      │
│  │  Vault   │    │ :3000     │    │ :9090     │    │ :3100    │      │
│  │ (2nd     │    │ /d/work-  │    │ (Ollama   │    │ (Daily/  │      │
│  │  brain)  │    │  matrix   │    │  metrics) │    │  logs)   │      │
│  └────┬─────┘    └──────────┘    └──────────┘    └──────────┘      │
│       │                                                              │
│       ▼                                                              │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │              HERMES SUPERVISOR (bonsai-2:4b)                  │    │
│  │  Routes via laya /v1/systemone → delegates to workers         │    │
│  │  Terminal: local | Browser: auto_local | Memory: enabled      │    │
│  └──────────────────────┬───────────────────────────────────────┘    │
│                         │                                          │
│         ┌───────────────┼───────────────┐                           │
│         ▼               ▼               ▼                           │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐                    │
│  │ @coder     │  │ @windows   │  │ @decider   │                    │
│  │ lfm3:1.7b  │  │ OpenClaw   │  │ laya       │                    │
│  │ (OpenCode  │  │ Node       │  │ /v1/       │                    │
│  │  subagent) │  │ (files,    │  │ systemone  │                    │
│  │            │  │  Office,   │  │ (routing)  │                    │
│  │            │  │  browser)  │  │            │                    │
│  └────────────┘  └────────────┘  └────────────┘                    │
│         │               │               │                           │
│         ▼               ▼               ▼                           │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │                    REVERSE ENGINEERING STACK                  │    │
│  │  Craft Anything (MCP, 30 tools) │ Ghidra │ JADX │ Rizin     │    │
│  │  mitmproxy │ Frida │ tshark │ GDB │ objdump (WSL)           │    │
│  │  faster-whisper │ ffmpeg │ yt-dlp                            │    │
│  └──────────────────────────────────────────────────────────────┘    │
│         │                                                          │
│         ▼                                                          │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │                    CLOUD ESCALATION (free, daily reset)       │    │
│  │  @beam │ @crouton-alpha │ @deepseek-v41-flash │ @flint-40b  │    │
│  │  @glm-53-flash │ @iceman │ @inkling-2-small │ @longcat-2-5  │    │
│  │  @mimo-v26-flash │ @nemotron-35-lightning │ @nemotron-35-super-vl│    │
│  └──────────────────────────────────────────────────────────────┘    │
│         │                                                          │
│         ▼                                                          │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │                    SUPPORTING SERVICES                        │    │
│  │  LM Studio :1234 (spare engine) │ Bionic (cloud reviewer)     │    │
│  │  Docker :2375 (containers) │ OpenClaw :18789 (gateway)       │    │
│  │  Ollama :11434 (primary LLM engine)                          │    │
│  └──────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────┘
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

A "second brain" is a personal knowledge management (PKM) system — a digital repository for capturing, organizing, and retrieving information. Popularized by Tiago Forte's "Building a Second Brain" (BASB) methodology.

**You already have one.** Your Obsidian vault at `C:\Users\jpowe\Documents\ObsidianVault\` IS your second brain:

| BASB Concept | Your Implementation |
|---|---|
| **Capture** | Daily notes, agent vocabulary, project rows |
| **Organize** | Daily/, Work/, Projects/, Dashboards/, Templates/ |
| **Distill** | Agent_Vocabulary.md, Agent_Vocabulary_GrokBot.md |
| **Express** | Grafana dashboards, PROJECT_MATRIX.md, Daily logs |
| **PARA** (Projects/Areas/Resources/Archives) | Work/ (projects), Daily/ (areas), Agent_Vocabulary (resources), git history (archives) |

## Component Status (all connected)

### Core (always running)
| Component | Port | Status | Role |
|---|---|---|---|
| Ollama | 11434 | ✅ Running | Primary LLM engine (bonsai-2:4b, lfm3:1.7b, laya) |
| Hermes | CLI | ✅ Configured | Supervisor (routes via laya /v1/systemone) |
| OpenClaw Gateway | 18789 | ✅ Running | Windows automation (files, Office, browser, canvas) |
| Grafana | 3000 | ✅ Running | Dashboards (/d/work-matrix), metrics, logs |
| Obsidian | Vault | ✅ Created | Second brain (Daily, Work, Projects, Templates) |

### Supporting (on-demand)
| Component | Port | Status | Role |
|---|---|---|---|
| LM Studio | 1234 | ⚠️ Server not started | Spare LLM engine (run ONE at a time) |
| Bionic | N/A | ⚠️ Needs endpoint config | Cloud reviewer (point to Ollama :11434) |
| Docker Desktop | 2375 | ✅ Running (7 containers) | Container runtime (selective services) |
| OpenCode | CLI | ✅ Configured | Subagent delegation (22 agents) |

### Reverse Engineering Stack
| Tool | Status | Purpose |
|---|---|---|
| Craft Anything | ✅ MCP connected to 9 agents | Investigation, triage, reports, rebuild |
| Ghidra 11.4.2 | ✅ Installed | Deep binary decompilation |
| JADX 1.5.3 | ✅ Installed | Android APK → Java source |
| Rizin 0.9.1 | ✅ Installed | CLI disassembly, binary analysis |
| mitmproxy 12.3.1 | ✅ Installed | HTTPS traffic interception |
| Frida 17.26.2 | ✅ Installed | Runtime hooking/tracing |
| tshark 4.2.2 | ✅ Installed (WSL) | Packet capture, protocol analysis |
| GDB 15.1 | ✅ Installed (WSL) | Linux binary debugging |
| objdump 2.42 | ✅ Installed (WSL) | ELF disassembly |
| faster-whisper | ✅ Installed | Speech-to-text |
| ffmpeg | ✅ Installed | Media processing |
| yt-dlp | ✅ Installed | Media download |

### MCP Servers (configured in opencode-mcp.example.json)
| Server | Status | Purpose |
|---|---|---|
| Playwright | ✅ Configured | Browser automation (Microsoft) |
| Chrome DevTools | ✅ Configured | Browser debugging |
| Perplexity | ⚠️ Needs API key | AI search |
| Firecrawl | ⚠️ Needs API key | Web scraping |
| Apify | ⚠️ Needs API key | Web scraping actors |
| Craft Anything | ✅ Connected (9 agents) | Reverse engineering (30 tools) |
| Filesystem | ✅ Configured | File operations |
| Memory | ✅ Configured | Knowledge graph |
| Git | ✅ Configured | Repository operations |
| Fetch | ✅ Configured | Web content fetching |

### Docker Services (docker-compose.services.yml)
| Service | Status | Port | Purpose |
|---|---|---|---|
| OpenProject | ⚠️ Stub (not started) | 8080 | Project management |
| Chatwoot | ⚠️ Stub (not started) | 3001 | Customer support |
| LiveKit | ⚠️ Stub (not started) | 7880 | Real-time media |

### Cloned Repos (hive-mind-rea-template/repos/)
| Repo | Status | Purpose |
|---|---|---|
| livekit | ✅ Cloned | Real-time communication |
| chatwoot | ✅ Cloned | Customer support platform |
| weknora | ✅ Cloned | Knowledge/RAG platform |
| cap | ✅ Cloned | Screen recording |
| cal.com | ✅ Cloned | Scheduling |
| openproject | ✅ Cloned | Project management |

## Quick Reference: How to use everything

### Start the full pipeline
```powershell
# 1. Ollama (should already be running)
ollama serve  # if not running

# 2. OpenClaw Gateway (should already be running)
# ws://127.0.0.1:18789

# 3. Grafana (should already be running)
# http://127.0.0.1:3000/d/work-matrix

# 4. Hermes supervisor
$env:HERMES_HOME="C:\Users\jpowe\AppData\Local\hermes"
python -m hermes_cli.main -p supervisor --model ollama/bonsai-2:4b chat

# 5. OpenCode (alternative interface)
opencode --model ollama/bonsai-2:4b
```

### Delegate to workers
```
@coder Fix auth.ts, run npm test
@windows Open Excel and check cell B2
@decider Score risk for deploying v2.0
@researcher Find latest SWE-bench results
@reviewer Review the coder's diff
@beam Design architecture for new feature
```

### Reverse engineer
```
craft-anything-cli triage target.exe
craft-anything-cli report --html
mitmdump  # intercept HTTPS
frida-trace -p <PID> -i "open*"
wsl -d Ubuntu sudo tshark -i any -w capture.pcap
```

### Track progress
- Obsidian: `C:\Users\jpowe\Documents\ObsidianVault\` (open as vault)
- Grafana: `http://127.0.0.1:3000/d/work-matrix`
- Daily log: `Daily/YYYY-MM-DD.md`
- Project matrix: `Work/PROJECT_MATRIX.md`

## 2nd Brain Summary

**You already have a second brain.** Your Obsidian vault at `C:\Users\jpowe\Documents\ObsidianVault\` is a fully functional second brain following Tiago Forte's BASB methodology:

1. **Capture**: Daily notes, agent vocabulary, project rows, tool manifests
2. **Organize**: Daily/, Work/, Projects/, Dashboards/, Templates/, mcp/, docker/, docs/, tools/, repos/
3. **Distill**: Agent_Vocabulary.md, Agent_Vocabulary_GrokBot.md, INTEGRATIONS.md
4. **Express**: Grafana dashboards, PROJECT_MATRIX.md, Daily logs, git commits

**Is it useful?** Yes — it's the backbone of your entire system. Every agent reads/writes to it. Grafana scrapes it for live metrics. The REA loop depends on it for tracking progress. Without it, you'd lose context between sessions.

**What makes yours special:** It's not just notes — it's a living database that your AI team reads and writes to automatically. Every turn adds a row. requestId dedup prevents duplicates. The Grafana dashboard turns it into a live monitoring system.