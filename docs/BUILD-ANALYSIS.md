# Build analysis and recommendations — 2026-11-24

Evidence: fresh `npm test`, `npm run build`, both link audits, the 27-point
requirement audit, Craft Anything's round-12 check, Playwright pixel diff, and
a source-size/registry count. This is a prioritised improvement list, not a
claim that everything is finished.

## Current state (verified)

| Measure | Result |
|---|---|
| Tests | 18/18 pass |
| Build | passes; 40 HTML pages, 1.1 MB `dist` |
| Links | 0 broken (23 HTML links, 41 JS path literals) |
| Requirement audit | 27/27 markers pass, 13 REA phases |
| Bridge | loaded on 40/40 pages |
| Craft Anything visual check | round 12, 99.69% overall; public pages 98.8–99.9%, phone width weakest |
| Dashboard pixel diff | 90.7% vs supplied `picture-1.png`; typography/positioning drift |
| Source size | `studio.js` 207 KB, `gaps.js` 48 KB, `dashhome.js` 31 KB; total 434 KB JS |

## P0 — do these first

1. **Fix the dashboard typography with measured values, not guesses.**
   The board geometry matches within ~2 px and glyph heights are ~29 px in both
   images, but words wrap differently and panels sit a few px off. Do a
   per-element measurement pass (font-size, line-height, margin, padding) using
   Playwright + PIL crops against `attachments/picture-1..6.png`, then lock it
   with a regression screenshot test. One earlier blind font-size change made
   the score worse (90.7 → 90.1) and was reverted — measurement is required.

2. **Add a Playwright visual regression suite to the repo.**
   Right now visual fidelity is only checked by Craft Anything interactively.
   Add `tests/visual.spec.js` rendering the 5 public pages and the dashboard at
   1440/768/390 and asserting a similarity floor. This prevents self-modification
   from silently degrading the design.

3. **Split `studio.js` (207 KB) into modules.**
   It is the single biggest maintenance risk. Extract the 13-phase engine,
   roster/registries, UI rendering and event wiring into separate files with
   explicit imports. Keep behaviour identical and re-run the 18 tests after each
   extraction. Target files under ~40 KB each.

4. **Add CI in GitHub Actions (free for public repos).**
   Workflow: `npm ci`, `npm test`, `npm run build`, both link audits, REA
   `--check`, then a Pages deploy of `dist/`. This makes the build reproducible
   without your laptop and matches the "run from GitHub + local/cloud split"
   decision in `DEPLOYMENT-ARCHITECTURE.md`.

5. **Close the loop on pending work before more features.**
   `docs/GROKBOT-TEAM-REA.md` and `docs/DEPLOYMENT-ARCHITECTURE.md` were
   uncommitted; the model registry was unreferenced. Commit/finish these first
   so the repo is a truthful record. Keep `craft.json` `ready` and one builder
   at most.

## P1 — high value, moderate effort

6. **Wire the model runtime registry into the team engine.**
   `app/src/models.js` now lists the same open-weight models for local Ollama
   and Cloudflare Workers AI (`qwen3:4b`, `gemma3:4b`, `deepseek-r1:7b`,
   `qwen3-vl:4b`, `nomic-embed-text`, `faster-whisper`, `edge-tts`, FLUX).
   Expose per-role engine selection from `ENGINES` without showing model names
   as teammates. Add a bridge `/api/models/health` that reports which runtimes
   are reachable.

7. **Adopt three Grok Bot patterns into the team model.**
   From `docs/GROKBOT-TEAM-REA.md`:
   - `BOT_ROLES` marketplace-style job descriptions (Sales Outbound, Talent
     Scout, Bug Reproduction, Chief of Staff, etc.) mapped to our role registry;
   - `ROOMS` + `@mention` routing and turn order on the shared bus;
   - **verification loop**: `tester`/`reviewer` must reproduce a failure and
     attach proof before `fix` closes it (matches field-notes rule).

8. **Give the solo business runner one front door.**
   The end vision is one runner doing plan → build → design → implement →
   amend → image/video/audio/music → email → phone. Add a `SOLO_WORKFLOW`
   registry that composes the existing 13-phase loop with the capability
   registry, so a single prompt can reach every capability. Keep `lead` as the
   only visible identity.

9. **Raise test coverage beyond the 18 smoke tests.**
   Add tests for: onboarding company creation (type + name → dashboard),
   payment invoice/crypto record generation, bridge allowlist rejection,
   human-gate re-ask, language routing between all 10 languages, and pagination.
   Current coverage is thin for 434 KB of source.

10. **Add a live bridge status indicator.**
    The bridge auto-detects `127.0.0.1:8787`, but the UI gives no feedback.
    Show a small "local bridge connected / local mode" badge in the studio and
    chat panel, with a button to copy the env template.

## P2 — quality and honesty

11. **Document unknowns explicitly.** Keep `evidence/rea/*.json` unknowns by
    offset; do not claim 100% *understanding* where we have 100% *accounting*.
    The curated REA evidence (`awesome-reverse-engineer-anything`) says REA
    helps on targeted questions, not open-ended exploration — use it that way.

12. **Finish the human ledger.** Revoke the exposed `gho_hV2Y…` token, fit the
    8 GB SODIMM, demote Intel telemetry services, decide remote-access autostart,
    review `repos/`. These are not app defects but they remain open.

13. **Formal legal review.** `docs/LEGAL-REVIEW.md` records the clean-room
    posture; a lawyer has not reviewed terms or look-and-feel.

## Suggested order

P0-1 → P0-2 → P0-3 → P0-4 → P1-6 → P1-7 → P1-8 → P1-9 → P1-10 → P2 items.

The app is functionally complete and clean; the remaining work is fidelity,
test depth, modularity and honest closure — not new feature breadth.
