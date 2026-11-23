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

### 4. Automation and human oversight

- Auto mode runs in rounds with intervals: hours, days, weeks, months, years,
  or non-stop. A visible countdown shows the next round.
- The person authorises once. That authorisation is remembered in local state;
  ordinary actions do not ask again. Sensitive actions can still be gated.
- Reports (round summary, messages, decisions, files changed) can be sent to a
  configured email address or chat webhook. No API keys are hard-coded.

### 5. Constraints

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
8. `npm run build` succeeds and the visual check still passes.
