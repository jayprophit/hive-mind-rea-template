# Rebrand and restyle plan

Written 2026-11-25. The user intends to rename the product and change
colours, UX and UI once the clone/rebuild work is finished. This is the safe
order of operations so the rename does not break tests, saved data or links.

## What is already easy to change

| Touchpoint | Where | Notes |
|---|---|---|
| Display name | HTML `<title>`, headers, footers, docs | ~37 source files, concentrated in `docs.js`, `studio.js`, `tools.js`, `dashhome.js` |
| Logo/favicon | `app/public/brand.svg` | single asset, referenced by every page |
| Theme colours | 8 CSS files, ~30 unique hex values in `styles.css` | tokenise before restyling |
| Storage keys | `pfv1_email`, `pfv1_lang`, `pfv1_provider`, `pfv1_human_v1` | needs a read-old/write-new migration |
| Bridge config | `PFV1_BRIDGE`, `PFV1_PAYMENTS_DIR`, `pfv1_bridge_config` | rename in `.env.example` and `bridge/` together |
| Package name | `app/package.json` → `polsia-free-v1` | also check lockfile |

Run `python scripts/rebrand_inventory.py "<app folder>"` before and after.

## Order of work

1. **Freeze the clone work.** Wait until Craft Anything is `ready` and the
   dashboard typography task is finished or dropped. Changing branding during
   a likeness round makes every score meaningless.
2. **Branch and snapshot.** Commit the current state; tag it
   `pre-rebrand`. Keep the clone commit reachable so the old look can be
   compared or restored.
3. **Tokenise before you restyle.** Move raw colours and font sizes into
   CSS custom properties (`--ink`, `--paper`, `--accent`, `--radius`,
   `--font-ui`, `--step-1..6`). Change values only after every page uses the
   tokens. This is what makes a colour change a 10-line diff instead of a
   30-file hunt.
4. **Rename display strings.** One pass over titles, headers, footers, docs
   and legal pages. Keep "Polsia" only where it is a factual reference to the
   competitor or the research (attribution must stay).
5. **Rename storage keys with migration.** Read `pfv1_*`, copy to the new
   prefix, then delete the old key. Never silently drop a user's language or
   provider choice.
6. **Rename env vars and package.** Update `.env.example`, bridge code,
   scripts and README in the same commit. Old env vars can be accepted as
   fallbacks for one release.
7. **Replace assets.** New `brand.svg`, favicon and any social image. Do not
   reuse third-party logos, screenshots or fonts you do not have rights to.
8. **Restyle.** Change tokens, spacing and type scale; keep the structural
   promises (4-column board, 19 panels, 59 controls) or update the tests and
   docs in the same commit that changes them.
9. **Regenerate visual baselines.** The 99.9% likeness is a clone score, not
   a design goal after rebranding. Capture new baselines at 1440/768/390 and
   treat drift from *those* as the regression signal.
10. **Re-verify.** `npm test`, `npm run build`, both link audits, the
    requirement audit and the visual suite. Update the ledger, vault and
    project DB.
11. **Human gates.** Trademark/company-name check, domain and TLS, legal/ToS
    review under the new name, and a check that no dependency licence or
    attribution was lost.

## What not to do

- Do not rename while a Craft Anything check round is mid-flight.
- Do not change the name in a way that implies endorsement by, or affiliation
  with, Polsia, Tavus, Aetherius or Genesis.
- Do not remove attribution from `docs/COMPETITOR-POLSIA-DEEP-RESEARCH.md`,
  `docs/AETHERIUS-GENESIS-RESEARCH-EXTRACT.md` or the benchmark reports.
- Do not let a colour change quietly alter contrast below WCAG AA; check the
  new palette before shipping.
- Do not reuse paid fonts, icon packs or stock assets without a licence.

## Owner-only items

- Final product name and trademark clearance.
- Domain, DNS and TLS.
- Legal review of the renamed terms, privacy notice and acceptable use.
- Choice of palette and brand direction (the code can implement it, but the
  taste is yours).
