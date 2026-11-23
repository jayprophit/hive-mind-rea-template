# Gap analysis — Polsia Free v1

Date: 2026-11-23. Based on a fresh audit of `app/`, `dist/` and the repo.

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
- Repo clean at `67d36f7`, `0/0` with origin. Project DB and vault notes current.

## P0 — real gaps that block "finished"

1. **No backend bridge for truly live connections.** The app is a static site:
   it cannot hold OAuth client secrets, SMTP passwords or payment keys. Login,
   email send, payments, phone assistant and browser automation currently
   dispatch **intents** through the bus or use `mailto:`/local drafts. Calling
   them "live" means the configuration path is live, not that the network call
   happens from the browser. **Fix:** add a small Node/Python proxy that holds
   secrets in environment variables, exposes an allowlisted MCP/HTTP endpoint,
   and performs OAuth/SMTP/Stripe/browser actions. Then point the app's bridge
   at it. This is the single biggest remaining item.
2. **Dashboard visual fidelity** is ~84% and was rebuilt from text snapshots of
   the authenticated page, because the browser extension kept timing out and a
   fresh full-page screenshot was not captured. **Fix:** when `browse` is
   connected again, capture `https://polsia.com/dashboard/pagemurmur-9jsvs1`
   at 1440/768/390 px and refine panels against the pixels.
3. **No automated tests or CI.** The 13-phase engine, 10-language router and
   action bus have no Vitest suite, so self-modification could silently break
   them. **Fix:** add `npm test` with tests for phase order, loop-back, human
   gate, language routing and pagination.

## P1 — should be added for completeness

4. **Automatic second-brain sync.** Obsidian export is manual (download a
   `.md`). Add a script/watcher that writes the exported note into
   `obsidian-vault/Projects/` and refreshes the project DB after each round.
5. **Token lifecycle.** Nous access tokens expire quickly; the app has no
   refresh flow. Move provider credentials to the backend bridge above.
6. **Multi-user / accounts.** Only guest/local workspace exists; no real
   accounts, teams or permissions backend.
7. **Real media generation.** Image/audio/music/video and TTS are registries
   with local placeholders; live output needs provider keys via the bridge.
8. **Pending integrations** in `docs/INTEGRATIONS.md` need identification or
   installation: `ffmpeg`, `yt-dlp`, `whisper`/`openwhispr`, `cal.com`,
   `openproject`, `chatwoot`, `weknora`, `cap`, `remotion`, `basemode`,
   `scion`, `mononoke`, Higgsfield items. Some are optional/unknown.
9. **Legal/ToS review.** The REA work is clean-room by design, but no formal
   review of target terms has been recorded.

## Not gaps (by design or impossible here)

- `graphify`, `demobase`, `basemode` do not exist on this machine — optional/disabled.
- BIOS is already `EMCN60WW`; that task is done.
- RAM purchase, driver repair, Intel service demotion, remote-access decision
  and `repos/` review are **machine tasks**, not app gaps.
- The exposed `gho_hV2Y…` token still needs revoking on GitHub.

## Recommended order

1. Backend bridge for real connections (P0-1).
2. Fresh dashboard screenshot + pixel refinement (P0-2).
3. Vitest + CI smoke test (P0-3).
4. Automatic vault/DB sync (P1-4).
5. Provider token refresh moved to backend (P1-5).
6. Install/identify the pending tools that are actually needed (P1-8).
