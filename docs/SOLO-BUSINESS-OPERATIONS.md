# Solo business operations layer — 2026-11-24

`app/src/operations.js` (`window.PFV1_OPERATIONS`) pulls together everything the
user asked for into one operating layer for a solo AI-run business.

## Coverage

| User requirement | Implementation |
|---|---|
| Digital + physical products | `PRODUCT_TYPES`: digital (files, licences), physical (goods, POD, wholesale), service (milestones) |
| Delivery | `DELIVERY`: per-type checklists, tracking, receipt confirmation; IoT trigger as reference only |
| Quality | `QUALITY`: build/test/independent review/acceptance gates; failed work returns to board with proof and a different owner; no self-approval |
| Complaints | `COMPLAINTS`: received → triaged → investigating → response → resolved/escalated; 5-day SLA; refunds need a human |
| Compliance | `COMPLiance`: consumer law, UK GDPR, FCA reference, HMRC tax, platform terms; terms/privacy pages, invoices, audit trail, tax sinking fund, ring-fencing |
| Laws / regulations / rules | `LAWS_AND_RULES`: source hierarchy law > regulation > contract > platform > internal; conflicts logged and escalated |
| Consensus / governance | `CONSENSUS` (lead, role review, majority, quorum, human final) and `GOVERNANCE` (decision register, separation of duties, audit log, escalation, public `/live/` feed) |
| Smart contracts | `CONTRACT_WORKFLOWS`: escrow milestones, dynamic access, local DAO voting allowed as records; royalties and SSI reference-only; no chain execution |
| Human oversight | `GUARDRAILS`: no auto contracts, no client-fund custody, no guarantees, no legal advice, no auto refunds |

## Local state functions
`createOrder()`, `advanceOrder(id, state)` (refund/dispute require the gate),
`fileComplaint()`, `orders()`, `complaints()`. Every change goes through the
shared bus, so it appears in the team channel, the activity log and `/live/`.

## What this layer does NOT do
- Give legal, tax or financial advice.
- Hold client money or execute smart contracts.
- Guarantee returns or auto-approve refunds/disputes.
- Call courier, payment or KYC APIs without the person's own configured bridge.

## Verification
18/18 tests, build passes, 41 pages, 0 broken links.
