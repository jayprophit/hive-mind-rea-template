# Integration & Tooling Manifest (Hive Mind REA Template)
Updated: 2026-11-10

This file tracks requested integrations. On this i3-1005G1/7.75GB RAM Windows host, prefer lightweight CLI/MCP configs and Dockerized services only when needed. Many items require API keys, accounts, or separate services - configure via .env / secrets, never commit keys.

## Status legend
- **configured**: config/template added in repo
- **installed**: binary/package present locally
- **cloned**: source repo cloned under repos/
- **blocked/needs-key**: requires API key, account, admin, or heavy deps
- **pending**: not yet installed

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

