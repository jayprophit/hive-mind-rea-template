# Recommendations and what is still needed

Living document for the `polsia free v1` build and the portable template.
Updated 2026-11-23. See `data/build-facts.json` for the machine-readable version.

## 1. Highest-impact recommendations (implement next)

| Priority | Item | Why | Where |
|---|---|---|---|
| P0 | **Logged-in capture evidence** | Original target redirects to `/login`; Craft Anything's browser uses a fresh profile with no logins. The authenticated dashboard is the main "missing parts" gap and cannot be inferred from public pages. | User supplies screenshots/saved HTML → `capture/dashboard/` |
| P0 | **Checkpoint / resume** | Three builds were lost to crashes and PTY timeouts. Persist phase, attempt, artefacts and gap list in IndexedDB after every phase so a restart resumes instead of rebuilding. | `app/src/studio.js` |
| P0 | **One builder at a time** | Two concurrent builders repeatedly overwrote `studio.js`. `craft.json` is paused; resume one run, wait for it to finish, then start another. | `craft.json`, operator |
| P1 | **Self-evaluation harness** | Run `npm run build` + link check + console errors + unit tests + visual comparison as one scored command, stored per round. Acceptance criteria then become machine-checked rather than judged. | `app/` + Craft Anything `rebuild_check` |
| P1 | **Visible blackboard panel** | Ten communication languages exist, but the shared blackboard facts are not visible. A panel would let the person see what agents know and spot bad facts early. Builder explicitly offered this. | `app/studio/index.html`, `studio.css`, `studio.js` |
| P1 | **Phase-runner tests (Vitest)** | The 13-phase engine and language router are now large; a self-modifying team can silently break them. Add tests for phase order, loop-back, human gate and registry routing. | `app/tests/` |
| P1 | **Model fallback registry** | Free Nous and OpenCode endpoints sometimes 429 or 503. Auto-failover to the other free endpoint, then local `lfm3:1.7b`, with a visible notice. | `app/src/studio.js`, `docs/MCP-WIRING.md` |
| P2 | **Payment guardrails** | Payments are test-mode only; add idempotency keys, a spend cap, an audit log and explicit confirmation before any live-mode switch. | `app/src/studio.js` |
| P2 | **Source provenance UI** | Sources are recorded, but a simple "evidence → decision" view would make the reverse-engineering work auditable. | `app/studio/index.html` |
| P2 | **Retrospective-driven prompt rewriting** | Use the round retrospective to adjust the next round's phase order and role assignments automatically. | `app/src/studio.js` |

## 2. What is still needed from the person

| Item | Exact ask | Blocks |
|---|---|---|
| Logged-in pages | Screenshots or "Save page as → HTML" for the dashboard at `https://polsia.com/dashboard/untitled-l1v2k8` and its main tabs while signed in. Put them in `capture/dashboard/`. | Faithful reproduction of the dashboard UI/mechanisms |
| GitHub token cleanup | Revoke the OAuth app that issued `gho_hV2Y…` (it was exposed during the credential audit). The local entry is deleted; the token is still valid on GitHub. | Security |
| RAM | Fit an 8 GB DDR4-2666 SO-DIMM (one slot; 4 GB soldered) for 12 GB total. | Compiling and multiple agents on the laptop |
| Elevated maintenance | Run an elevated shell to move `ESRV_SVC_QUEENCREEK` and `UDCService` to Manual (~324 MB), and run `tools/repair-windows-admin.ps1`. | Memory and driver repair |
| Remote-access decision | Keep or disable `AnyDesk` and `TeamViewer` autostart (~67 MB). Stopping them could lock out remote access. | Memory |
| Repo review | `repos/` is 1.56 GB and excluded from git; review which clones to keep. | Disk |
| Builder control | Resume **one** build at a time. `craft.json` is paused to protect the verified build. | Avoid corrupted files |

## 3. Known limitations (honest ledger)

- Visual check is ~80–82% alike, 30/30 claims. Legal pages (`/privacy`, `/terms`) are weakest; the checker reports a missing form field and some missing text/colours.
- The dashboard behind login is **not** reproduced — no evidence exists locally.
- Payments are integration scaffolding in test mode, not a live merchant account.
- The app runs locally in the browser; multi-device sync needs a user-configured endpoint.
- Craft Anything's `web_site_open` has no login state by design.

## 4. Tools installed vs optional

Installed and in use: `sqlite-utils` 4.2.1, Pillow, PyYAML, pandas, matplotlib, python-docx/pptx/openpyxl, free cloud model wiring, `browse` and craft-anything MCP.

Optional, not installed: DB Browser for SQLite (GUI), Datasette (browser DB UI), `ripgrep`, `jq`. None are required.

## 4b. Composio — useful, but optional

Researched 2026-11-23 from `composio.dev`, `docs.composio.dev/docs/claude-code-plugin`
and the GitHub API (`ComposioHQ/composio`: 31,254 stars, MIT, TypeScript).

**What it gives you:** 1,700+ app connections (Gmail, Slack, GitHub, Notion,
HubSpot, Instagram, and most of the social/business tools in the brief), managed
OAuth so your app never holds provider tokens, per-action permission limits and
audit logs. It works with Claude Code, Hermes, OpenClaw, Codex, Cursor and any
MCP client, which matches the agent stack here. Free Hobby plan: 100,000 tool
calls/month.

**Why it is optional here:** credentials are held by Composio Cloud by default
(self-hosted/CMK are enterprise); some third-party tools (search, transcription,
media generation) are billed separately; and a browser-only static app cannot
safely hold a Composio API key — it needs a small backend proxy or the MCP URL
registered with the agent instead. That conflicts with the "no account, fully
local by default" goal.

**Recommendation:** add it as an optional `MCP_SERVERS` / `CAPABILITIES` provider
with the free Hobby tier, alongside the existing local-first providers. Keep
`mailto:`, local MCP and webhook paths as the zero-setup default. Never make a
Composio account a prerequisite for a feature.

## 5. Where the machine-readable version lives

`data/build-facts.json` contains `recommendations`, `still_needed`, `requirements`, `lessons` and `pending`. The knowledge base indexes them:

```powershell
python scripts\query.py --facts recommendations
python scripts\query.py --facts still_needed
python scripts\query.py --db projects\polsia-free-v1\knowledge.db --facts project
```
