# AI governance, privacy and compliance — 2026-11-24

Source: the AI-compliance taxonomy supplied by the user. `app/src/governance.js`
is exposed as `window.PFV1_GOVERNANCE`. Informational only — not legal advice.

## Coverage
- **Legal:** UK GDPR/ICO, EU AI Act disclosure, truth in advertising (ASA),
  IP/licensing of AI outputs, terms/privacy disclosure of AI processors.
- **Privacy:** never paste PII/client lists/financials/passwords/trade secrets
  into public models; prefer zero-retention business accounts; local-first
  state; `/live/` redaction.
- **Cyber:** verify unusual payment requests via a second channel, deepfake
  awareness, audit extensions, patch software, segment payment/OT hardware.
- **Quality control:** human review, fact-checking, code verification, labelled
  synthetic media, evidence for objective claims.
- **Internal governance:** AUP for new businesses, shadow-AI audit and
  retraining for established ones.
- **Checklist:** nine concrete actions, from terms disclosure to audit trails.

## Honest scope
Requirements depend on sector, region and clients. This is a reference layer,
not a certification. No feature is gated by it. Verified with 18/18 tests,
build passing and 0 broken links.
