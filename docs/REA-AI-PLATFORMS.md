# REA plan — five AI platforms

Written 2026-11-25 for the owner's request to REA ChatGPT, Claude, Manus,
DeepSeek and Kimi and add what is useful to this project.

Registry: `app/src/rea-targets.js` (`window.PFV1_REA`), tests in
`app/tests/rea-targets.test.js`.

## What this is and is not

This is **competitive, public-surface reverse engineering for original
design**, not cloning. We record what a visitor can see, describe mechanisms
in plain words, then build our own implementation. We do not copy source,
prompts, assets, copy or branding, and we do not bypass authentication,
paywalls, CAPTCHAs or rate limits.

Every target needs an account for the chat surface. The public landing,
pricing, help and documentation pages can be observed without one. Anything
behind a login is done only in the owner's own session, with the owner's
permission, and stays `OBSERVED`, not `VERIFIED`.

## Method (same 11 phases per target)

1. Scope — the question, the boundary, the stop conditions.
2. Public surface — landing, pricing, help, docs.
3. Navigation — visible routes and menus; note what needs an account.
4. Controls — every visible control and its states.
5. States — empty, loading, streaming, stopped, error, limit reached.
6. Limits and pricing — record public numbers, mark them unverified.
7. Mechanism — plain-word description of how it appears to work.
8. Original design — our own equivalent, fitted to the existing app.
9. Build — behind the existing human gate, free/local first.
10. Test — unit tests plus a visual check at 1440/768/390.
11. Attribute — observed vs inferred vs built, with the source.

## Targets

### ChatGPT — `https://chatgpt.com/`

Observe: streaming reply with stop, model/reasoning picker, file/image/voice
input, canvas-style side panel, memory and projects, browsing/code/image
tools, history and sharing.

Build originally: local streaming transcript with a real stop button, an
engine picker that names engines not teammates, a side panel for generated
documents, opt-in local memory with export and erase.

Boundary: account required for chat; no automated probing of the service.

### Claude — `https://claude.ai/new`

Observe: single-column composer, artifacts panel, projects with knowledge,
attachments, connectors/MCP-style tools, extended-thinking indicator.

Build originally: composer with attachment tray, artifact panel with copy,
download and version history, project workspace with local knowledge files,
optional connector registry with explicit consent.

Boundary: account required; public docs and pricing only otherwise.

### Manus — `https://manus.im/app`

Observe: task-style agent runs, plan and step log, browser/computer-use
steps, deliverable files, scheduled tasks, workspace and knowledge.

Build originally: durable task record with plan, steps and status; human
approval before browser or file actions; deliverables stored locally with
provenance; scheduled runs with a visible cancel control.

Boundary: account required; computer use is high-risk and always human-gated.

### DeepSeek — `https://chat.deepseek.com/`

Observe: chat with reasoning toggle, web search toggle with citations, file
upload and long-document reading, code blocks, open-weight model and API docs.

Build originally: reasoning toggle that is honest about the mode, search
toggle that keeps source links, local document reader with stated limits,
engine registry that can point at a local model.

Boundary: account required for chat; docs and API pages are public.

### Kimi — `https://www.kimi.ai/en`

Observe: long-context chat and document reading, research/agent modes,
slide and document generation, file and web-page input, responsive entry
points.

Build originally: long-document reader with a visible context budget,
research mode that lists sources and open questions, document/slide export
to local files, layout that works at 390 px.

Boundary: account required for chat; public pages otherwise.

## Evidence vocabulary

`REFERENCE` → `OBSERVED` → `MODELLED` → `BUILT` → `TESTED` → `VERIFIED`,
with `BLOCKED` when a term, login or rate limit stops the work. Nothing moves
to `VERIFIED` without a local test.

## What the owner must provide

- Permission to observe each platform in the owner's own signed-in session,
  or a decision to stay on public pages only.
- A check of each platform's terms before any automated observation.
- Any API keys only if a target's API is used; keys stay in bridge env and
  are never stored in app state.

## Current status

All five are `REFERENCE`. The registry and plan generator exist and are
tested; no target has been observed yet, and no claim is made that it has.
