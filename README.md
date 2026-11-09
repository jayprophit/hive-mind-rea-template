# HIVE MIND - Local REA Template for Windows 11/10
# Crouton Alpha deployment - local-first Hive Mind (Hermes + Ollama + OpenClaw + OpenCode + LM Studio + Grafana + Obsidian)

## Stack
- Hermes Supervisor (bonsai-2:4b local) - full computer-use, terminal, browser
- Ollama worker models: bonsai-2:4b 1.6GB, lfm3:1.7b 1.1GB, laya 844MB
- LM Studio spare engine (1234), Bionic cloud reviewer
- OpenClaw Gateway (18789), Grafana (3000), Obsidian vault (this repo)

## Quick start Win11/Win10
1. Install Ollama .\install\OllamaSetup.exe, then ollama pull bonsai-2:4b lfm3:1.7b laya
2. Install Hermes via installer, then copy hermes/config.yaml -> %LOCALAPPDATA%\hermes\config.yaml
3. Install OpenCode, OpenClaw Gateway, LM Studio, Grafana - see docs/setup.md
4. Open Obsidian vault: obsidian-vault/ as vault folder
5. Run: python -m hermes_cli.main -p supervisor --model ollama/bonsai-2:4b chat

## Repo layout
hermes/                 Hermes Bot profiles (supervisor,coder,decider,windows,designer,finance,hr,marketer,qa,researcher,reviewer,writer + cloud specialists)
grafana/provisioning/   datasources.yaml + dashboards/work-matrix.json + dashboards.yaml
obsidian-vault/         Daily/Work/Project.md + PROJECT_MATRIX.md (requestId dedup, Grafana ingest)
docs/                   Setup scripts, gap analysis, model matrix

See PROJECT_MATRIX.md for full loop: Plan → Design → Build → Check → Research → ... → Improve → Next version

Crouoton Alpha deployment. No cloud keys needed for local operation.
