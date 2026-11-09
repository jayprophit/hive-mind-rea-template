---
type: vocab
date: 2026-11-09
supervisor: "bonsai-2:4b"
router: "laya"
grafana: "http://127.0.0.1:3000/d/work-matrix"
---

# Claude Vocabulary — How It Maps To Our Hive Mind

*Every term is a Hermes Bot + OpenCode subagent skill, not just a label. Supervisor routes, workers do.*

| Term you named | What Claude means it is | What it is in our stack |
| --- | --- | --- |
| **loop engineering** | Dynamic Workflow JS: `agent()` spawns one subagent; `parallel()` fans out; `pipeline()` streams each item. Failure modes combated: agentic laziness, self-preferential bias, goal drift | Hermes `message_agent(target="coder")` + OpenCode `subagent` tool + Grafana `requestId` dedupe |
| **claude-red** | Red-team harness — untrusted input (Slack tickets) goes to reader agents with read-only tools, never writes/commits | @researcher = read-only, @windows = high-privilege actor only sees summaries |
| **replay theater** | Replaying sessions / trajectories to debug — `state.db` + logs | Hermes `replay` verb regenerates TUI history from state.db |
| **terminal browser** | In-editor terminal pane + browser control | Hermes `browser_exec` (local Chromium) + `terminal local` |
| **reflect** | Post-turn `/reflect` summarises what went wrong | `PROJECT_MATRIX.md` gaps → `SOUL.md` update `/skill` |
| **blast radius** | Scope of a change — file, module, service, fleet | Coders get `worktree` isolation, reviewers get `read` only |
| **cache tax** | Prompt caching cost when you rewrite past context mid-conversation (Hermes invariant: mutating past context swaps toolsets and multiplies cost, only compression is exception) | Supervisor delegates, never rewrites. Use `/compress` only. |
| **filetree** | File map, filetree `/tree` understanding | `filetread` + `glob` + `grep` tools via OpenClaw Node |
| **you should know** | Claude’s 4 knowledges: subagents vs workflows, skills vs MCP, hooks vs CLI, cost vs quality | Hermes Bot Mode roster covers all 4: `@coder` (subagent), `@beam/@longcat-2-5` (workflow), `@researcher` (skills), `cost_guard` |
| **claude skins** | Pure data `SkinConfig` — colors, spinner faces, thinking verbs | Hermes `display.skin` in `config.yaml`, key-by-key table |
| **savvy progress** | Headway widget — task sub-progress on redirected prints | Hermes `display` progress HUD, `orchestrated progress footer` |
| **mods** | Claude Code Mods — Data sette, Loom, Obfuscator, Operator Mode, VibeSec | Hermes equivalents: `plugins/model-providers/ollama-cloud`, `plugins/memory/obsidian-memory`, `plugins/delegation/default`, `plugins/post_update/`, Kanban |
| **context 7** | Long-window filetree `/tree`/`context7` reading | `context_length: 1000000` in Hermes config, `optimise` prune |
| **skill ui** | Desktop `Skills` lane in `ui-tui/src/app/` | Local `skills/` folder at HERMES_HOME/skills/ |
| **vibeSec** | Vibecoding security tag — `/security audit`, OSV.dev for venv/plugins/MCP | `hermes security audit` in your setup |
| **supabase** | Common MCP server (`mcp_catalog.py`, `mcp.json`) | Connect Supabase MCP → Hermes can query tables (`supabase/mcp.json` catalog) |
| **playwright** | Browser tool primitive | Hermes `tools/builtin/browser` → read `mcp.json` for Playwright MCP |
| **claude-content-skills** | Declarative skill wrappers — content creation micro-tasks (`/review-pr`, `/deploy-staging`) | Local `skills/` + OpenCode `@writer`/`@marketer` |

## How the hive runs this loop

```
Plan → Design → Build → Check → Research → Recheck → Build → Fix → Amend → Compare
 → Feedback → Fine-tune → Plan → Build → Discovery → Test → Compare
 → Gather data → Weakness/Gaps → Improve → Next version
```

Every step writes one row to `Daily/2026-11-09.md` + `Work/Project.md` + `Work/PROJECT_MATRIX.md` frontmatter (`requestId, tokens_total, cost_usd, risk(laya)`). Grafana scrapes Pros + Daily notes to build live matrix. **No duplicate requestId = no duplicate work.**

*Top pick local:* `bonsai-2:4b` (1.6GB, 256K, vision+tools+thinking) — unlimited tokens, 8-12 tok/s on i3-1005G1. Escalate cloud free models once/day (token heavy) when `is_risky>0.8`.
