# Coverage and gap audit — after all supplied prompts

Date: 2026-11-24. Strict classification:
- **LIVE** = implemented, verified in build/browser
- **REFERENCE** = registry/knowledge only, no external execution
- **HUMAN** = needs you or a qualified third party
- **MISSING** = real gap in the build

## 1. Verified build state (last full check)
18/18 tests, `npm run build` passes, 41 HTML pages, 0 broken links
(28 HTML links + 42 JS path literals), 13 REA phases, 27/27 requirement
markers pass, bridge client on 40/40 pages, `craft.json` `ready`, ≤1 builder.

## 2. Domain coverage

| Domain | Status | What exists / what is missing |
|---|---|---|
| Polsia UI + 5 doc pages | **LIVE** | Public pages 99.9% Craft Anything likeness |
| Authenticated dashboard | **LIVE / PARTIAL** | 4 columns, 19 panels, 59 controls; pixel similarity ~90.7% vs supplied screenshots — typography pass outstanding |
| Onboarding / company choice | **LIVE** | Business type + name chosen before provisioning; no hard-coded example company |
| 13-phase REA loop, 10 languages, role team | **LIVE** | Data-driven engine, bus, selection, approvals, metrics |
| Byte-accounting evidence | **LIVE** | 100% coverage on 11 artifacts; no evidence-*ID* REA study |
| Tests / CI | **PARTIAL** | 18 smoke tests; **no visual regression suite** in repo; CI validates repo only, not app (app lives outside repo) |
| Bridge (email/payments/media/browser) | **LIVE / OPTIONAL** | Allowlisted, env secrets; auto-detect local; **no provider keys supplied by user** |
| Payments B2C/B2B/A2A/Web3 | **LIVE** | Invoice/receipt PDF, Stripe/PayPal, crypto URI+QR; settlement needs your executor |
| Solo runner front door | **LIVE** | `PFV1_SOLO.runTask()` walks 13 phases + 21 capabilities |
| Second brain (Obsidian + DBs) | **LIVE** | Auto-sync script, vault mirror, project DB |
| Model runtimes | **LIVE (registry)** | Local Ollama / Workers AI pairs; GitHub free tiers; no keys needed |
| Multi-user accounts | **PARTIAL** | Local role-based accounts + permissions; **no hosted IdP / multi-device sync** |
| Media generation | **PARTIAL** | Local SVG/Pillow/ffmpeg/edge-tts/faster-whisper; no provider-key route for high-quality output |
| Browser automation execution | **PARTIAL** | intents emitted + bridge CLI allowlist, but `browse` relay path unreliable |
| Treasury / trading | **REFERENCE** | Paper-first trades, risk caps, strategies, human-gated live orders; **no exchange API connected** |
| Finance/fintech/capital/smart contracts | **REFERENCE** | Taxonomies + guardrails; no KYC, custody, deployment or regulated activity |
| Commerce / e-learning platforms | **REFERENCE** | Platform metadata; no marketplace credentials or course content |
| Security / anti-tampering / quantum | **REFERENCE** | Defensive controls, STRIDE, red lines, PQC readiness; **not a security audit** |
| AI governance / compliance | **REFERENCE** | GDPR/AI Act/ASA/IP/AUP checklist; **not legal advice** |
| Solo business operations | **LIVE (local) + REFERENCE** | Orders, complaints, quality gates, governance records; no courier/KYC APIs |
| Monitor | **LIVE / ONGOING** | 15-min automation, silent when healthy |

## 3. P0 — real gaps that could still be closed

1. **Dashboard typography (PARTIAL).** ~9% pixel drift. Needs a measured
   per-element pass (font-size, line-height, margin) against
   `attachments/picture-1..6.png`, then a locked regression screenshot.
2. **Visual regression in repo tests (MISSING).** Add Playwright assertions for
   the 5 public pages + dashboard at 1440/768/390 with similarity floors.
3. **Studio.js monolith (MISSING refactor).** 207 KB single file is the biggest
   maintenance risk; split into engine/UI/wiring modules with behaviour intact.
4. **Hosted identity (MISSING).** Local accounts only; multi-device sync needs a
   free Supabase/Auth0 instance you create.
5. **High-quality media provider route (MISSING).** Local placeholders work;
   FLUX/Higgsfield-style output needs your own key via the bridge.
6. **Browser relay reliability (MISSING).** `browse` CLI writes screenshots to
   an inaccessible path; local Playwright works but isn't wired to the app's
   browser-automation intents as a default executor.

## 4. Human-only (cannot be done here)
- Revoke exposed `gho_hV2Y…` token on GitHub.
- Fit 8 GB DDR4-2666 SODIMM; Intel service demotion; remote-access decision;
  `repos/` review.
- Formal legal/ToS/compliance review and any regulated activity.
- Provider keys, marketplace accounts, exchange keys, wallets — all yours.

## 5. Deliberate exclusions (not gaps)
MEV/front-running/sandwich, flash-loan arbitrage, autonomous shorting,
guaranteed returns, commingling client funds, offensive security tools, DRM
bypass, paid feature gates. Rejected by design with documented reasons.

## 6. Honest answer to "have we covered everything needed?"
**No.** We have far surpassed the original Polsia concept in breadth — 13-phase
REA, 10 languages, role team, payments, commerce/learning/finance/security/
governance references, solo runner, observability — but three things remain:
(a) the dashboard's last ~9% visual fidelity, (b) test/refactor depth, and
(c) anything requiring your keys, accounts, hardware or a lawyer. Everything
reference-only is honestly labelled and never presented as a live connection.

## 7. Recommended order
1. Dashboard measured typography pass + visual regression suite.
2. Split `studio.js` into modules.
3. Wire local Playwright as the browser-automation executor.
4. Add hosted auth only if you want multi-device accounts.
5. Add provider keys only where you actually need high-quality media or live
   payments — never as gates.
6. Work the human ledger.
