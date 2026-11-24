# Capital, allocation and institutional methods — 2026-11-24

Added `app/src/capital.js` (`window.PFV1_CAPITAL`) as an educational reference
plus deterministic risk caps. It does **not** trade, pool client funds, or
promise returns. Paper mode remains the default in `treasury.js`.

## What is modelled

- **Allocation rules:** 10/90 barbell, 10/20/30/40 pyramiding, 1–2% risk rule,
  50/30/20 personal cash flow, 80/20 Pareto, 70/20/10 corporate treasury,
  3–6 month runway.
- **Strategy families:** mean reversion, trend/momentum, statistical pairs,
  grid, TWAP/VWAP execution, sentiment/event, LP fee farming, delta-neutral,
  options wheel, basis/carry, yield tokenisation.
- **Capital practices:** pay-yourself-first, sinking funds, DCA, Profit First,
  treasury sweeps, tax-loss harvesting, ring-fencing/SPVs.
- **Institutional methods:** smart order routing, factor investing, risk parity
  (ATR/vol sizing), yield-curve regime filter, **fractional Kelly only**.
- **Trader personas** (role patterns, not identities): statistical, global
  macro, market maker.
- **Copy trading** with a mandatory independent risk wrapper and source-wallet
  checks.
- **Overlooked edges:** maker rebates, honeypot/contract audit, walk-forward
  testing, Monte Carlo with slippage, oracle feeds, RPC redundancy.

## Rejected explicitly

| Method | Reason |
|---|---|
| Front-running | Manipulative and likely unlawful; harms other participants |
| Liquidity hunting (pushing price into retail stops) | Predatory |
| Dark-pool deceptive order display | Deception, not appropriate here |
| Using copy-traders as exit liquidity | Fraud-like; explicit warning in `COPY_TRADING.requiredChecks` |
| Full Kelly sizing | Too aggressive; quarter-Kelly cap instead |

## Hard caps

Max 2% account risk per trade, max 10% risk sleeve, 20% reserve, 6-month
runway, quarter-Kelly, walk-forward required, contract audit required before a
token buy. These sit outside the AI model.

## Honest note
The taxonomy is knowledge, not a licence. TradFi activity is regulated
(FCA/SEC, KYC/AML, tax); DeFi keeps the risk and removes the intermediary.
Nothing here guarantees returns, and client funds are never pooled. Verified:
18/18 tests, build passes, 41 pages, 0 broken links.
