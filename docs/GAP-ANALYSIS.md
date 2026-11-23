# Gap analysis — Polsia Free v1

Date: 2026-11-23. Based on a fresh audit of `app/`, `dist/` and the repo, then
updated after the "install the missing gaps" pass.

## Verified complete

- `npm run build` passes; **40 HTML pages** in `dist`.
- **0 broken links**: 23 internal HTML links, 41 JS path literals, all resolve.
- All 7 workspace deep links resolve to real `panel-*` IDs and activate the tab.
- 38+ audited capability markers present: 13-phase REA loop, byte sweep, 10
  languages, free services, human gate, skills/hooks/subagents/workflows/agent
  teams/auto-memory/doctor, role team + engines, autonomous bootstrap,
  capabilities/MCP/protocols, dashboard routes + 58 actions, social connections,
  chat widget, burger/cascading nav, instincts, access allowlist, run monitor,
  behaviour recordings, optional Composio, help pages, extra login providers,
  local analytics, paginator, browser-automation intents, Obsidian export,
  72 currencies.
- Repo clean and pushed. Project DB and vault notes current.

## Resolved in this pass

| Gap | Status | What now exists |
|---|---|---|
| P0-1 Backend bridge for real connections | **Built** | `app/bridge/server.py` — local-only, allowlisted, env-held secrets. Routes: `/health`, `/api/email/send` (SMTP), `/api/payments/checkout` (Stripe, requires per-transaction `confirm`), `/api/oauth/refresh` (token lifecycle), `/api/webhook`. Plus `client.js` forwarding the app's `pfv1:*` intents, `.env.example` and `README.md`. Verified: health, no-config responses, 404s and the payment gate all behave correctly. Missing keys never gate a feature. |
| P0-3 Automated tests / CI | **Built** | `npm test` (Vitest + jsdom), `app/tests/smoke.test.js`: **18 tests pass** covering roles/engines, all 10 languages and routing, role selection, free-by-default capabilities, human payment gate, MCP allowlists, 58 dashboard actions/surfaces and the byte sweep. `npm run build` still passes with 0 broken links. |
| P1-4 Automatic second-brain sync | **Built** | `scripts/sync_second_brain.py` — idempotent, cross-platform, standard library. Syncs project DB to the workspace `.hive/` copy, mirrors `obsidian-vault/` to `Documents\ObsidianVault\`, and writes `Work/SYNC_LOG.md` to both. `--check` dry-run supported. Verified applied. |
| P1-5 Token lifecycle | **Built** | Folded into the bridge: `POST /api/oauth/refresh` with `OAUTH_<PROVIDER>_*` env credentials and an allowlisted provider. |
| P1-8 Installable tools | **Installed** | `graphify` 0.9.118 (knowledge graph: 660 nodes / 863 edges / 39 communities; CLI, OpenCode skill + plugin, MCP registered), `yt-dlp` 2026.10.26, `faster-whisper` 1.2.1. `ffmpeg` was already installed. `demobase` and `basemode` do not exist as installable package/repo/skill (checked GitHub, npm, PyPI, skills.sh) — documented, not faked. |

## Still open

1. **Dashboard visual fidelity ~84%.** Rebuilt from text snapshots because the
   browser extension kept timing out; needs a fresh pixel capture at
   1440/768/390 px against `https://polsia.com/dashboard/pagemurmur-9jsvs1`.
   Blocked on a working browser bridge.
2. **Multi-user accounts / permissions backend (P1-6).** Guest/local workspace
   only. A real auth/teams service would need a database and identity provider;
   the local bridge is the foundation but this is not yet built.
3. **Real generated media / TTS (P1-7).** Capabilities are free local
   placeholders; live image/audio/video output needs provider keys routed
   through the bridge. No feature is locked meanwhile.
4. **Browser automation execution.** The app emits intents; a `browse` MCP
   bridge is needed to execute them. Same bridge pattern applies.
5. **Pending unidentified integrations (P1-8 remainder).** `cal.com`,
   `openproject`, `chatwoot`, `weknora`, `cap`, `voicestudio`, `openseo`,
   Higgsfield items, `calude x jev skill` — need repo/source identification or
   are too heavy for 8 GB RAM. Optional, not blockers.
6. **Legal / ToS review (P1-9).** Clean-room by design, but no formal review
   recorded. Human task.

## Not gaps (by design or outside the app)

- `demobase`, `basemode` — not real installable targets.
- BIOS is already `EMCN60WW`. RAM purchase, driver repair, Intel service
  demotion, remote-access decision and `repos/` review are **machine tasks**.
- The exposed `gho_hV2Y…` token still needs revoking on GitHub.

## Recommended order from here

1. Fresh dashboard screenshot + pixel refinement (needs browser bridge).
2. Execute browser-automation intents through a `browse` bridge.
3. Multi-user accounts/permissions on top of the local bridge.
4. Live media providers via env-held keys.
5. Human ledger: token revocation, RAM, services, remote-access decision.
