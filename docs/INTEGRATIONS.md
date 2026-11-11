# Integration & Tooling Manifest (Hive Mind REA Template)
Updated: 2026-11-10

This file tracks requested integrations. On this i3-1005G1/7.75GB RAM Windows host, prefer lightweight CLI/MCP configs and Dockerized services only when needed. Many items require API keys, accounts, or separate services - configure via .env / secrets, never commit keys.

## Status legend
- **configured**: config/template added in repo
- **installed**: binary/package present locally
- **cloned**: source repo cloned under repos/
- **blocked/needs-key**: requires API key, account, admin, or heavy deps
- **pending**: not yet installed

## Reverse Engineering Stack (complete - 2026-11-11)
| Tool | Version | Location | Purpose |
|---|---|---|---|
| Craft Anything | Latest (30 MCP tools) | C:\Program Files\Craft Anything\ | Investigation, triage, reports, rebuild studies. MCP connected to 9 agents. |
| Ghidra | 11.4.2 | C:\Tools\Ghidra\ | Deep binary decompilation (C-like pseudocode from exe/dll/so/firmware) |
| JADX | 1.5.3 | C:\Tools\JADX\ | Android APK decompilation to Java source |
| Rizin | 0.9.1 | C:\Tools\Rizin\ | CLI disassembler, binary analysis, strings, structure |
| Java (Temurin) | 21.0.13 | C:\Program Files\Eclipse Adoptium\ | Runtime for Ghidra/JADX |
| mitmproxy | 12.3.1 | C:\Program Files\mitmproxy\ | HTTPS traffic interception, API reverse-engineering |
| Frida | 17.26.2 + tools 14.13.1 | codex-runtimes/python/Scripts/ | Runtime function tracing, hooking, dynamic analysis |
| faster-whisper | Latest | pip | Speech-to-text for audio analysis |
| ffmpeg | Gyan.FFmpeg | winget | Media processing, format conversion |
| yt-dlp | 2026.10.26 | pip | Media download from URLs |

### Not installed (optional, niche)
| Tool | Why skip | Install when |
|---|---|---|
| GDB | Debugging compiled code (Linux focus) | Specific debugging tasks (Rizin/Ghidra cover analysis) |
| objdump | Disassembly (covered by Rizin) | Quick one-off disassembly |
| tshark/Wireshark | Network packet analysis (covered by mitmproxy) | Deep packet forensics |
| LLDB | Apple/macOS debugging | Only if developing for Apple (user has iPad Pro 1 but builds on Windows; Apple dev needs Mac + license) |

### Environment variables set
- JAVA_HOME = C:\Program Files\Eclipse Adoptium\jdk-21.0.13.9-hotspot
- PATH includes: Java bin, Ghidra, JADX bin, Rizin bin, Frida scripts

### How they work together in the pipeline
```
Craft Anything (MCP) ── investigation, triage, reports, rebuild studies
       │
       ├── Ghidra ── deep binary decompilation (C pseudocode)
       ├── JADX ── Android APK → Java source
       ├── Rizin ── CLI disassembly, strings, structure analysis
       ├── mitmproxy ── intercept HTTPS traffic from target apps
       ├── Frida ── hook/trace running processes dynamically
       ├── faster-whisper ── transcribe audio from media
       ├── ffmpeg ── process/convert media files
       └── yt-dlp ── download media from URLs for analysis
```

| Item | Type | Status | Notes / Install |
|---|---|---|---|
| scion | TBD | pending | needs identification (SCION network? other) |
| mononoke | source control (Meta) | pending | heavy Rust build; Linux-oriented; likely not feasible locally |
| perplexity mcp | MCP | configured | needs PERPLEXITY_API_KEY; npx-based server |
| playwright mcp | MCP | configured | `npx @playwright/mcp@latest` |
| firecrawl mcp | MCP | configured | needs FIRECRAWL_API_KEY |
| higgsfield mcp | MCP/AI media | pending | needs Higgsfield API/key identification |
| fifth - chrome devtools mcp | MCP | configured | Chrome DevTools MCP (community/fifth) |
| open higgsfield | app/repo | pending | needs repo URL identification |
| voicestudio | app | pending | needs identification |
| openseo | SEO tool | pending | needs identification |
| weknora | RAG/knowledge | pending | clone & configure if repo found |
| openwhispr | speech-to-text | pending | local Whisper UI/alternative |
| openproject | PM (Docker) | pending | docker compose; needs RAM |
| cal.com | scheduling | pending | SaaS or self-host Docker |
| chatwoot | support (Docker) | pending | docker compose; needs RAM |
| cap | screen recording | pending | Cap.so app/repo |
| basemode | TBD | pending | needs identification |
| apify mcp | MCP | configured | needs APIFY_TOKEN |
| vidiq mcp | MCP | configured | needs VidIQ API access |
| calude x jev skill | skill | pending | needs source/packaging |
| yt-dlp | CLI media | pending | `pip install -U yt-dlp` or winget |
| whisper | STT | pending | openai-whisper (heavy) or whisper.cpp/faster-whisper |
| ffmpeg | media | pending | winget/choco/scoop |
| remotion | video (React) | pending | npm project scaffold |
| youtube analytics api | API | needs-key | Google Cloud project + OAuth/API key |
| instagram api | API | needs-key | Meta app + permissions |
| skool mcp | MCP | pending | community MCP if exists; needs auth |
| aireceptionist | GitHub repo | cloned/pending | clone target |
| j.a.v.i.s / JARVIS | GitHub repo | cloned/pending | clone target (specify exact repo) |
| grok bot clone repo | GitHub repo | cloned/pending | clone target (specify exact repo) |
| livekit | realtime media | pending | LiveKit server/SDK; docker or cloud |
| craft-anything | investigation/reverse-engineering | installed | MCP server (30 tools), connected to 9 agents, skill in 3 locations, Chromium engine OK |

