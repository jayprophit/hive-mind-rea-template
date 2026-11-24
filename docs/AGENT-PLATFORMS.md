# AI agent platform landscape — 2026-11-24

Source: the platform list supplied by the user. Market reference, not a REA
study. `app/src/agent-platforms.js` exposes it as `window.PFV1_AGENT_PLATFORMS`.

## Centralised "company-in-a-box"
Polsia, NanoCorp, Willo, brainer.ceo, Cofounder (cofounder.co), Launchyard,
Sistava, Marblism, Vybe. They host infrastructure and agent loops, charge
subscription/fees, and differ on refunds, revenue share and approval gates.

## Decentralised / open-source
Virtuals Protocol, Olas/Autonolas, Fetch.ai (Agentverse), ElizaOS, CyreneAI,
Paperclip, Agent Zero. They emphasise self-custody, tokenised co-ownership,
on-chain revenue, agent marketplaces and self-hosted control planes.

## Trade-off
Centralised = no-code and fiat rails, but vendor fees/terms. Decentralised =
sovereignty and on-chain settlement, but wallets, tokens and technical setup.

## What we already cover (so these are not gaps)
Role team + swappable engines, 13-phase REA loop, human gate, A2A language,
decision register, audit log, public live feed, paper-first treasury,
per-transaction confirmation, self-hosted static app, free-first registries.

## One new pattern, deliberately reference-only
**Agent-to-agent labour commerce** (Olas/Fetch): agents offering and buying
discrete work from one another. It needs identity, a service catalogue, an
offer/accept protocol, settlement through person-owned keys and a reputation
record. We record it as knowledge (`AGENT_COMMERCE`, `allowed: false`) rather
 than executing autonomous economic contracts without legal and settlement
clarity.

## Decision
No competitor platform is wired in, no credentials or wallets are stored, and
no feature is gated by any of them. Verified: 18/18 tests, build, 0 broken links.
