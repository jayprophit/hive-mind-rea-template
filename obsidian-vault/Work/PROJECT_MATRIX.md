---
type: matrix
project: "Master Project Tracker"
supervisor: "bonsai-2:4b"
router: "laya"
coder: "lfm3:1.7b"
grafana: "http://127.0.0.1:3000/d/work-matrix"
vault: "ObsidianVault"
started: 2026-11-06
status: active
---

# Master Project Tracker — Hive Mind

*This file is the spine. Every agent reads/writes it. Grafana scrapes Pros + Daily notes to build the live matrix. Nothing is duplicated: requestId is the primary key.*

## Lifecycle (human loop, revived by AI each turn)

```
Plan → Design → Build → Check → Research → Recheck → Build → Fix → Amend → Compare
 → Feedback → Fine-tune → Plan → Build → Discovery → Test → Compare
 → Gather data → Weakness/Gaps → Improve → Next version
```

| Phase | What happens | Agent | Model |
|-------|--------------|-------|-------|
| Plan | supervisor scopes task, asks laya `/v1/systemone` | @supervisor | bonsai-2:4b |
| Design | architect drafts, Beam/Crouton/DeepSeek/LongCat/Mimo to compare | @beam/@crouton-alpha/@deepseek-v41-flash/@longcat-2-5/@mimo-v26-flash | nous cloud free |
| Build | coder implements, windows opens apps | @coder (lfm3:1.7b) + @windows (OpenClaw) | ollama local |
| Check | reviewer QA, decider scores risk | @reviewer + laya | ollama |
| Research | researcher websearch/webfetch, designer canvas/vision | @researcher + @designer | bonsai-2:4b vision |
| Recheck | @reviewer re-reads diff, decider re-scores | @reviewer/@qa | bonsai-2:4b |
| Build | coder patch, windows verify in Office/browser | @coder/@windows | local |
| Fix | coder fixes, windows re-opens app | @coder | lfm3 |
| Amend | supervisor rewrites plan, bumps version in frontmatter | @supervisor | bonsai-2:4b |
| Compare | Beam/DeepSeek/LongCat/Mimo score vs prior | @beam/@deepseek-v41-flash | cloud |
| Feedback | marketer/hr/finance score receipt | @finance/@hr/@marketer | laya routing |
| Fine-tune | supervisor compresses, updates SOUL.md | @supervisor | local |
| Discovery | @researcher + @windows screen.snapshot | @researcher | local |
| Test | @qa shell `npm test`, @coder re-run | @qa | local |
| Gather data | Grafana pulls Prometheus + Obsidian frontmatter | Grafana |  |
| Weakness/Gaps | doctor gaps section, `openclaw doctor`, `hermes doctor` | @supervisor | local |
| Improve | next version row below, no duplicate requestId | @supervisor | local |

## Project rows (Grafana ingest key)

| requestId | date | project | phase | agent | model | tokens | cost | risk | status |
|-----------|------|---------|-------|-------|-------|--------|------|------|--------|
| baloon-2026-11-06 | 2026-11-06 | baloon | plan | supervisor | bonsai-2:4b | 0 | 0.00 | 0.2 | done |
| hermes-fix-2026-11-06 | 2026-11-06 | hermes-fix | build | coder | lfm3:1.7b | 0 | 0.00 | 0.3 | done |
| lmstudio-first-run | 2026-11-07 | lmstudio | build | windows | bonsai-2:4b | 0 | 0.00 | 0.1 | done |
| grafana-obsidian | 2026-11-07 | grafana-obsidian | build | supervisor | bonsai-2:4b | 0 | 0.00 | 0.15 | done |
| migration-2026-11-06 | 2026-11-06 | disk-cleanup | check | supervisor | bonsai-2:4b | 0 | 0.00 | 0.1 | done |

## Agent roster

| Agent | Profile | Model | Caps |
|-------|---------|-------|------|
| @supervisor | ~/.hermes/profiles/supervisor | ollama/bonsai-2:4b | full local (terminal/browser/computer-use) |
| @coder | ~/.hermes/profiles/coder + opencode coder.md | ollama/lfm3:1.7b | edit, shell |
| @decider | ~/.hermes/profiles/decider | ollama/laya | decision only |
| @windows | ~/.hermes/profiles/windows + OpenClaw Node | ollama/bonsai-2:4b | Office, files, browser, canvas |
| @beam | ~/.hermes/profiles/beam | nous/beam | cloud reasoning |
| @crouton-alpha | ~/.hermes/profiles/crouton-alpha | nous/crouton-alpha | general |
| @deepseek-v41-flash | ~/.hermes/profiles/deepseek-v41-flash | nous/deepseek-v4.1-flash | CTO |
| @flint-40b | ~/.hermes/profiles/flint-40b | nous/flint-40b | Lead dev |
| @glm-53-flash | ~/.hermes/profiles/glm-53-flash | nous/glm-5.3-flash | fast coding |
| @iceman | ~/.hermes/profiles/iceman | nous/iceman | design |
| @inkling-2-small | ~/.hermes/profiles/inkling-2-small | nous/inkling-2-small | fast vision |
| @longcat-2-5 | ~/.hermes/profiles/longcat-2-5 | nous/longcat-2.5 | research |
| @mimo-v26-flash | ~/.hermes/profiles/mimo-v26-flash | nous/mimo-v2.6-flash | vision+coding |
| @nemotron-35-lightning | ~/.hermes/profiles/nemotron-35-lightning | nous/nemotron-3.5-lightning | edge assistant |
| @nemotron-35-super-vl | ~/.hermes/profiles/nemotron-35-super-vl | nous/nemotron-3.5-super-vl | vision master |

## Grafana

Dashboard: http://127.0.0.1:3000/d/work-matrix
Datasource: Prometheus http://127.0.0.1:9090 scrapes Ollama `/metrics` + Loki tails `Daily/` + `Work/Project.md` frontmatter.
Every turn writes one row here. requestId dedup = no duplicate work.

## Obsidian

Vault: C:\Users\jpowe\Documents\ObsidianVault
- Daily/2026-11-09.md = today
- Work/Project.md = project matrix (above)
- This MATRIX.md = master spine

Open: Obsidian > File > Open folder as vault > C:\Users\jpowe\Documents\ObsidianVault
