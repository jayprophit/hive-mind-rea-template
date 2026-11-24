# Smart-contract reference — 2026-11-24

Source: the smart-contract taxonomy supplied by the user. Public technology
overview, not a REA study.

## Two models

| | Permissioned / enterprise | Permissionless / public |
|---|---|---|
| Control | Company or consortium | Code / community |
| Benefit | Efficiency, cost reduction, auditability | Trustless, censorship-resistant, global |
| Speed/cost | High, fixed fees | Variable, gas fees |
| Mutability | Updatable, pausable, reversible | Typically immutable |

Examples: Hyperledger, R3 Corda (enterprise); Ethereum, Solana (public).

## Public-chain benefits
Trustless exchange, censorship resistance, composability (money Legos), global
access, DAO governance, fractional ownership/tokenisation.

## Enterprise benefits
Elimination of reconciliation, compliance/audit rules in code, instant
settlement (vs T+2), IoT-triggered supply-chain payments, automated back-office
tasks (claims, payroll).

## Cross-sector capabilities
Programmable royalties, self-sovereign identity, milestone escrow, dynamic
pricing/access.

## Build decision
`app/src/contracts.js` holds all of the above as `window.PFV1_CONTRACTS`
reference data. **Guardrails:** the app does not deploy contracts, sign
transactions or hold private keys. On-chain interaction requires the person's
own wallet, per-transaction approval and a contract audit first. No feature is
unlocked by a chain account. This is not legal or financial advice.

## Verification
18/18 tests, build passes, 41 pages, 0 broken links.
