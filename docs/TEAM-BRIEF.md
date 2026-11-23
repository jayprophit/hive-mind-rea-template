# Team workflow brief — polsia free v1

## The correction

The current studio is a **picker**: a list of agents you select one at a time.
That is not what was asked for. The requested system is **one team** that works
together, like a real company or organisation: members have roles, work at the
same time on the same task, and pass information between themselves.

## What to build in `app/`

### 1. One team, not a picker

- Remove the "choose an agent" interaction as the primary mode.
- Show a **team** of role-based members, all present and active on the current
  task. Selecting a member opens their detail/status; it does not switch the
  system to only that member.
- Default state: the whole team is working on the shared task.

### 2. Concurrent work with roles

- A task is created once. The orchestrator decomposes it into role-sized jobs
  and assigns them to several members **at the same time**.
- Members have distinct roles (orchestrator, planner, researcher, engineer,
  reviewer, tester, operations, integration, documentation, support, finance,
  QA, etc.), each with goals, permissions and a live status:
  `idle → working → blocked → handoff → done`.
- Several members can be `working` simultaneously.

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

1. One task assigned to the team causes several members to show `working` at
   the same time.
2. A message from one member appears in the shared channel and can be addressed
   to another member, who responds or produces a handoff artefact.
3. The task board updates automatically as work moves between members.
4. Authorisation is requested once, then remembered.
5. Auto-mode interval selector includes hours/days/weeks/months/years/non-stop.
6. `npm run build` succeeds and the visual check still passes.
