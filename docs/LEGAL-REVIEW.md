# Legal / terms posture — Polsia Free v1

Date: 2026-11-24. This is an engineering posture record, **not legal advice**.
A qualified lawyer has not reviewed this project.

## Clean-room design (what the build actually does)

| Area | Posture | Evidence |
|---|---|---|
| Source code | Rebuilt from observed behaviour, captured text/design tokens and the person's own screenshots. No original source code was pasted into `app/`. | `capture/`, `samples/dashboard-evidence/`, `docs/REA-EVIDENCE.md` |
| Reverse engineering | Byte accounting records length, sha256, offset ranges and findings/unknowns. Opaque binary regions are accounted by range + hash and **not decoded**. No DRM circumvention was attempted. | `scripts/rea_evidence.py`, `evidence/rea/*.json` |
| Brand assets | The app uses its own `brand.svg` and generic shapes. No copied logos, photos or long passages of the target's text are embedded in `app/`. | `app/public/brand.svg`, source review |
| Fonts | Local/system fallbacks (Courier New, Times New Roman) stand in for the captured font families; no font binary was copied. | `app/src/styles.css` |
| Data / privacy | State stays in the browser's local storage. Optional bridge holds secrets only in environment variables on the person's own machine. No tracking cookies or cloud analytics by default. | `app/src/actions.js`, `app/bridge/` |
| Payments | Transactions use the person's own Stripe test/live key, require `confirm: true`, and never gate a feature. | `app/bridge/server.py` |
| Credentials | No secret is hard-coded. A previously exposed token remains a human action to revoke. | `docs/GAP-ANALYSIS.md` |

## Open items (honest)

1. **Formal ToS review not obtained.** The target site's terms were not reviewed by counsel. Whether observational reconstruction is permitted under those terms is an open question.
2. **Trademark / trade dress.** The rebuilt UI intentionally follows the observed layout. Commercial use of look-and-feel beyond personal use has not been cleared.
3. **Human-ledger item.** The exposed `gho_hV2Y…` token still needs revoking on GitHub — this is a security action, not a code gap.
4. **Provider terms.** Free-tier model providers (Nous, OpenCode free) and local Ollama have their own terms; the person is responsible for compliance when supplying keys.

## Conclusion

The engineering posture is clean-room with 100% byte accounting and no copied
proprietary code. The legal questions above remain **unresolved** and require
human review; they are not closed by this document.
