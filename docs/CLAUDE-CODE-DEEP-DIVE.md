# Claude Code deep dive — capabilities, free equivalents, what to adopt

Research date: 2026-11-23. Primary sources: `code.claude.com/docs` (official),
`agentskills.io`, and the GitHub REST API for repository/licence facts.
Web search was unavailable (HTTP 402); all findings below came from direct fetches.

## 1. What Claude Code actually has now

### Core engine
- Terminal CLI, IDE extensions (VS Code/Cursor/JetBrains), Desktop app and Web.
- `CLAUDE.md` / `AGENTS.md` memory files plus **auto memory** that saves learnings
  across sessions without the user writing anything.
- Git-native workflow: stages changes, writes commits, branches and opens PRs.
- Composable CLI: `claude -p "..."`, pipes, CI, `--agents`, `--append-subagent-system-prompt`.
- Scheduling: cloud routines, desktop scheduled tasks, `/loop`.
- Remote Control, Dispatch, `claude --teleport`, Slack `@Claude`, Chrome debugging.

### Skills (the biggest portable idea)
`SKILL.md` = YAML frontmatter + Markdown instructions, directory name is the
command. Skills follow the **Agent Skills open standard** (`agentskills.io`),
so they work across tools. Key frontmatter fields:

| Field | Purpose |
|---|---|
| `name`, `description`, `when_to_use` | discovery and auto-invocation |
| `context: fork`, `agent`, `background` | run in a subagent context |
| `allowed-tools`, `disallowed-tools` | permission scoping |
| `model`, `effort` | per-skill model/effort override |
| `paths` | activate only for matching files |
| `hooks` | lifecycle hooks registered while the skill is active |
| `!`command`` | dynamic context injection (runs shell before Claude sees the skill) |
| `metadata`, `license` | open-standard extension fields |

Locations: managed settings → `~/.claude/skills/` → project `.claude/skills/` →
nested → plugin → claude.ai sync. Bundled skills include `/doctor`, `/code-review`,
`/batch`, `/debug`, `/loop`, `/run`, `/verify`, `/run-skill-generator`, `/claude-api`.
`/run` + `/verify` + a recorded `run-<name>` skill let a project follow a saved
launch/verify recipe instead of rediscovering it.

### Subagents
Markdown files with `name`, `description`, `tools`, `disallowedTools`, `model`,
`permissionMode`, `mcpServers`, `hooks`, `maxTurns`, `skills`, `memory`, `effort`,
`isolation: worktree`, `color`. Built-ins: Explore (read-only), Plan (read-only),
General-purpose, `claude`, statusline-setup, claude-code-guide, web-fetch.
They preserve context, enforce tool restrictions, route to cheaper models and
can run in isolated git worktrees.

### Hooks
40+ lifecycle events: `SessionStart`, `UserPromptSubmit`, `PreToolUse`,
`PermissionRequest`, `PostToolUse`, `PostToolUseFailure`, `SubagentStart/Stop`,
`TaskCreated/Completed`, `Stop`, `StopFailure`, `TeammateIdle`, `PreCompact`,
`SessionEnd`, `FileChanged`, `ConfigChange`, `Elicitation`, and more.
Handlers can be `command`, `http`, `mcp_tool`, `prompt` or `agent`; they can deny
or rewrite tool calls, and `PostToolUse` can auto-format or lint after edits.

### Agent teams (experimental)
`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`. A lead session spawns teammates that
have **separate contexts**, a **shared task list** and a **mailbox**
(`~/.claude/teams/{team}/inboxes/{agent}.json`). Teammates self-claim unblocked
tasks, message each other directly, and can be individually steered. Quality
gates use `TeammateIdle` / `TaskCompleted` hooks (exit 2 = keep working).
This is the closest official analogue to the team the user asked for.

### Dynamic workflows
A JavaScript script (`agent()`, `pipeline()`, `parallel()`, `phase()`)
orchestrates dozens-to-hundreds of subagents in the background. Plans live in
code, not in the model's context; runs are **resumable**, agents auto-retry on
stall (up to 6 attempts), and results can be cross-checked adversarially.
`/deep-research` is the bundled example; `ultracode` triggers automatic workflows.

## 2. Free / reverse-engineered ecosystem (facts from GitHub API)

| Project | Stars | Licence | Relevance |
|---|---:|---|---|
| `milind-soni/OpenMausBot` | 27,013 | Apache-2.0 | Open Grok-bot alternative with a VM agents can use; agent/computer-use patterns |
| `AgriciDaniel/claude-obsidian` | 16,707 | MIT | Self-organising Obsidian second brain + knowledge graph; directly relevant to vault sync |
| `ParadevAI/Paradev` | 16,501 | MIT | Open Codex App/Conductor alternative; orchestrates parallel coding agents with your own subscriptions |
| `nexu-io/openmotion` | 15,561 | Apache-2.0 | Agentic video studio, 300+ Motion.md guides, 22 agents; skill-pack pattern |
| `HarnessMD/munder-difflin` | 9,700 | MIT | Local multi-provider agent harness / agent teams / custom worlds |
| `OpenCoworkAI/open-codesign` | 8,249 | MIT | BYOK, local-first, multi-model prompt→prototype/slides/PDF |
| `ZSeven-W/openpencil` | 7,330 | MIT | AI-native vector design with concurrent agent teams |
| `kalil0321/reverse-api-engineer` | 4,212 | MIT | Website → typed API client; works with Claude Code, Codex, Cursor, OpenCode |
| `alejandrobalderas/claude-code-from-source` | 3,017 | **none** | Architecture/patterns reverse-engineered from source maps |
| `NiazMorshed2007/reanimate` | 2,304 | MIT | Skill that reverse-engineers animation frame-by-frame and proves motion parity |
| `AIshihzong/awesome-reverse-engineer-anything` | 873 | CC0-1.0 | Curated REA case list incl. Clean-room and open-source alternatives |
| `ruvnet/open-claude-code` | 576 | MIT | "Nightly Claude Code CLI Decompile — Reverse Engineered & Rebuilt" |
| `T-Lab-CUHKSZ/claude-code` | 327 | **none** | Buildable research fork from reverse-engineered build system (Bun) |
| `senlindesign/taste-skill` | 515 | **none** | Skill: extract design tokens + rationale from any site |

### Safety / licensing boundary
- MIT/Apache/CC0 projects are safe to **study and reuse patterns from**, with
  attribution and their licence retained. Do **not** paste their code into `app/`.
- Repos with **no licence** are not licensed for reuse. Treat them as reading material only.
- Decompiled/rebuilt Claude Code binaries may breach the Anthropic terms of
  service and can carry malware or telemetry. **Do not install or run them.**
- We adopt **open standards and documented behaviour** (Agent Skills, MCP, hooks,
  subagent frontmatter, workflow shape), not proprietary source or keys.

## 3. Gap analysis: what this build is missing

Already present: 13-phase REA loop, ten inter-agent languages, free-service
registry, human gate, checkpoint ledger, project knowledge databases,
multi-member auto-selection, message bus, task board, handoffs.

Missing (highest value first):

1. **Skills registry with `SKILL.md` shape** — no reusable, on-demand procedure
   packages; the team re-derives the same workflows every round.
2. **Hooks / lifecycle gates** — no automatic policy on tool use, task completion
   or stop; nothing prevents a bad write or a premature "done".
3. **Subagent definitions** — roles exist as names only; no tool restrictions,
   model routing, worktree isolation or max-turn limits.
4. **Workflow engine** — the loop is sequential; no `parallel()`/`pipeline()`
   fan-out, resume, or adversarial cross-check of findings.
5. **Agent teams semantics** — no explicit lead/teammate mailbox and shared task
   claim protocol with file-locking-style safety.
6. **Auto memory + `/doctor`** — no cross-session learnings or self-checkup that
   reports and fixes setup problems.
7. **Recorded run/verify recipe** — builds succeed but the launch/check recipe is
   not saved as a reusable skill.

## 4. Concrete adoption plan (implemented in `app/`)

Add data-driven registries to `app/src/studio.js`, exposed in the UI:

- `SKILLS`: built-ins `doctor`, `verify`, `run`, `deep-research`, `code-review`,
  `reverse-api`, `taste-skill`, plus a project `run-<name>` recipe. Fields mirror
  Agent Skills: `name`, `description`, `when_to_use`, `context`, `allowedTools`,
  `model`, `paths`, `hooks`.
- `HOOKS`: events `PreToolUse`, `PostToolUse`, `TaskCompleted`, `Stop`,
  `SubagentStop`, `TeammateIdle`; handler types `command`, `http`, `mcp_tool`,
  `prompt`, `agent`; decisions allow/deny/rewrite with a reason.
- `SUBAGENT_TYPES`: `Explore` (read-only), `Plan` (read-only), `General-purpose`,
  `web-fetch`, each with `tools`, `model`, `permissionMode`, `maxTurns`,
  `isolation: worktree`.
- `WORKFLOWS`: script-shaped phases with `agent()`, `parallel()`, `pipeline()`,
  resume from saved results, stall retry and adversarial verification.
- `AGENT_TEAMS`: lead + teammates + shared task list + mailbox, self-claim and
  direct messaging, with `TeammateIdle`/`TaskCompleted` quality gates.
- `AUTO_MEMORY`: cross-session facts written to local state, surfaced in reports.
- `DOCTOR`: checks MCP wiring, provider/model health, free-service registry,
  broken links and build output; offers fixes.

## 4b. Second wave — skill packs and harness frameworks

A follow-up GitHub API query (`agent-skills in:name,description`, sorted by stars)
found much larger, directly reusable ecosystems:

| Project | Stars | Licence | What to take |
|---|---:|---|---|
| `mattpocock/skills` | 330,919 | MIT | Practical engineering skills from a real `.agents` directory; skill-shape conventions |
| `obra/superpowers` | 324,536 | MIT | Agentic skills framework + **subagent-driven development** methodology |
| `affaan-m/ECC` | 309,231 | MIT | Skills, **instincts**, memory, security and **research-first development** for Claude Code/Codex/OpenCode |
| `anthropics/skills` | 199,208 | none | Official Agent Skills examples (PDF/XLSX/DOCX/PPTX) — reference only, no licence to copy |
| `Shubhamsaboo/awesome-llm-apps` | 145,472 | Apache-2.0 | 100+ agents, skills and RAG apps as a discovery catalogue |
| `JuliusBrussee/caveman` | 122,268 | Apache-2.0 | Token-efficient skill + local proxy: shorter output, smaller tool results, **every original recoverable** |
| `Leonxlnx/taste-skill` | 120,384 | MIT | Art direction, reference images and browser checks instead of generic AI pages |
| `addyosmani/agent-skills` | 119,887 | MIT | Production-grade engineering skills for coding agents |
| `tt-a1i/archify` | 98,934 | Apache-2.0 | Idea/codebase → interactive diagrams (Mermaid/diagrams-as-code) |
| `OpenMontageInc/OpenMontage` | large | see repo | 12 production pipelines, 100+ tools, 700+ skill/knowledge files |

### Additional concrete takeaways for this build

1. **Research-first development** (ECC): no implementation until evidence is
   gathered and cited. Our `discover`/`reverse` phases already do this; make the
   rule explicit in the phase body.
2. **Instincts** (ECC): persistent, small learned rules that survive sessions —
   different from facts in memory. Add an `INSTINCTS` registry that the team
   writes after a failed approach and reads before each phase.
3. **Subagent-driven development** (superpowers): decompose a task into
   independent subagent jobs with verification before merge. Our `WORKFLOWS`
   registry should require a verifier agent after each builder agent.
4. **Token efficiency with recoverable originals** (caveman): compress tool
   output in the channel but store the full original in the project database,
   with a pointer. This keeps the UI fast without losing evidence.
5. **Taste / art direction** (taste-skill): when reverse-engineering a visual
   target, capture not only tokens but the *rationale* (why 480px, why mono)
   and verify in a browser. Our `taste-skill` built-in should do this.
6. **Diagrams as code** (archify): use Mermaid for plans and architecture,
   already supported by `scripts/viz.py`.
7. **Catalogue discovery**: treat `awesome-llm-apps` and `awesome-reverse-engineer-anything`
   as append-only source lists, not dependencies.

**Licensing reminder:** MIT/Apache projects may be studied and their patterns
reimplemented. `anthropics/skills` and projects with no licence are reference
only. Never copy code into `app/`; attribute ideas in this document.

## 4c. Third wave — by named agent ecosystem

GitHub API searches for each named system (stars/licences as of 2026-11-23):

| Ecosystem | Project | Stars | Licence | Best part to take |
|---|---|---:|---|---|
| Grok Bot | `milind-soni/OpenMausBot` | 27,013 | Apache-2.0 | VM that bots can use; computer-use patterns |
| Grok Bot | `HarnessMD/munder-difflin` | 9,700 | MIT | Local multi-provider harness, agent teams, custom worlds |
| Grok/Manus | `Anil-matcha/suparagent` | 7,156 | Apache-2.0 | **Named AI coworkers with instructions, memory, routines, their own isolated computer, and approval before acting** |
| Manus | `hexdocom/lemonai` | 1,570 | other | **Self-evolving** local general agent; study the evolution loop only |
| Manus/ChatGPT | `AFK-surf/open-agent` | 1,063 | Apache-2.0 | Open alternative to Agent SDK/ChatGPT Agents/Manus; multi-agent workspace |
| Claude Code/Codex/Manus | `Backboard-io/Backboard-Desktop` | 26 | other | Parallel agents, computer use, BYOK, built on Code-OSS |
| Claude Code | `ParadevAI/Paradev` | 16,501 | MIT | Orchestrate parallel coding agents with your own subscriptions |
| Claude Code | `ruvnet/open-claude-code` | 576 | MIT | Clean-room rebuild patterns (study only; do not run decompiled binaries) |
| Claude Code | `alejandrobalderas/claude-code-from-source` | 3,017 | none | Architecture notes from source maps — reference only |
| Claude Code | `T-Lab-CUHKSZ/claude-code` | 327 | none | Buildable research fork — reference only |
| Hermes | `amajorai/ryu` | 45 | other | **Monitor every run and control what agents can access**; plugin-based tools |
| Hermes | `Colton-z/AstraBox` | 17 | Apache-2.0 | Managed agents on your own infrastructure with **sandbox** |
| Hermes | `magnusfroste/flowwink` | 26 | MIT | **500+ skills** driving CMS/CRM/ERP; catalogue-at-scale pattern |
| Hermes | `winnifredbalistreri60-prog/murf` | 2 | MIT | Phone bridge / live agent desktop — remote-control pattern |
| OpenClaw | `AstrBotDevs/AstrBot` | 47,378 | AGPL-3.0 | IM integrations + plugins + multi-LLM gateway (AGPL: do not copy code) |
| OpenClaw | `poco-ai/poco-claw` | 1,357 | MIT | **Channel-based team collaboration + sandboxed runtime + nicer Web UI** |
| OpenClaw | `SimonSchubert/Kai` | 1,365 | Apache-2.0 | Cross-platform (Kotlin Multiplatform) mobile assistant |
| OpenClaw | `swarmclawai/swarmvault` | 739 | MIT | Local-first **knowledge graph + RAG + durable agent memory** for Claude/Codex/OpenClaw |
| OpenClaw | `kossakovsky/selfhost-ai` | 964 | Apache-2.0 | One-command self-hosted stack (n8n, Ollama, Qdrant, 30+ tools) |

### Concrete additions selected from the third wave

1. **Isolated per-member computer** (suparagent): each team member gets a
   namespaced workspace in the shared state, not just a role label.
2. **Routines** (suparagent): named recurring jobs per member, in addition to
   our global auto-mode interval.
3. **Access-control registry** (ryu) + **sandbox flag** (poco-claw, AstraBox):
   every tool call checks `AGENT_ACCESS` before running; risky actions are
   sandboxed or sent to the human gate.
4. **Run monitor** (ryu): a visible list of active/finished runs with owner,
   phase, cost/tokens and outcome, not just the activity log.
5. **Skill catalogue** (flowwink): `SKILLS` should be loaded from a catalogue
   with tags and counts, not a fixed list; add `CATALOGUES` for external lists.
6. **Durable agent memory + graph** (swarmvault): our per-project SQLite DB is
   the memory store; add a `graph` view exporting nodes/edges to Mermaid.
7. **Self-evolution ledger** (lemonai): record failed approaches as instincts.
8. **One-command bootstrap** (selfhost-ai): a `bootstrap-free-stack` skill that
   documents installing only free/self-hosted services.

Not adopted: anti-detect/stealth browser projects (`oss-invisible/dots`) —
evading bot protections is out of scope and conflicts with our human-oversight rule.

## 4d. Fourth wave — general reverse-engineering practice

Source: the CC0-licensed `AIshihzong/awesome-reverse-engineer-anything` list,
fetched directly (287 lines). Every entry is checked and tagged REA / AI-RE /
Rebuild / Claim?. Its own summary is that of six most-shared cases, only one
actually says it used REA.

### The most decision-relevant evidence

- `pablodiazjorge/rea-lab`: five preregistered studies, 482 Claude Code runs.
  **No significant solve-rate gain from REA**; REA runs took about twice the
  time and cost. Study 2: 11/24 solved without REA vs 4/24 with it (p = 0.092).
- `aicodeking/leanrea`: one **8 KB skill** that drives Ghidra/Hopper/JADX
  directly through the shell instead of an MCP layer. 36 runs: same accuracy,
  **38% less wall time, 35% less cost, 56% fewer turns, 60% fewer tokens**,
  and 34.5k tokens of context instead of 400.7k. Caveat: three reps per cell,
  one model, one machine, and the external tools were absent in both arms.
- Conclusion for us: **prefer lean skills + direct CLI tools over a large MCP
  layer**. Our use of the Craft Anything CLI rather than loading 300+ tools into
  context is already the right shape. Keep registries small and load on demand.

### Practical patterns worth adopting

1. **Hash-pinned evidence + differential tests** (`devtechedge/feature-heist`):
   every rebuild stores the evidence with a hash and has a differential test
   against the original. Our project DB already stores sha256 per source; add
   a differential check to `verify`.
2. **Behaviour recordings** (`erkamyaman/rust-anything`, `ruguevara/zx-reaper`,
   `AsyncFinn/rook`): record what the original returns/throws, rewrite one
   piece, replay the recording, then move on. This is stronger than visual
   similarity alone. Add a `BEHAVIOUR_RECORDINGS` ledger.
3. **Evidence IDs on every conclusion** (`pablodiazjorge/rea-casebook`): no
   finding without a cited `evidence_id`. Craft Anything already does this;
   require it in our report template.
4. **Sandbox + tool allowlist + hash-approved inputs** (`dagoSte/rea-safe-agents`,
   `lalbers/agent-sandbox`): no network, read-only roots, no capabilities, and
   only an allowlisted subset of tools. Maps directly onto our planned
   `AGENT_ACCESS` registry and human gate.
5. **Findings → spec → architecture → plan → validation**
   (`ShadowSwaps/REA-Reconstruction-Companion`): our `intake`/`plan` phases
   should emit these five artefacts explicitly.
6. **Clean-room default, deep mode opt-in** (Craft Anything itself): keep
   `clean_room: false` only in deep mode; never copy proprietary code.
7. **Legal boundary** (the whole list): own-copy only, interoperability,
   research and preservation. No DRM circumvention, no shipping original assets.

### Not adopted

Static recompilation of commercial games, console ports, anti-bot/stealth
projects, and anything requiring a legally purchased original we do not have.

## 5. Sources

- https://code.claude.com/docs/en/overview
- https://code.claude.com/docs/en/skills
- https://code.claude.com/docs/en/sub-agents
- https://code.claude.com/docs/en/hooks
- https://code.claude.com/docs/en/workflows
- https://code.claude.com/docs/en/agent-teams
- https://agentskills.io
- GitHub REST search API queries above (stars and licences as of 2026-11-23)
- https://github.com/AIshihzong/awesome-reverse-engineer-anything (CC0-1.0)
- https://github.com/pablodiazjorge/rea-lab, https://github.com/aicodeking/leanrea
- https://github.com/devtechedge/feature-heist, https://github.com/erkamyaman/rust-anything
- https://github.com/dagoSte/rea-safe-agents, https://github.com/lalbers/agent-sandbox
- https://github.com/ShadowSwaps/REA-Reconstruction-Companion
- https://github.com/mattpocock/skills, https://github.com/obra/superpowers,
  https://github.com/affaan-m/ECC, https://github.com/anthropics/skills,
  https://github.com/Shubhamsaboo/awesome-llm-apps,
  https://github.com/JuliusBrussee/caveman,
  https://github.com/Leonxlnx/taste-skill,
  https://github.com/addyosmani/agent-skills,
  https://github.com/tt-a1i/archify,
  https://github.com/OpenMontageInc/OpenMontage
