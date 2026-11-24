# Grok Bot team/worker + REA ecosystem study — 2026-11-24

Sources supplied by the person, plus a GitHub API search. Findings are
observations from the fetched pages. No Grok Bot code, assets or extracted
bundles were copied into `app/`. All quoted projects are independent and state
they are not affiliated with xAI.

## 1. x.ai/bot — the product shape (what "AI teammates" means)

From the live page:
- **Bots are teammates, not assistants.** They sign into your tools, appear in Slack/Teams, take projects start-to-end, and check in when approval is needed.
- **Parallel by default.** Give each Bot a job and add another when work grows; they work in parallel, hand off to each other, run 24/7.
- **Initiative.** Example: Sales Bot notices four renewals next month, pulls usage, runs health checks and drafts proposals *before being asked*.
- **Own computer.** "Sign a Bot in once, and it uses your apps and websites just like you would" — a browser/desktop per bot.
- **Teach once, remember.** Show a workflow once; it remembers the steps and repeats them (our `AUTO_MEMORY` + skills equivalent).
- **Meetings.** Bots join Google Meet/Zoom, listen, jump into chat, follow up afterwards.
- **Bot-to-bot delegation with visible trail.** Invoice Bot asks AP Bot in a channel; AP Bot replies, flags a third for a human. Humans see every step.
- **Learning/suggestions.** Bots keep context, suggest improvements ("Default Acme renewals to annual?") with Update / Not now.
- **Marketplace roles:** Sales Outbound, Talent Scout, Paid Media, Expense Manager, Product Performance, Bug Reproduction, Account Health, Chief of Staff.
- **Paid tiers** $30/$100/$200 per month in the product. Our build deliberately has no paid gates.

## 2. harsipsum/grokbot-rea — the REA study method

- **177 reader reports**, versions 0.71.2 → 1.2.3 (Oct–Nov 2026), folders: briefs, reports, studies, measured, live, parity, method, gateway.
- **Method:** unpack the shipped Electron app (`sand`), reformat bundles, one brief per feature area, run cheap read-only model readers (DeepSeek 4.1 flash) in parallel, each claim marked **READ** (file + line) or **INFERRED**, lead spot-checks quoted names, read-only live CDP captures for exact sizes/tokens, then a **~1,000-row parity matrix** rescored as the rebuild moves.
- **Uses `morluto/rea`** to extract, orchestrating Hopper/Ghidra/IDA/JADX; no original code in the study repo.
- **Two rules worth adopting verbatim in spirit:** separate read/inferred/unknown; quote only short identifiers and short strings; never paste original code.

## 3. nickvasilescu/orgo-teammates — open-source Grok Bot-shaped runtime (MIT)

- Previously published as `grokbot-clone` (GitHub still redirects). 295 stars, 145 forks.
- Stack: React/TS/Vite/Zustand web; Node/Hono/SQLite/SSE server; Grok Responses API runtime; Orgo VMs with noVNC; Composio connectors; realtime voice.
- **Each bot:** name, look, instructions, thinking effort, skills, memories, own desktop; one primary point of contact.
- **Team:** bots delegate, start subagents, join group chats with @mentions.
- **Approval model:** read actions run automatically; Composio **write** actions pause for approval with "remember my choice".
- **Routines** + app-event reactions + scheduled check-ins from the primary bot.
- **Security defaults:** server listens 127.0.0.1, `DEV_LOGIN` ignored off localhost, `ALLOWED_EMAILS` required on public URLs, keys on server only.
- Direct analogues in our build: `ROLES` + `ENGINES`, `SKILLS`, `HOOKS`, `AUTO_MEMORY`, `HUMAN_GATES`, `AUTONOMOUS_BOOTSTRAP`, bridge env secrets, `SUBAGENT_TYPES`.

## 4. unicodef1wn/grokbot-field-notes — operating rules (MIT, 729 stars)

- Three xAI engineers built and launched the product from an empty repo in 72 hours live on stream.
- Repo contents: `AGENTS.md` house rules, `ANTIPATTERNS.md` (40 failures and the rule from each), `agents/` (verification, orchestration, skills/routines, prompts), **69 role files** in `roster/`, 9 `playbooks/` (engineering, PM, founders, sales engineering, sales, SDR, support, post-sales, marketing), PDF guides, `ports/cursor` rules.
- Core paragraph: **give each agent one narrow job and a name; build a verification loop before the second agent; make the agent reproduce a bug before fixing it; attach proof to everything; write the general principle, not the specific story; audit routines weekly; keep a human gate on migrations, deploys, money and permissions.**

## 5. REA / Craft Anything ecosystem (forked versions and renames)

- **`morluto/rea`** — the original MIT MCP server + CLI (`npx rea-agents setup`, npm `rea-agents`). Orchestrates Hopper/Ghidra/IDA/JADX; static JS analysis needs no native engine. 400k+ stars.
- **`storytold/craft-anything`** — Rust engine, ~320 inspection tools, Study → build → Check → Ready, clean-room default, Deep mode opt-in. The tool driving this project.
- **`AIshihzong/awesome-reverse-engineer-anything`** (CC0, 896 stars) — curated, claim-checked cases. Notable verified REA rebuilds: `rec-rs` (OBS), `hexgrab` (PowerToys), `paper-rs`, `ledger-reborn` (QuickBooks), `blender-agent-sdk`, `OpenBattlefield2`, `feature-heist` (hash-pinned evidence + differential tests per rebuild).
- **Agent integrations/renames** (different names, same idea): `dsh-rea`, `rea-dsh-plugin`, `dsh-rea-mcp`, `picode-rea`, `rea-mcp` (LM Studio), `oh-my-rea` (`omr`), `marrow` (formerly REA Studio), `anyrea`, `rea-agent-docker`, `docker-reverse-engineer-anything`, `REA-ReverseEngineerAndroid` (hard fork 6.8.0, 117 tools), `rea-python`, `rea-flake`, `coop-anything`, `co-op`.
- **Evidence discipline tools:** `rea-casebook` (conclusions must cite `evidence_id`), `rea-safe-agents` (container-isolated REA with 27-tool allowlist), `agent-sandbox`, `reaproof`, `leanrea` (8 KB skill, 38% less time / 35% less cost at same accuracy in one 36-run benchmark).
- **Honest evidence on REA itself:** `rea-lab` ran 5 preregistered studies, 482 runs with Claude Code — **no significant solve-rate gain**, about 2× time and cost; `leanrea` 36 runs found a plain-CLI skill close to REA's accuracy (74/75 vs 75/75) with 38% less wall time and 35% less cost. Conclusion from the curated list: use REA for targeted questions on a known surface, not open-ended exploration.
- **Grok Bot–specific neighbours:** `b-nnett/grok-bot-0.18-reconstructed` (manual RE, archived), `RongleCat/grok-bot-sdk` (0.78.1 API), `ArvinYin1/grokbot-animation-anatomy` (53 avatar states), `jeremy-prt/bloub` (14 avatar states measured from video), `storytold/photocraft` and the *Craft apps* (clean-room rewrites).

## What we actually adopt

1. **Narrow jobs + names** → our `ROLES` already do this; add the marketplace-style job descriptions as `BOT_ROLES`.
2. **Rooms / turn order / @mentions** → add `ROOMS` + mention routing to the shared bus.
3. **Primary point of contact** → `lead` role stays the single front door.
4. **Teach once, remember** → `AUTO_MEMORY` + skills already do this.
5. **Read-only default, write approvals** → `HUMAN_GATES` + `AUTO_APPROVABLE_GATES` already do this.
6. **Proof attached to everything** → our `evidence/rea/*.json` with offsets + hashes; extend to action records.
7. **Reproduce before fix** → add a `verify-first` rule to QA (`tester`/`reviewer` roles).
8. **Weekly routine audit** → `AUTONOMOUS_BOOTSTRAP` + `RUN_MONITOR`.
9. **Human gate on money, deploys, permissions** → payments `confirm: true`, account switches, publish actions.
10. **REA targeting** → use the byte-accounting script for *specific* artifacts, not endless exploration; record unknowns, do not pretend 100% understanding where only 100% accounting exists.

No proprietary code was copied; all of the above are behaviour patterns reimplemented with our own tokens and free defaults.
