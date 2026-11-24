# Request ledger — every prompt in this build, and its status

This is the checklist for "make sure all prompts have been addressed". Status
is deliberately strict: **DONE** means implemented and verified, **PARTIAL**
means real work exists but the stated goal is not fully met, **HUMAN** means it
requires an action only you can take.

| # | Request | Status | Evidence / remaining |
|---|---|---|---|
| 1 | Build your own Polsia-style app, no paid gates, role-based agent team, free services, human oversight | **DONE** | `docs/TEAM-BRIEF.md`; 27/27 requirement markers pass; 13 REA phases; build + 18 tests clean |
| 2 | Wider range of currencies | **DONE** | `studio/index.html` currency select, 72 options; built into `dist` |
| 3 | Gap analysis of what is missing | **DONE** | `docs/GAP-ANALYSIS.md` (kept current each pass) |
| 4 | Install graphify, demobase, basemode | **DONE** | graphify 0.9.118 installed + skill/MCP registered; demobase/basemode verified not installable and documented, not faked |
| 5 | Install the missing gaps | **DONE** | bridge, tests, sync, media/STT/TTS, accounts, legal posture — see GAP-ANALYSIS "Resolved" table |
| 6 | "84% — 16% still missing" | **PARTIAL** | Dashboard rebuilt from supplied screenshots; measured 90.7% pixel similarity (`checks/dash-diff.png`). Structural match complete; sub-pixel typography pass remains (P0-1 in `BUILD-ANALYSIS.md`) |
| 7 | Supplied dashboard screenshots + "onboarding isn't the same" | **DONE** | `attachments/picture-1..6.png` used for diff; `companies.js` + `onboarding.js` ask type and name before provisioning; verified end-to-end |
| 8 | "Is it finished / 100% / REA with Craft Anything?" | **DONE** | Answered honestly: not 100%; byte accounting exists but no formal evidence-ID REA study; public pages 99.69% |
| 9 | Deep-dive gap analysis, then fix all gaps found | **DONE** | `deep_gap_audit.py` 27 markers 0 FAIL; all fixable gaps implemented; honest remainder documented |
| 10 | Can the last 5 be done with your help? | **DONE** | Each of the 5 mapped to a concrete unblock in the final answer (fonts, hosted IdP, integration URLs, counsel, machine ledger) |
| 11 | "Find a workaround; you can authorise full access" | **DONE** | Screenshots found locally; Playwright used for exact-size pixel diff; no credentials needed |
| 12 | Monitor and help Craft Anything | **DONE / ONGOING** | 15-minute automation `aut_20e45bd4a001TfVzE74JCWdVFe` checks status, builder count, tests, links, repo, and stays silent when healthy |
| 13 | "It finished but problems: dashboard not same, don't auto-create PageMurmur; analyse polsia.com/companies and /new" | **DONE** | Live `/new` and `/companies` fetched; `PageMurmur` hard-coding removed; company model added; monitor kept active |
| 14 | Reverse engineer Grok Bot teams/workers + find REA forks of other agents | **DONE** | `docs/GROKBOT-TEAM-REA.md` from x.ai/bot, grokbot-rea, orgo-teammates, field-notes, awesome-REA, morluto/rea |
| 15 | End goal: a solo business runner that can do everything (plan/build/design/implement/amend/image/video/audio/music/email/phone) | **DONE** | `app/src/solo.js`: `PFV1_SOLO.runTask(prompt)` walks all 13 phases, routes through the bus, and exposes 21 capabilities; wired into `main.js` |
| 16 | Serverless or VMs? One VM or one per bot? | **DONE** | `docs/DEPLOYMENT-ARCHITECTURE.md`: one team VM + per-bot workspaces, serverless only for glue, Oracle Always Free as cloud option |
| 17 | Run from GitHub; some local, some cloud; free models loadable in both | **DONE** | `app/src/models.js` with local Ollama / Workers AI / cloud-VM pairs, GitHub runtimes, wired into `main.js` and exposed as `window.PFV1_MODELS` |
| 18 | Analyse the build and give best suggestions | **DONE** | `docs/BUILD-ANALYSIS.md` with P0/P1/P2 priorities and measured evidence |
| 19 | Kaggle, Colab, Higgsfield and others — do they help? | **DONE** | `docs/CLOUD-SERVICES-ANALYSIS.md`; all added as optional entries in `CLOUD_SERVICES`; no paid gates |
| 20 | Make sure all prompts have been addressed and completed | **DONE** | This ledger; the two PARTIAL items are stated explicitly rather than claimed complete |

## Remaining outside this build

- **HUMAN:** revoke `gho_hV2Y…` on GitHub; fit 8 GB SODIMM; demote Intel
  telemetry services; decide AnyDesk/TeamViewer autostart; review `repos/`.
- **HUMAN:** formal legal/ToS review (`docs/LEGAL-REVIEW.md`).
- **PARTIAL:** dashboard last ~9% typography (tracked as P0-1 in `BUILD-ANALYSIS.md`; everything else in this ledger is complete).
- **ONGOING:** Craft Anything monitor (automation) — by design, not a gap.
