---
type: board
date: 2026-11-26
project: "polsia free v1"
status: live
generated: track_status.py
---

# Polsia Free V1 — live board

Generated from `work_items` in the project database. Edit
`data/board-polsia-free-v1.json`, then run
`python scripts/track_status.py`. Do not hand-edit this note.

Counts: active 2, next 3, blocked 4, owner 13, missing 4, done 23.

## Active now

| Area | Item | Detail | Evidence |
|---|---|---|---|
| build | Craft Anything builder — dashboard typography toward >95% | Builder round 31, 99.9% overall. Do not edit app/ while a builder runs. | `craft.json, checks/` |
| build | Watcher restarts the builder immediately, no backoff | Every 2 minutes; reports consent_required instead of working around it. | `aut_20fd8e3db001rJFlKqKd661Qcv` |

## Next — no user input needed

| Area | Item | Detail | Evidence |
|---|---|---|---|
| audit | Re-run requirement and benchmark audits after the next app change | Update docs/DEEP-DIVE-GAP-ANALYSIS.md, COVERAGE-AND-GAPS.md and REQUEST-LEDGER.md. | `scripts/build_requirement_audit.py, scripts/benchmark_targets.py` |
| brand | Execute the rebrand once the owner gives the new name | Follow docs/REBRAND-PLAN.md; migrate pfv1_* keys; regenerate baselines; re-verify. | `docs/REBRAND-PLAN.md` |
| code | Split app/src/studio.js into modules | Behaviour-preserving refactor after the builder is idle; keep tests green. | `app/src/studio.js` |

## Blocked

| Area | Item | Detail | Evidence |
|---|---|---|---|
| design | Raise dashboard likeness from 90.56% to >95% | Only typography may change; 4-column board, 19 panels and 59 controls must stay. Blocked by the Craft Anything app's own consent prompt. | `docs/DEEP-DIVE-GAP-ANALYSIS.md, craft.json` |
| research | REA ChatGPT public surface | Challenge page and 403 in a fresh private browser; nothing observed. Original equivalents stay reference-only. | `app/src/rea-targets.js OBSERVATIONS, docs/REA-AI-PLATFORMS.md` |
| research | REA Claude public surface | /new returned a challenge page and 403; nothing observed. No bypass attempted. | `app/src/rea-targets.js OBSERVATIONS` |
| research | REA DeepSeek public surface | Content-delivery error page; no chat surface observed. No bypass attempted. | `app/src/rea-targets.js OBSERVATIONS` |

## Owner-only — cannot be closed locally

| Area | Item | Detail | Evidence |
|---|---|---|---|
| accounts | Owner-owned provider, marketplace and wallet keys | Optional; missing keys never gate a feature. | `app/bridge/.env.example` |
| auth | Hosted identity provider | Local accounts work; hosted auth needs owner accounts and review. | `docs/LEGAL-REVIEW.md` |
| brand | New product name, domain and trademark clearance | Owner decision; then execute docs/REBRAND-PLAN.md. | `docs/REBRAND-PLAN.md` |
| code | Review repos/ and decide what to keep or publish | Owner decision; nothing deleted. | `repos/` |
| data | Remote backups | Owner accounts and cost/risk choice; local export already works. | `app/src/data-ownership.js` |
| design | Approve the Craft Anything consent prompt | rebuild_start returns consent_required; only the app's own consent click unblocks it. Never worked around. | `craft.json` |
| hardware | Elevated demotion of Intel telemetry services | Admin policy choice; no hardware or credential change made. | `machine audit` |
| hardware | Fit 8 GB DDR4-2666 SODIMM | One slot, 4 GB soldered; BIOS EMCN60WW. | `machine audit` |
| legal | Formal legal, terms and privacy review | Qualified human review; current pages are drafts. | `docs/LEGAL-REVIEW.md` |
| research | Permission for signed-in observation of the five platforms | Public pages can be observed now; anything behind a login needs the owner's own session and a terms check. No bypass. | `docs/REA-AI-PLATFORMS.md` |
| security | Independent OWASP agentic audit | Third-party assessor; cannot self-certify. | `docs/DEEP-DIVE-GAP-ANALYSIS.md` |
| security | Remote-access decision | Owner chooses whether any remote access is enabled. | `human-only ledger` |
| security | Revoke the exposed gho_hV2Y GitHub token | Only the account owner can revoke it; gho_XxIp is the working local token. | `human-only ledger` |

## Missing by design or hardware

| Area | Item | Detail | Evidence |
|---|---|---|---|
| human | Photoreal 720p real-time avatar | Not possible on this machine: i3-1005G1, 8 GB RAM, no Griffin-class GPU. The local canvas avatar is the honest fallback. | `machine audit, docs/AETHERIUS-GENESIS-RESEARCH-EXTRACT.md` |
| media | High-quality paid media provider route | Local STT/TTS/image/video exist; higher quality needs the owner's own key and explicit approval. | `app/bridge/server.py` |
| money | Native exchange SDK integration | Deliberately not built: generic env-URL connectors only; no custody or keys. Live trading needs the owner's executor. | `app/src/connectors.js` |
| site | Native mobile app | Not in the current scope; the site is responsive at 390 px and passes visual checks. | `scripts/visual_regression.py` |

## Done and verified

| Area | Item | Detail | Evidence |
|---|---|---|---|
| audit | 100-area requirement audit | 28 Verified, 57 Implemented, 2 Partial, 11 Reference, 1 Human, 1 Missing. | `docs/REQUIREMENT-AUDIT-100.md` |
| audit | 12-target benchmark harness | 3 Verified, 8 Implemented, 1 Unverified. | `docs/BENCHMARK-REPORT.md` |
| brand | Rebrand plan and read-only inventory script | Rename order, storage-key migration, baseline regeneration, legal gates. | `docs/REBRAND-PLAN.md, scripts/rebrand_inventory.py` |
| core | 13-phase REA loop, 10 languages, role/engine registries | Byte accounting with sha256 and 4096-byte ranges at 100% coverage on 11 artifacts. | `app/src/main.js, registries` |
| core | Local bridge with allowlisted routes | SMTP, Stripe/PayPal, invoices, OAuth, browser, media STT/TTS, connectors, web fetch; secrets only in env. | `app/bridge/server.py` |
| data | Client-owned data and GDPR-aligned rights | Local-first, user-chosen backups, export and erasure, no silent upload. | `app/src/data-ownership.js` |
| human | Local AI human at /human/ | Listen, speak, camera, canvas avatar, local memory, interruption, explicit AI disclosure, human gates. | `app/src/ai-human.js, app/human/index.html` |
| infra | Cloud-fabric guardrails: cost ladder, quota controller, no secrets | Local/self-hosted first; pauses before any charge; provider registry holds no credentials. | `app/src/cloud-fabric.js` |
| money | Paper trading and local backtesting | Live trading only via the owner's webhook with per-order confirmation; no custody. | `app/src/treasury.js` |
| money | Payment idempotency ledger and budget ceiling guard | Irreversible calls need per-transaction confirmation; hard spend limit zero by default. | `app/bridge, app/src/governance.js` |
| quality | 0 broken internal links | 28 HTML links and 42 JS path literals checked. | `%TEMP%/opencode/audit-links.py, audit-js-links.py` |
| quality | 40 JS tests passing | Vitest suite covering roles, languages, gates, budget, contracts, human and fabric. | `app/tests` |
| quality | 6 Python bridge tests passing | Idempotency and web-fetch tests. | `app/bridge/tests` |
| quality | Visual regression suite, 16 captures at 1440/768/390 | Public pages 100% vs baseline; dashboard 90.56% vs attachments/picture-1.png. | `scripts/visual_regression.py` |
| research | Aetherius/Genesis research extract | Attributed; no code, assets or prompts copied. | `docs/AETHERIUS-GENESIS-RESEARCH-EXTRACT.md` |
| research | Public-page reader and browser automation | Respects access controls; no bypass. | `app/src/web.js, bridge` |
| research | REA Kimi public surface | OBSERVED: public app shell with chat, projects, plugins, scheduled, research, docs, build etc.; modes mapped to local originals, no login used. | `app/src/rea-targets.js OBSERVATIONS, MODE_EQUIVALENTS` |
| research | REA Manus public surface | PARTIAL: /app redirected to login; signed-out framework shell only. Durable task record stays a local original. | `app/src/rea-targets.js OBSERVATIONS` |
| research | REA registry for ChatGPT, Claude, Manus, DeepSeek and Kimi | Public-surface scope, 11-phase plan, legal guardrails, evidence states and 5 tests; nothing observed or copied yet. | `app/src/rea-targets.js, docs/REA-AI-PLATFORMS.md` |
| site | Public site and dashboard, 42 built pages | Five public pages at 99.9% likeness and must not change. | `app/dist` |
| site | Visible /rea/ findings page | Observation cards, evidence ids, mode equivalents and guardrails rendered from the registry; no shared nav or public-page styling changed. | `app/rea/index.html, app/vite.config.js` |
| tooling | Knowledge graph refreshed | Use python -m graphify update . | `graphify-out/` |
| tracking | Work items tracked in the project database | work_items table generated from board.json; vault board generated from the same data. | `scripts/track_status.py, projects/polsia-free-v1/board.json` |

## Rules that keep this honest

- Free/open-source by default; paid only with the owner's own keys and
  explicit approval. No gates, credits or subscriptions.
- No claims of consciousness, guaranteed returns, or a self-trained model
  where none exists.
- Human gate for sensitive/irreversible actions; secrets only in bridge env.
- Research and competitor material stays attributed; no copied proprietary
  code, assets, branding or prompts.
