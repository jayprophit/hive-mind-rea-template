# Treasury / trading tool REA — 2026-11-24

Sources: the 14 repositories listed by the person, read via the GitHub API.
Licences matter: **GPL/AGPL code was not copied into `app/`**. Only behaviour
patterns were reimplemented in our own code.

## Repository findings

| Repo | Stars / licence | What it does | Use for this build |
|---|---|---|---|
| `gloom-sh/gloomberb` | 2,790 / MIT | Finance terminal in your terminal; market data, portfolio tracking | Pattern for a terminal-style market/portfolio view |
| `dakma-dev/gloomberg` | 32 / MIT | Proof of concept: live NFT transaction stream in a terminal or web UI, Ethereum | Pattern for read-only on-chain live events |
| `huggingface/smolagents` | 30,515 / Apache-2.0 | Barebones library for agents that think in code | Optional **code-thinking engine** pattern; add as an optional runtime, not copied |
| `paulrobertlloyd/barebones` | 646 / archived / no licence | HTML/CSS directory setup, style guide and pattern primer | Style-primer idea only; already covered by our theme tokens |
| `Fincept-Corporation/FinceptTerminal` | 34,181 / AGPL-3.0 | Market analytics, investment research, economic data, AI agents, algo trading | Research workflow pattern only; AGPL forbids copying |
| `freqtrade/freqtrade` | 57,231 / GPL-3.0 | Free crypto trading bot, backtesting, paper trading, strategies, Telegram | Paper-first execution and strategy metadata patterns |
| `freqtrade/freqtrade-strategies` | 5,681 / GPL-3.0 | Free trading strategies | Strategy families as metadata only |
| `ccxt/binance-trade-bot` | 8,838 / GPL-3.0 | Automated crypto trading | Exchange-abstraction pattern |
| `chrisleekr/binance-trading-bot` | 5,622 / Apache-2.0 | Pluggable strategies, backtesting, live dashboard, **agent over MCP** | MCP-connected trading agent — directly relevant to our `MCP_SERVERS` |
| `ctubio/Krypto-trading-bot` | 3,736 / unclear licence | Self-hosted HFT market making in C++ | Skipped: HFT complexity and unclear licence |
| `coding-kitties/investing-algorithm-framework` | 2,255 / Apache-2.0 | Quant development, backtesting, deployment framework | Backtest field pattern |
| `Drakkar-Software/OctoBot` | 6,982 / GPL-3.0 | AI/Grid/DCA/TradingView strategies, 15+ exchanges, paper trading | Strategy families (trend, grid, DCA, signal) |
| `Superalgos/Superalgos` | 5,820 / Apache-2.0 | Visual bot design, charting, data mining, backtesting, paper trading, multi-server | Visual strategy-design and paper-trading patterns |
| `spanoff/mega-arbitrade-flashbot` | 22 / no licence / stalled 2021 | "No code" flash-loan arbitrage, ETH/BSC | **Skipped**: unmaintained, no licence, risky "risk-free" claim, flash loans |

## What was added to the build

`app/src/treasury.js` (exposed as `window.PFV1_TREASURY`):

- **Paper mode by default** — simulated trades recorded locally, no exchange order.
- **Live orders require a separate `confirm: true`** for that transaction.
- `STRATEGIES`: trend, grid, DCA, signal, mean-reversion, arbitrage-scan (read-only).
- `EXCHANGES`: Binance, Coinbase, Kraken, Hyperliquid — each needs the person's own env keys.
- `RISK_LIMITS`: max allocation 25%, daily loss stop 5%, no borrowing, no auto-compounding without approval.
- `BACKTEST_FIELDS` and `MARKET_DATA_SOURCES` (free/public where available).
- `paperTrade()`, `liveOrder()`, `trades()` and an explicit risk disclaimer.

`app/bridge/payments.py` adds `/api/trading/paper` and `/api/trading/live`.
A live order is only forwarded when `TRADING_WEBHOOK_URL` points to the person's
own executor; with no executor it returns "not configured" and paper mode still
works. No feature is gated.

## Safety and honesty

- **Not financial advice. Trading risks capital.** No returns are promised.
- No flash loans, no automatic compounding, no autonomous live orders.
- Every live order re-asks, even if general autonomy is enabled.
- GPL/AGPL projects informed the design; none of their code is in this app.
- The flash-loan arbitrage project was deliberately rejected as unsafe/unmaintained.

## Verification
Paper trade recorded; no-confirm live order rejected with `tradingConfirm`;
no-executor live order returns `configured: false`. 18/18 tests, build, and both
link audits pass (41 pages, 0 broken links).
