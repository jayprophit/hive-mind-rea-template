# Defensive security, anti-tampering and quantum readiness — 2026-11-24

`app/src/security.js` (exposed as `window.PFV1_SECURITY`) adds defensive
coverage requested by the user. It is **strictly protective**.

## Coverage

- **Security goals:** confidentiality, integrity, availability, authenticity,
  accountability, non-repudiation.
- **Threat model:** STRIDE (spoofing, tampering, repudiation, information
  disclosure, denial of service, elevation of privilege) with a control for each.
- **Anti-tampering:** hash pinning, signed records, tool allowlists, sandbox by
  default, read-only evidence, audit trail, optional bridge token, allowlisted
  browser CLI calls with no shell interpolation. This protects **our own** data.
- **AI-specific risks:** prompt injection, data exfiltration, tool misuse,
  supply chain, model poisoning, autonomy drift, deepfake media — each with a
  control already present in the build (untrusted content as data, no secrets in
  logs, role allowlists, pinned versions, kill switch).
- **Red lines:** no offensive tools, no credential theft, no bypass of DRM or
  bot protections, no unauthorised access, no malware. These are explicit
  refusals, not features.
- **Quantum:** threat to RSA/ECC, post-quantum algorithms (Kyber, Dilithium,
  SPHINCS+), hybrid transition, QKD as hardware reference, quantum ML as
  research only, readiness checklist.

## What is deliberately absent
No exploit code, no scanning of systems the user does not own, no credential
harvesting, no evasion or persistence techniques, no "hack back". The user's
mention that AI can be used to attack systems is addressed by **defensive**
controls and refusal boundaries, not by building those capabilities.

## Honest limits
This is a reference layer, not a security audit or certification. The app has
no cryptographic keys of its own; bridge keys remain in the person's
environment. Quantum advantage claims are treated as research until verified.

## Verification
18/18 tests, build passes, 41 pages, 0 broken links.
