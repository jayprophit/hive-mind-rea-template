---
type: project
date: 2026-11-23
project: "polsia free v1"
source: "app/tools.js"
database: projects/polsia-free-v1/knowledge.db
status: building
machine: "Lenovo IdeaPad 3 15IIL05 / 81WE"
---

# Polsia Free v1 — build tracker

## Where things live

| Item | Path |
|---|---|
| App source | `C:\Users\jpowe\Desktop\projects\polsia free v1\app\` |
| Built site | `...\app\dist\` |
| Project database | `projects/polsia-free-v1/knowledge.db` |
| Workspace copy of DB | `...\.hive\knowledge.db` |
| Template database | `data/knowledge.db` |
| Repo vault | `obsidian-vault/` |
| Local mirror | `C:\Users\jpowe\Documents\ObsidianVault` |
| Tools page | `/tools/` in the built app |

## Tracking

- The app's **Tools** page exports a Markdown note with frontmatter for this
  file, plus local analytics and the browser-action log. Drop it into
  `obsidian-vault/Projects/` to keep the build tracked across machines.
- The project SQLite DB stores one sha256 per source file, assets, runs and
  approvals. Rebuild with:
  `python scripts/build_index.py --root "<workspace>" --project --out projects/polsia-free-v1/knowledge.db`
- The template DB stays generic; this project has its own file.

## Capability state (audited)

All 38+ audited features are implemented: 13-phase REA loop, byte sweep, 10
languages, free services, human gate, skills/hooks/subagents/workflows/agent
teams/auto-memory/doctor, dashboard routes and actions, social connections,
chat widget, burger/cascading menus, role-only teammates with engines,
autonomous bootstrap, capabilities/MCP/protocols, instincts, access allowlist,
run monitor, behaviour recordings, optional Composio, help pages and extra
login providers. Section 5n tools were added directly to the single build:
browser automation intents, paginator, local analytics and Obsidian export.

## Known limits

- Visual likeness ~83%: long legal pages have drift; our own email form was
  designed because the original capture did not contain that field.
- Browser automation in a static page emits intents; a `browse` MCP bridge is
  required to execute them.
- `craft.json` must stay `ready` (not `paused` — that breaks project loading). Only one builder runs at a time.

## Gap pass — 2026-11-23

- **Backend bridge built** (`app/bridge/`): local-only, allowlisted, env-held secrets. Real SMTP email, Stripe checkout (per-transaction `confirm`), OAuth token refresh and report webhook. Client adapter forwards the app's `pfv1:*` intents. Missing keys never gate a feature.
- **Tests added**: `npm test` — 18 Vitest smoke tests covering roles/engines, 10 languages, free-by-default capabilities, human payment gate, MCP allowlists, 58 actions/surfaces and the byte sweep. Build still passes with 0 broken links.
- **Automatic second-brain sync**: `scripts/sync_second_brain.py` keeps the project DB, vault mirror and SYNC_LOG current after each round.
- **Tools installed**: graphify (knowledge graph, skill + MCP registered), yt-dlp, faster-whisper, ffmpeg. `demobase` / `basemode` do not exist as installable targets.
- **Dashboard rebuilt from the supplied screenshots**: four-column board with all 19 captured panels (including Routines, Website, Teams, Instagram, LinkedIn, Google Business, TikTok, YouTube Shorts, Pinterest, Facebook), black terminal strip, exact top bar and black chat bubble. Fixed the empty-`#dash-app` bug: the route loaded `dashhome.js` without calling `initDashboardHome()`. Verified in-browser: 59 controls, 4 columns, 19 panels.
- **Onboarding corrected**: `/new` no longer jumps to `/studio/`. It now streams the 46-line company provisioning log from a shared `provision-log.js`, saves the choice locally, then opens the dashboard. Verified end-to-end in-browser.
- **Foundation corrected**: the target is polsia.com itself, not the example company site. Removed hard-coded PageMurmur auto-creation. `companies.js` gives 7 business types and user-chosen name; `/new` asks type + name before provisioning; dashboard copy is generated from the chosen company. Verified end-to-end with "Northwind Goods / ecommerce".
- **Payments extended**: bridge now issues B2C/B2B/A2A/other invoices (PDF/HTML/JSON), receipts, Stripe/PayPal checkouts and Web3 (crypto) payment requests with wallet URI + QR; studio panel has mode/chain/wallet controls. All secrets are bridge env vars and every irreversible call needs per-transaction confirmation.
- **Skill-market analysis**: `docs/SKILL-MARKET-ANALYSIS.md` covers all eight requested marketplace/skill sites with counts, licences and relevant free tools.
- **Dashboard pixel diff**: supplied screenshots were found in `attachments/picture-1..6.png`; Playwright (system Edge) renders at 1668x925. Measured 90.7% similarity to picture-1; remaining drift is typography scale. Structural check (4 columns, 19 panels, 59 controls) passes.
- **Deep-dive gap pass (2026-11-24)**: 27-point requirement audit now reports 0 FAIL. Fixed: bridge client wired into all 40 served pages (plus chat on 6 static doc pages); real REA byte accounting with sha256 + 4096-byte ranges at 100% coverage on 11 artifacts (verified by `--check`); browser-action bridge endpoint with CLI allowlist; local STT/TTS/image/video endpoints (faster-whisper, edge-tts, Pillow, ffmpeg); local role-based multi-user accounts with permissions UI in the studio; clean-room legal posture documented in `docs/LEGAL-REVIEW.md`. Still open: numeric pixel diff, hosted identity provider, a few unidentified optional integrations, formal legal review, and the human ledger.

## Gap pass — 2026-11-24 (competitive research)

- **Research filed**: `docs/COMPETITOR-POLSIA-DEEP-RESEARCH.md` (business
  assessment 11 Nov + full gap/architecture research 24 Nov) and mirrored as
  `app/src/competitive-intel.js` (`window.PFV1_INTEL`). Reference only, no
  integration, no gates, no copied proprietary code.
- **Client-owned data**: `app/src/data-ownership.js` (`window.PFV1_DATA`) —
  local-first, user-chosen GitHub/cloud/Obsidian backups, six GDPR-aligned
  rights, export and erasure, no silent upload, secrets only in bridge env.
- **Optional connectors wired**: `app/src/connectors.js`, bridge
  `/api/connectors/status|call`, `pfv1:connectors-*` client events, plus
  `agent-platforms.js` landscape. Nothing enabled by default.
- **Verification**: 18/18 tests, build passes, 41 pages, 0 broken links,
  27/27 audit markers, Python bridge compiles. A real builder is active
  (round 22, 99.9% likeness), so `craft.json` stays `building` until it ends.
- **Graphify CLI currently fails silently** (exit 1, no output), so the graph
  could not be refreshed this pass; recorded honestly rather than claimed.

## Deep-dive pass — 2026-11-24

- **Authoritative analysis**: `docs/DEEP-DIVE-GAP-ANALYSIS.md`. Uses all research
  beyond the original site: 100-area registry, 12 benchmark targets, byte
  accounting, competitor architectures, connector/data-ownership layers.
- **Implemented this pass**: 100-area audit generator and report; contract
  intelligence pipeline + 6 tests; benchmark harness + report; visual regression
  suite (16 captures, dashboard 90.56% vs supplied screenshot); payment
  idempotency ledger + 2 Python tests; local Edge browser executor; budget
  ceiling guard + 4 tests; build snapshot/rollback; company namespace helper;
  graphify via `python -m graphify update .`.
- **Verification**: 28/28 tests, build passes with snapshot, 41 pages, 0 broken
  links, 27/27 markers, 0 FAIL; bridge modules compile; Python idempotency tests OK.
- **Only remaining blockers**: dashboard typography (builder tool consent),
  studio.js refactor, external OWASP audit, your keys/accounts/hardware, legal
  review. Nothing is hidden behind a percentage.

## Capability audit — 2026-11-24

`docs/CAPABILITY-AUDIT.md` answers every capability question with file evidence:
paper trading and local backtesting are LIVE; live trading is user-executor +
per-order confirmation only; browser automation, pagination and local analytics
are LIVE; public-page scraping is now LIVE via `/api/web/fetch`; REA framework
is LIVE but full autonomous reverse engineering is PARTIAL; exchange/fiat/crypto
and Web3 wallet are OPTIONAL/REFERENCE with no custody or key storage.

Added `runBacktest()` (4 tests), `/api/web/fetch` + `webFetch()` (4 Python
tests) and the browser `extract` tool. 32 JS + 6 Python tests pass.

The builder watcher is now `aut_20fd8e3db001rJFlKqKd661Qcv`, every 2 minutes,
restarting immediately with no idle window. `consent_required` is reported, not
worked around.

## Research extract + local AI human — 2026-11-25

- `docs/AETHERIUS-GENESIS-RESEARCH-EXTRACT.md` distils the two supplied full
  conversations: £0-first cost ladder, zero-surprise quota controller,
  service/provider registries with no credentials, logical directory tree,
  credential-broker guardrails, provisioning human gates and evidence states.
- `app/src/cloud-fabric.js` implements those guardrails locally: no network,
  no secrets, no feature gates; `quotaController()` pauses before any charge.
- `app/src/ai-human.js` + `/human/` page: free browser-only AI human with
  listen/speak/camera/avatar, local memory, interruption, explicit AI
  disclosure and human gates. Work requests go through `PFV1_SOLO.runTask`.
- Verification: 40/40 tests, build passes (42 pages), 0 broken links.
- Craft Anything was restarted by the user and is inspecting pages via the GUI.

## Open ledger

- Revoke exposed `gho_hV2Y…` token on GitHub.
- Fit 8 GB DDR4-2666 SODIMM; BIOS already EMCN60WW.
- Elevated demotion of Intel telemetry services; remote-access decision.
