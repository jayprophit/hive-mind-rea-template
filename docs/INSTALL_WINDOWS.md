# Hive Mind REA Template - Windows 10/11 Install Notes
Updated: 2026-11-10 (i3-1005G1, 7.75GB RAM)

## Core (already in this setup)
- Ollama: `winget install Ollama.Ollama` or installer; `ollama pull bonsai-2:4b lfm3:1.7b laya`
- Hermes: install Hermes Agent/Desktop; set `HERMES_HOME=%LOCALAPPDATA%\hermes`; copy `hermes/config.yaml` and `hermes/profiles/*`
- OpenCode: copy `opencode/agents/*.md` to `~/.config/opencode/agents/`
- Docker Desktop (WSL2): enable WSL, install Docker Desktop; engine 29.x verified. Start UI via `Docker Desktop.exe`
- Grafana: service on :3000; copy `grafana/provisioning/*` to Grafana conf/provisioning (Admin) and restart service
- Obsidian: open `obsidian-vault/` as vault

## MCP servers (configure in OpenCode/Claude/Hermes MCP config)
Use `mcp/opencode-mcp.example.json` as template. Most run via `npx -y <pkg>` (Node 18+).
- **Playwright MCP**: `npx -y @playwright/mcp@latest` (Microsoft)
- **Chrome DevTools MCP**: `npx -y chrome-devtools-mcp@latest` (or package per your client)
- **Perplexity MCP**: `npx -y server-perplexity-ask` + `PERPLEXITY_API_KEY`
- **Firecrawl MCP**: `npx -y firecrawl-mcp` + `FIRECRAWL_API_KEY`
- **Apify MCP**: `npx -y @apify/actors-mcp-server` + `APIFY_TOKEN`
- **Reference MCP servers**: `@modelcontextprotocol/server-memory`, `@modelcontextprotocol/server-filesystem`, `uvx mcp-server-git`, `uvx mcp-server-fetch`
- **VidIQ / Skool / Higgsfield MCPs**: require vendor API keys or community packages - add endpoints/keys in `.env` once obtained

## Media / creator CLI (lightweight first)
- **FFmpeg**: `winget install Gyan.FFmpeg` (or `choco install ffmpeg`) - verify `ffmpeg -version`
- **yt-dlp**: `python -m pip install -U yt-dlp` or `winget install yt-dlp.yt-dlp`
- **Whisper**: prefer `pip install faster-whisper` (lighter) or `openai-whisper` (heavier, needs torch). On 7.75GB RAM use small/base models only.
- **Remotion**: `npx create-video@latest` in a project folder (Node 18+); render costs CPU/RAM
- **LiveKit**: `docker run --rm -p 7880:7880 -p 7881:7881 -p 7882:7882/udp livekit/livekit-server --dev` or see `docker/docker-compose.services.yml`; SDKs via npm/pip

## APIs (keys/OAuth required - do not commit)
- **YouTube Analytics API**: Google Cloud project, enable YouTube Analytics/Data APIs, OAuth consent/credentials
- **Instagram API**: Meta Developer app, Instagram Graph API permissions/tokens
- Store in local `.env` or OS credential store

## Repos / apps requested (clone/configure selectively)
- **OpenProject / Chatwoot / Cal.com**: self-host via Docker compose (see `docker/docker-compose.services.yml`) - heavy for 7.75GB RAM, run one at a time
- **Weknora, OpenWhispr, Cap, Open Higgsfield, VoiceStudio, OpenSEO, BaseMode**: identify official repos/releases and clone under `repos/` or install binaries; document in `docs/INTEGRATIONS.md`
- **aireceptionist, J.A.R.V.I.S, Grok bot clone, Scion, Mononoke**: clone exact GitHub repos once URLs confirmed (ambiguous names - verify before cloning)
- **claude x jev skill**: obtain skill package/source and place in Hermes/OpenCode skills path

## Performance tips (this machine)
- Run **one** LLM server at a time (Ollama preferred). Keep Docker services minimal.
- Prefer `--disable-gpu` for Electron apps on Intel UHD if renderer crashes.
- `OLLAMA_KEEP_ALIVE=10m`; avoid loading >2GB models simultaneously.
