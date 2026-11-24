# Finance scope, guardrails and the "guarantee" question — 2026-11-24

## What this build does
`app/src/finance.js` (exposed as `window.PFV1_FINANCE`) is a **reference
taxonomy**: asset classes, mechanisms, strategies, platforms and infrastructure
from the four-pillar map supplied by the user. It also holds deterministic
guardrails that sit outside the AI model:

- kill switch, max drawdown 5%, slippage 0.5%, max position 10%
- simulation before broadcast
- human confirmation for every live order
- never borrow, never front-run, never flash-loan
- **no guaranteed returns, no commingling of client funds**

`orderAllowed()` checks these before any order proceeds. Paper mode remains the
default in `app/src/treasury.js`.

## Why there are no REA/Craft Anything forks for these niches
Searches for `rea flashbots mev`, `rea staking compounding defi` and
`simulation tenderly foundry transaction` returned **zero** repositories. The
general REA toolkit and Craft Anything cover the *method*; the *domain patterns*
come from the open-source projects already documented in
`TRADING-TREASURY-REA.md` (freqtrade, OctoBot, Superalgos, degenbot, AMM
arbitrage bots, LinkCharts, etc.). No dedicated finance REA fork was found.

## On banks, investment and "guarantees"

The user's observation is correct as a description of traditional banking:
banks lend/invest deposited money to earn a spread and can offer depositors a
return. But the important parts are the **constraints**, not the idea:

1. **Deposits are not risk-free.** Banks can and do fail; deposit insurance
   (e.g. FSCS in the UK) covers only a capped amount and is a government scheme,
   not a bank guarantee.
2. **Guaranteeing investment returns is not something a private operator can
   honestly promise.** If an investment can lose money, a guarantee is either
   backed by real capital and regulation, or it is misleading. Promising
   "guaranteed returns" to the public is a classic regulatory red flag and is
   associated with fraud/Ponzi schemes.
3. **Client funds must be segregated.** Using clients' money for the operator's
   own trading is a conflict of interest and, for regulated activities,
   unlawful without authorisation and disclosure.
4. **Regulation applies.** TradFi broking, fund management and taking deposits
   require licences (FCA/SEC and equivalents), KYC/AML, capital adequacy,
   suitability assessments and complaints/redress processes. DeFi removes the
   intermediary but not the risk, and keys are entirely the user's.

## Design decision
This app therefore **does not** pool client money, promise returns, or invest
on behalf of clients. It can:
- record paper trades and simulated performance locally;
- prepare an invoice/receipt for services actually delivered;
- show risk metrics and disclosures;
- forward a *person's own* confirmed order to *their own* executor.

It cannot claim a guarantee, and any UI copy must say "capital at risk, not
financial advice." If the user later wants a regulated investment product,
that needs a licensed institution, legal counsel and segregated custody —
not a code change here.

## Rejected mechanisms
MEV front-running/sandwich, flash-loan arbitrage, autonomous shorting,
autonomous compounding, commingling and guaranteed returns are all explicitly
excluded in `EXCLUDED`, with reasons.
