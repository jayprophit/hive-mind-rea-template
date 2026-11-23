# Team workflow brief — polsia free v1

## The correction

The current studio is a **picker**: a list of agents you select one at a time.
That is not what was asked for. The requested system is **one team** that works
together, like a real company or organisation: members have roles, work at the
same time on the same task, and pass information between themselves.

## What to build in `app/`

### 1. No picker — the task selects the members

- **Remove member selection from the UI entirely.** The person types a task and
  presses Go. They never choose who works on it.
- The system automatically selects the right member(s) for that task by role,
  and shows **why** each was chosen ("Matched: research, data analysis, QA").
- Members are visible as a live team roster with status, but clicking one only
  opens their detail — it does not make the system work on only that member.
- Default state after a task is submitted: the selected members work together.

### 2. More than one member is active by default

- A task is created once. The orchestrator decomposes it and delegates to
  several members **at the same time**, based on the task's needs.
- **More than one member is always active** unless the task genuinely requires
  only one role. When a single member is selected, the UI explains why
  ("Single-role task: documentation only"). This decision is automatic.
- Members have distinct roles (orchestrator, planner, researcher, engineer,
  reviewer, tester, operations, integration, documentation, support, finance,
  QA, etc.), each with goals, permissions and a live status:
  `idle → working → blocked → handoff → done`.
- Several members must be able to show `working` simultaneously.

### 3. Shared communication (the important part)

- Implement a **shared message bus** in the browser (event bus + `localStorage`
  persistence, no backend):
  - members post messages to the team channel with `{from, to, taskId, type, body, time}`
  - `to` may be a member id, a role, or `all`
  - a member's output can become another member's input (artefact handoff)
- The UI shows a **team channel** (chronological messages), a **task board**
  (to-do / in progress / review / done with owner and role), and a **handoff
  trail** showing what each member passed to whom.
- Members react to messages addressed to them and to new tasks in their role;
  this is what makes it feel like a team rather than a list.

### 3b. Agents have several languages — support them all

Agents do not all speak the same way, and the team must be efficient. The shared
bus must support **more than five** distinct communication types, label each
message with its type, choose the right one automatically, and let the person
filter the channel by type. Implement at least these:

| # | Language / type | Use |
|---|---|---|
| 1 | Natural-language prose | human-readable team channel and summaries |
| 2 | Canonical JSON envelope | `{from,to,taskId,type,body,time,priority}` — the internal wire format |
| 3 | Compact task/intent DSL | short verbs: `TASK`, `ASSIGN`, `ASK`, `ANSWER`, `HANDOFF`, `BLOCKED`, `DONE` |
| 4 | Markdown artefacts | plans, specs and reports passed between roles |
| 5 | Tool/function-call format | `{tool, arguments, result}` for work done by a member |
| 6 | Topic-based events (pub/sub) | `task.created`, `build.failed`, `review.ready` with subscribers |
| 7 | Shared blackboard state | small key/value facts any member can read/write, with versions |
| 8 | Semantic tags / embedding-style summary | compact meaning tags plus a short vector-like digest for fast matching |
| 9 | A2A/MCP-style envelopes | agent-to-agent and tool-result messages compatible with external agents |
| 10 | Human report digest | plain-language round summary for the person (email/chat) |

Rules:
- A message carries a `language` field; the UI shows which language was used.
- The router picks the most efficient type for the situation (DSL for control
  messages, JSON for machine handoffs, Markdown for documents, prose for the
  person).
- New languages must be pluggable: a `LANGUAGES` registry, not hard-coded
  `if/else` chains.
- All languages persist to the same local message log and participate in the
  handoff trail.

### 4. Automation and human oversight

- Auto mode runs in rounds with intervals: hours, days, weeks, months, years,
  or non-stop. A visible countdown shows the next round.
- The person authorises once. That authorisation is remembered in local state;
  ordinary actions do not ask again. Sensitive actions can still be gated.
- Reports (round summary, messages, decisions, files changed) can be sent to a
  configured email address or chat webhook. No API keys are hard-coded.

### 5. Autonomy — the continuous REA loop

Given a task, the team runs this loop **without hand-holding**, and keeps
cycling until the task's acceptance criteria pass or a human-only item blocks it:

| # | Phase | Key | What must happen |
|---|---|---|---|
| 1 | Intake + gap analysis | `intake` | Restate the task, write acceptance criteria, list what is known/unknown, identify exactly what is missing and what the user must supply. Produce a gap list with severity. |
| 2 | Plan | `plan` | Decompose the gaps into role-sized jobs, assign owners, set order and dependencies. |
| 3 | Internet + open resources | `discover` | Search the internet for similar builds, prior art, docs and data. Check open-source repos, public datasets and free services. Record each source with a URL and a one-line finding. |
| 4 | Reverse-engineer closed sources | `reverse` | Where a target is closed, inspect what is observable: page/HTML, JS bundles, network requests, file formats, strings and behaviour. Record evidence; never copy proprietary code into `app/`. |
| 5 | Automatic setup | `setup` | Install/configure whatever the build needs: tools, free-tier accounts/endpoints, model providers, storage and integrations. Use free substitutes for paid services (see registry). |
| 6 | Build | `build` | Produce the first working version from the gathered evidence. |
| 7 | Test | `test` | Run automated checks: build, links, console errors, unit tests, visual comparison. |
| 8 | Check / verify | `check` | Independent review against the acceptance criteria by roles that did not build it. |
| 9 | Fix errors | `fix` | Correct every failure; re-run the failing check. |
| 10 | Amend | `amend` | Improve the result using new evidence: wording, layout, logic, data and missing content. |
| 11 | Implement | `implement` | Integrate the amended work, rebuild and freeze a version. |
| 12 | Report + retrospective | `report` | Write the round report, what changed, what is still blocked, and the next improvement. |
| 13 | Loop | `loop` | If any acceptance criterion fails, return to phase 3 (new evidence) or 6 (rebuild) with a new attempt. Continue until achieved or blocked only on the human gate. |

Rules:

- A task is `done` only when every acceptance criterion passes and the gap
  list is closed. "Good enough" is not a stopping condition.
- Failures never end the loop: retry with a different approach, then hand the
  job to another role if it stays blocked.
- `PHASES` in code must be data-driven so new phases can be added without
  rewriting the runner.
- The activity log must show phase, attempt number, evidence used and owner.

### 5b. Free services instead of paid ones

Keep a `FREE_SERVICES` registry that maps a paid capability to a free/open
substitute and uses it automatically unless the user supplies their own:

| Paid capability | Free substitute |
|---|---|
| Search / web data | Marginalia, Hacker News, Wikipedia, direct site fetch, Bing/DDG HTML, user's browser via `browse` MCP |
| LLM inference | Nous free tier models, OpenCode free models, local Ollama fallback |
| Repo / hosting | GitHub free, GitHub Pages, local git |
| Storage / DB | IndexedDB + local SQLite knowledge databases in this repo |
| Diagrams / docs | Mermaid, Markdown, Open XML (.docx/.xlsx/.pptx), CSV, SVG, HTML |
| Email reports | `mailto:` draft plus a user-configured free webhook |
| Payments | Stripe/PayPal **test mode** with the user's own key; no gating of features |
| OCR / PDF / media | Local Python libs already installed (pypdf, Pillow, pandas) |

Every substitute records `substitutesFor`, cost `0`, and a source URL. If a
free option cannot do the job, the team produces a user handoff card instead
of silently failing or buying anything.

### 5c. Human gate — only what the person must do

When a step needs a login, API key, payment credential, irreversible action or
authorisation, the team must not stop the whole loop. It creates a **handoff
card** containing:

- exactly what is needed and why (one short paragraph),
- a numbered click-by-click walkthrough to get it,
- the precise field/link/permission required,
- which task and phase is waiting,
- a "continue without it" fallback if one exists.

All other members keep working on independent gaps. Once the user supplies the
item, the waiting phase resumes automatically. Authorisation given once is
remembered; only sensitive or irreversible actions ask again.

### 6. Payments (commerce, not feature gates)

- The app must be able to **take payments** for real transactions through a
  payment provider the person configures (e.g. Stripe or PayPal, test mode by
  default): create an invoice/checkout, record the transaction, issue a receipt.
- This is **not** a subscription, credit system or paywall. No feature, core,
  module or function may require payment to activate. The earlier requirement
  "no paid feature gates" still wins.
- Never hard-code keys or treat a payment as permission to use a feature.

### 7. Self-improvement of delivery

- At the end of each round the team writes a short **retrospective** into local
  state: what failed, what was retried, what worked, what to change next time.
- Track a simple completion metric (tasks done / attempted, retries, blocked
  items) and show it in the UI.
- Failed tasks go back on the board with a different owner or approach instead
  of disappearing.

### 8. Constraints

- Keep the captured visual design: same fonts, 480 px column, breakpoints,
  monochrome palette and no sideways scroll on phone.
- No subscription, credits, tokens-to-buy or paid feature gates anywhere.
- Everything runs locally in the browser unless the person configures their own
  endpoint. Do not paste the original site's code into `app/`.
- Only edit files inside `app/`. Build with `npm run build` until `dist/` is
  produced, then run the Craft Anything visual check and fix what it reports.

## Acceptance criteria

1. There is **no control to pick a member**. The person only enters a task and
   presses Go.
2. Submitting a normal task automatically activates **more than one** member;
   each shows `working` at the same time, with a visible reason for selection.
3. A single member is active only for genuinely single-role tasks, and the UI
   says why. This is automatic, not chosen by the person.
4. A message from one member appears in the shared channel and can be addressed
   to another member, who responds or produces a handoff artefact.
5. The task board updates automatically as work moves between members.
6. Authorisation is requested once, then remembered.
7. Auto-mode interval selector includes hours/days/weeks/months/years/non-stop.
8. A task runs the full 13-phase REA loop (intake/gap analysis → plan →
   discover internet+open resources → reverse-engineer closed sources →
   automatic setup → build → test → check → fix → amend → implement → report →
   loop) without manual steps. It keeps cycling until every acceptance
   criterion passes or a human-only item is handed off.
9. A payment integration can create a test-mode checkout and record it, while
   no feature is locked behind payment.
10. Each round produces a retrospective and a visible completion metric.
11. At least ten communication languages/types are supported, each message is
   labelled with its type, the channel can be filtered by type, and new types
   are added through a registry.
12. A `FREE_SERVICES` registry maps paid capabilities to free substitutes and
   uses them automatically; no paid tool is required to complete a task.
13. Human-only items produce a handoff card with the walkthrough and the exact
   field/permission needed, while other members keep working.
14. The gap list, sources with URLs, attempts and evidence are visible in the UI
   and written into the round report.
15. `npm run build` succeeds and the visual check still passes.
