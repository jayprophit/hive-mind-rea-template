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

## Active work - 2026-11-19

### Laptop health (IdeaPad 3 15IIL05 / 81WE) - complete
- Commit charge 14.9 GB -> 9.5 GB (-36%), processes 358 -> 268
- 15 auto-start services moved to Manual (`tools/trim-services.ps1 -Tier 2 -Apply -StopNow`)
- `vmmemWSL` capped at 2 GB via `.wslconfig` (was 2.9 GB)
- `RestartApps = 0` so Windows stops reopening apps at sign-in
- Codex sandbox service moved to Manual via registry (Set-Service denied)

### Pending - needs a human
- **BIOS** EMCN42WW (2020) -> EMCN60WW (2024-05-27)
  https://download.lenovo.com/consumer/mobiles/emcn60ww.exe
- **RAM** 8GB DDR4-2666 SO-DIMM -> 12 GB total (Lenovo PSREF max = 4GB soldered + 8GB)

### Toolkit
- `scripts/research.py` key-free search/fetch/HN/Wikipedia
- `scripts/office.py` JSON/MD -> xlsx/docx/pptx/csv
- `scripts/viz.py` SVG charts + Mermaid diagrams
- `docs/AGENT-ACTIONS.md` read/write/buy/sell contract for any agent

### Tooling
- `browse` 0.1.5 installed, registered with OpenCode, Claude Code, Codex, VS Code,
  Windsurf, Gemini CLI, Copilot CLI, LM Studio, Hermes. Extension pairing pending.

### Not present
- `graphify` and `demobase` do not exist on this machine. Optional, disabled in
  `core/stack.yaml`. Do not report them as broken.

## Active work - 2026-11-23

### Idle commit hogs - complete
- `ollama app` held **3.6 GB commit with no model loaded** -> stopped, `Ollama.lnk`
  moved out of Startup (Tier 2 = start on demand)
- `ChatGPT.exe` is really the **Codex MSIX package**; 14 processes / 1.17 GB commit.
  No autostart exists (manifest `Enabled="false"`, no Run key/task, `RestartApps=0`).
  It had been left running since 19/11 17:26. Killed; no respawn.
- Microsoft Copilot app (9 processes) and an unresponsive Settings window killed.
- Result: commit **17.9 GB -> 12.2 GB**, free RAM 1.07 -> 1.50 GB.
- Remaining 12.2 GB is mostly open Chrome/Edge tabs (3.5 GB) + this agent (1.0 GB).

### GitHub credentials - complete
- 4 targets -> 1 (`git:https://github.com`). Two distinct live tokens found.
- Duplicate `gho_XxIp…` entries and a second token `gho_hV2Y…` deleted.
- **User action:** revoke the OAuth app that issued `gho_hV2Y…`; it was printed
  during the audit and is treated as exposed.
- The leaked `gho_zjsFDSeR…` from 2026-11-19 is already revoked.
- Lesson recorded: `Select-String -SimpleMatch` with a regex caused a false
  "no credentials" result.

### Pending - needs elevation or a human
- Intel `ESRV_SVC_QUEENCREEK` (198 MB) + `UDCService` (126 MB): Access denied
  without an elevated shell.
- `AnyDesk` + `TeamViewer` still Auto (~67 MB). Decision needed before stopping.
- **BIOS** updated to EMCN60WW (was EMCN42WW) — verified done.
- **RAM** 8 GB -> 12 GB (8 GB DDR4-2666 SO-DIMM) still not bought.

### Craft Anything / Hermes wiring - complete
- 30 min of silence was NOT MCP: Hermes MCP test = 38 tools, enabled.
- Cause 1: Ollama stopped during RAM cleanup, so the local provider was down.
- Cause 2: `bonsai-2:4b` has no chat template; 57.7 s and ~200 hidden tokens
  for "OK". Switched Hermes to `lfm3:1.7b` (tool-calling, ~16-21 s).
- Cause 3: Craft Anything retries every ~90 s; two Hermes one-shots collide
  on one gateway (`Gateway disconnected`). Loop stopped; one builder at a time.
- Added `tools/agent-preflight.ps1` (7/7 PASS), `tools/wire-craft-anything.ps1`,
  `docs/MCP-WIRING.md`. Run preflight before every build on any workstation.
- 8 GB CPU: use OpenCode/cloud for builds. Desktop 16 GB+/GPU: 7B-14B local.

### Knowledge base - complete
- `data/build-facts.json` (curated), `data/index.json`, `data/knowledge.db`
  (SQLite FTS5: 107 docs, 388 chunks, 123 facts), `scripts/build_index.py`,
  `scripts/query.py`.
- Committed on purpose: a fresh clone on the desktop gets it with no network.
- `.gitignore` exception added for `data/knowledge.db`; all other `*.db`
  stay excluded as runtime state.

### Free cloud model migration - complete
- Hermes -> Nous API `stepfun/step-3.7-flash:free` (tool calls verified, 2.6 s
  on a 9k prompt). OpenCode -> `opencode/hy4-flash-free` (2.7 s, no credits).
- Craft Anything builder -> OpenCode (`craft.json` + `--backend OpenCode`).
- All paid Nous models return 404 (no credits); several free models have no
  tool support and were rejected. See `docs/MCP-WIRING.md`.
- Ollama no longer required for agents; stays Tier 2 and can be stopped.

### `polsia free v1` status
- Was blocked; now building successfully. First CLI run produced the Vite site
  (`app/`, `dist/` 9 files) and reached **83% likeness / 6 of 6 claims**.
- That CLI run hit a 600 s tool timeout; user restarted Craft Anything at 07:19
  and the new run is refining the existing app.
- Keep exactly one builder at a time. Monitor `build-activity.log`.

### Project database - complete
- `data/knowledge.db` remains the generic template. `projects/polsia-free-v1/knowledge.db`
  is the project's own copy (same schema + assets/sources/runs/approvals), with a
  working copy in the project workspace `.hive/`.
- Rebuild with `scripts/build_index.py --root <workspace> --project --out <db>`.
- `sources` ledger gives one sha256 per file: nothing duplicated or missed.

### Known gaps - next refinement
- **Team workflow:** studio currently picks one agent at a time. Required: one
  team of role-based members working concurrently, sharing messages and
  handoffs, with a task board and one-time authorisation. See `docs/TEAM-BRIEF.md`.
- **Authenticated pages:** original target redirected to `/login`; Craft Anything
  browser has no logins. Need logged-in screenshots/HTML from the user.
- Built nav link gaps FIXED: `/changelog` and `/acceptable-use` now exist;
  `npm run build` produces 15 dist files across 7 page folders.
- Ten inter-agent communication languages FIXED (pluggable registry, labelled,
  auto-routed, filterable, persisted). See `docs/TEAM-BRIEF.md` §3b.
- Remaining: visual likeness 78% (legal pages weakest, missing form field);
  authenticated dashboard pages need logged-in evidence from the user.
- Only run ONE builder at a time; concurrent runs overwrote `studio.js`.

### REA loop expansion - complete
- Gaps closed: internet/open-resource scan, closed-source reverse engineering,
  automatic setup with free-service substitutes, explicit intake/gap analysis,
  amend and implement phases, loop-until-criteria-pass, and human handoff cards.
- `PHASES` is now 13 data-driven stages; `FREE_SERVICES` registry added;
  handoff cards give the walkthrough and exact user input needed.
- `app/src/studio.js` 1,488 lines; `npm run build` succeeds (dist 15 files).
- `craft.json` paused to prevent duplicate auto-builders; resume one at a time.
- Remaining external blocker: logged-in dashboard evidence for the original.

### Recommendations ledger - complete
- `docs/RECOMMENDATIONS.md` holds P0/P1/P2 actions, user asks, known limits and
  installed-vs-optional tools. Same data is in `data/build-facts.json` under
  `recommendations` and `still_needed`, queryable with `scripts/query.py`.

## Active work - 2026-11-23

### Idle commit hogs - complete
- `ollama app` held **3.6 GB commit with no model loaded** -> stopped, `Ollama.lnk`
  moved out of Startup (Tier 2 = start on demand)
- `ChatGPT.exe` is really the **Codex MSIX package**; 14 processes / 1.17 GB commit.
  No autostart exists (manifest `Enabled="false"`, no Run key/task, `RestartApps=0`).
  It had been left running since 19/11 17:26. Killed; no respawn.
- Microsoft Copilot app (9 processes) and an unresponsive Settings window killed.
- Result: commit **17.9 GB -> 12.2 GB**, free RAM 1.07 -> 1.50 GB.
- Remaining 12.2 GB is mostly open Chrome/Edge tabs (3.5 GB) + this agent (1.0 GB).

### Credentials - complete
- 4 targets -> 1 (`git:https://github.com`). Two distinct live tokens found.
- Duplicate `gho_XxIp.` entries and a second token `gho_hV2Y.` deleted.
- **User action:** revoke the OAuth app that issued `gho_hV2Y.`; it was printed
  during the audit and is treated as exposed.
- The leaked `gho_zjsFDSeR.` from 2026-11-19 is already revoked.
- Lesson recorded: `Select-String -SimpleMatch` with a regex caused a false
  "no credentials" result.

### Knowledge base & agent preflight - complete
- `tools/agent-preflight.ps1` - checks MCP handshake, OpenCode, Hermes, provider, model
- `tools/wire-craft-anything.ps1` - idempotent agent registration
- `data/knowledge.db` committed (via `.gitignore` negation)
- `docs/MCP-WIRING.md` - root cause of the silent 15-min run + per-agent configs

### Craft Anything + Hermes diagnosis
- Failure was **not MCP** (38 tools, verified).
- 1. Ollama was stopped → Hermes provider timeouts (0 tokens in/out).
- 2. `bonsai-2:4b` has no chat template; measured 57.7 s for "OK".
- 3. Retry loop + concurrent Hermes runs collide.
- Fix: `hermes config set model.default lfm3:1.7b`; use preflight; 1 builder at a time.

### Pending - needs elevation or a human
- Intel `ESRV_SVC_QUEENCREEK` + `UDCService`: Access denied without an elevated shell.

### Claude Code + REA research - complete
- `docs/CLAUDE-CODE-DEEP-DIVE.md`: official skills/subagents/hooks/workflows/
  agent-teams, plus free reverse-engineered ecosystems and controlled evidence.
- Implemented in `app/`: SKILLS, HOOKS, SUBAGENT_TYPES, WORKFLOWS, AGENT_TEAMS,
  AUTO_MEMORY, DOCTOR. Build passes; visual check 81%, 30/30 claims.
- Documented but not yet in code: INSTINCTS, AGENT_ACCESS allowlist, run monitor,
  behaviour recordings, catalogue scaling (wave 4 of the deep dive).
- Policy: lean registries + direct CLI tools; MIT/Apache/CC0 patterns only.
