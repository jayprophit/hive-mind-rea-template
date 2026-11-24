# Fintech models — CeFi, DeFi and hybrid (2026-11-24)

Source: the fintech taxonomy supplied by the user. Public market analysis, not
a REA study. These are optional contexts for the solo business runner; none is
a dependency and none unlocks a feature.

## Centralised fintech (CeFi)
Regulated institutions modernising existing rails:

- **Open Banking / instant payments** — third-party apps aggregate account data
  and initiate payments via API; no card-network fee.
- **Algorithmic credit scoring** — alternative data (cash flow, rent, utilities)
  for thin-file borrowers. Regulated lending needs authorisation.
- **Robo-advisors** — automated portfolio construction, rebalancing and
  tax-loss harvesting at lower cost.
- **Embedded finance** — lending, insurance and payments inside non-financial
  checkout flows.
- **RegTech / fraud detection** — ML anomaly detection, automated KYC/AML.
- **Fractional investing** — small increments of equities, property or bonds.

**Build fit:** our bridge already models env-held keys, SMTP, Stripe/PayPal,
invoices and receipts. We do not perform KYC, credit decisions or regulated
advice. Open Banking would be an optional OAuth integration, never required.

## Decentralised fintech (DeFi)
Smart contracts replacing intermediaries:

- **Permissionless access** — wallet + internet, no geography or credit file.
- **24/7 settlement** — seconds/minutes, no clearing windows.
- **Programmable composability** — "money Legos" stacked atomically.
- **Transparent ledgers** — real-time solvency verification.
- **AMMs** — pools replace order books.
- **RWA tokenisation** — treasuries, commodities and property on-chain.

**Build fit:** our crypto payment request (wallet URI + QR) and paper trading
cover the safe primitives. Self-custody means the user bears key risk; the app
never holds keys. Composability is recorded as knowledge, not auto-executed.

## CeFi vs DeFi (the real trade-off)

| | CeFi | DeFi |
|---|---|---|
| Custody | Regulated institution | Self-custody / keys |
| Intermediaries | Banks, processors, brokers | Smart contracts |
| Onboarding | KYC/AML | Wallet only |
| Protection | Statutory (e.g. FSCS) | Irreversible, user bears risk |
| Hours | Banking windows | 24/7 |
| Transparency | Periodic audits | Public real-time data |

## Emerging hybrid (CeDeFi)
- **Regulated stablecoins** — fiat-backed, licensed issuers.
- **Tokenised money-market funds** — on-chain shares of government debt.
- **ZK compliance** — prove KYC/accredited status without exposing personal data.

## Build decisions
1. Record all three models in `app/src/fintech.js` as `CEFI`, `DEFI`, `CEDEFI`
   and a `TRADEOFFS` matrix.
2. Add `PRINCIPLES`: no KYC performed by this app; no custody of user funds;
   no regulated advice; DeFi transactions are irreversible; optional
   integrations need the person's own keys.
3. ZK compliance is referenced as an emerging pattern, not implemented.
4. No feature is gated by a CeFi or DeFi account.

All of this is knowledge + optional connection paths, consistent with the
no-guarantee, no-commingling policy in `docs/FINANCE-GUARDRAILS.md`.
