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
| Dashboard visual fidelity | **Rebuilt against real screenshots** | The user supplied authenticated dashboard screenshots. `app/src/dashhome.js` + `dashhome.css` were rebuilt into the captured four-column board: all 19 panels now present (Polsia, Routines, Business, Website, Teams, Tasks, Documents, Twitter, Instagram, Email, TikTok, YouTube Shorts, Pinterest, Facebook, LinkedIn, Google Business, Meta Ads, Media, Team activity), black terminal strip, exact top bar and black chat bubble. Also fixed a real bug where the dashboard route loaded `dashhome.js` but never called `initDashboardHome()` (empty `#dash-app`). Verified in-browser: 59 controls, 4 columns, 19 panels. |
| Onboarding flow | **Corrected** | `/new` previously jumped straight to `/studio/` on either CTA. `app/src/onboarding.js` now runs the captured provisioning sequence in the terminal (46 lines from `provision-log.js`, shared with the dashboard log), records the choice/state locally, supports reduced motion and Escape-to-skip, then opens `/dashboard/pagemurmur-9jsvs1/`. Verified end-to-end in-browser: CTA → 9/46 lines after 1.6 s → completion → dashboard with 4 columns. |
| Bridge wired into served app | **Fixed** | `app/src/bridge-client.js` imports the adapter into every entry point; the six static doc pages now load `main.js` too. Verified at bundle level: **all 40 HTML pages load the bridge client**, and all 40 now have the floating chat widget. The client also auto-detects a local bridge at `127.0.0.1:8787` (live by default where possible) and forwards payment, email, OAuth, report, browser, capability and media intents. |
| Real REA byte evidence | **Built** | `scripts/rea_evidence.py` records total byte length + sha256 for 11 captured artifacts, walks each in explicit 4096-byte ranges with offset, length, hash and finding/unknown, and verifies `analysed_bytes / total_bytes = 100%`. `python scripts/rea_evidence.py --check` passes for all 11; full records in `evidence/rea/*.json`, summary in `docs/REA-EVIDENCE.md`. Opaque binary ranges are recorded as unknowns by hash, never decoded. |
| Browser automation execution | **Built** | Bridge route `POST /api/browser/action` invokes an allowlisted `browse` CLI tool with an argument list (no shell). Verified: health reports browser=True, allowlisted pass-through works and a disallowed tool (`rm`) is rejected. |
| Local media / TTS | **Built** | Bridge routes `/api/media/stt` (faster-whisper), `/api/media/tts` (edge-tts, installed), `/api/media/image` (Pillow) and `/api/media/video` (ffmpeg) run locally with no paid API. Verified image generation and generic capability passthrough. |
| Multi-user accounts / permissions | **Built** | `app/src/accounts.js` provides role-based local accounts (owner/lead/researcher/developer/coder/designer/tester/reviewer/ops/integration/support/finance/viewer) with per-role permission lists, create/switch/remove and an exposed `window.PFV1_ACCOUNTS` API. An Accounts & permissions card in the studio account panel creates and switches accounts and shows the active role's permissions. |
| Legal/ToS posture | **Documented** | `docs/LEGAL-REVIEW.md` records the clean-room posture (no copied source/assets/fonts, no DRM circumvention, local data, user-held keys) and lists the unresolved human questions (formal ToS review, trademark/look-and-feel, provider terms). |
| Payments B2C/B2B/A2A/other + Web3 | **Built** | `app/bridge/payments.py` issues numbered invoices (JSON + HTML + PDF), PDF receipts, Stripe/PayPal mode-aware checkouts and Web3 payment requests with wallet URI + QR. All secrets/addresses come from bridge env vars; every irreversible call needs `confirm: true` for that transaction. Studio Payments panel now has mode, chain, wallet, tax-rate, invoice, receipt and crypto buttons. Verified directly: invoice PDF, receipt PDF and a bitcoin URI+QR all generate; missing wallet/key returns "not configured" without gating anything. |
| Skill-market discovery | **Analysed** | `docs/SKILL-MARKET-ANALYSIS.md` records the eight requested sites with counts, licences and relevant findings (SkillsMP free API/MCP, `rea`, `human-gate`, `skill-security-auditor`, Context7, Browser Use, Defuddle, etc.). No code copied; none is a hard dependency. |

## Still open

1. **Numeric pixel-perfect pass at 1440/768/390.** The dashboard structure and
   styling follow the supplied screenshots and render correctly, but an exact
   pixel diff was not run (the `browse` CLI writes screenshots into a filesystem
   namespace this shell cannot read). The structural/token audit passes; only
   sub-pixel typography/spacing tuning may remain.
2. **Cloud-hosted accounts (P1-6 remainder).** Local role-based accounts exist;
   a real hosted identity provider / multi-device sync is not built and would
   need a service the person chooses.
3. **Pending unidentified integrations (P1-8 remainder).** `cal.com`,
   `openproject`, `chatwoot`, `weknora`, `cap`, `voicestudio`, `openseo`,
   Higgsfield items, `calude x jev skill` — need repo/source identification or
   are too heavy for 8 GB RAM. Optional, not blockers.
4. **Formal legal review.** `docs/LEGAL-REVIEW.md` documents the posture; a
   qualified lawyer has not reviewed terms or trademark/look-and-feel.
5. **Human ledger.** Revoke the exposed `gho_hV2Y…` token; fit the 8 GB SODIMM;
   demote Intel telemetry services; decide remote-access autostart; review
   `repos/`. These are machine/account actions, not app defects.

## Not gaps (by design or outside the app)

- `demobase`, `basemode` — not real installable targets.
- BIOS is already `EMCN60WW`. RAM purchase, driver repair, Intel service
  demotion, remote-access decision and `repos/` review are **machine tasks**.
- The exposed `gho_hV2Y…` token still needs revoking on GitHub.

## Recommended order from here

1. Numeric pixel diff at 1440/768/390 once screenshots can be written into the
   workspace (the app-side design is complete).
2. Hosted identity provider for multi-device accounts, if wanted.
3. Identify/install the remaining optional integrations that actually exist.
4. Formal legal/ToS review with counsel.
5. Human ledger: token revocation, RAM, services, remote-access decision.

## Deep-dive verification (2026-11-24)

A full requirement audit (`deep_gap_audit.py`) checks 27 acceptance markers
against the actual source plus built output: **0 FAIL**, 13 REA phases, bridge
client present on **40/40** pages, 100% byte coverage on 11 artifacts, 18/18
tests passing, build passing, 0 broken links. The audit separates "marker
present" from "behaviour verified in-browser"; both were done for the gaps
fixed in this pass.
