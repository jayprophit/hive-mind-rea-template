# Capability audit — what the build can actually do

Date: 2026-11-24. Every answer is tied to code that exists in
`C:\Users\jpowe\Desktop\projects\polsia free v1\app`. Classification:
- **LIVE** — working local implementation, backed by tests where stated.
- **OPTIONAL / HUMAN** — works only with a key, account, executor or approval you own.
- **REFERENCE** — registry or knowledge only; no external execution.
- **PARTIAL** — real code exists but the full goal is not met.
- **MISSING** — not implemented.

A registry entry is never presented as a working connection.

## 1. Direct answers

### Can it paper trade / practise and test strategies?
**Yes — LIVE, now including local backtesting.**
- `src/treasury.js paperTrade()` records simulated trades in local state; the
  bridge has `/api/trading/paper` with no keys needed.
- Six strategy families are registered (`trend`, `grid`, `dca`, `signal`,
  `mean-reversion`, read-only `arbitrage-scan`) with risk caps and a
  `BACKTEST_FIELDS` result schema.
- New `runBacktest({ prices, strategy, initial, fee })` runs a deterministic
  offline backtest over a supplied price series and returns net profit, trade
  count, win rate, max drawdown and an equity curve. It never places an order.
  Evidence: `app/tests/treasury-backtest.test.js`, 4 tests; 32 JS tests total.
- Market data sources are metadata only (public CoinGecko/Stooq patterns); no
  live feed is fetched by the app itself.

### Can it go from paper to live trading with real assets and money?
**Conditionally — OPTIONAL / HUMAN, by design not autonomous.**
- `liveOrder(order, confirm)` requires `confirm: true` **per order**.
- The bridge forwards the order to `TRADING_WEBHOOK_URL`, your own executor.
  With no executor configured it returns "not configured" and paper mode still
  works. The bridge never holds exchange keys, never settles and never claims
  an order filled.
- `RISK_LIMITS` caps allocation at 25%, daily loss stop at 5%, `neverBorrow`,
  and no auto-compounding without approval.
- **No custody, no KYC, no guaranteed returns, no commingling.** Real trading
  happens only in the user's own executor and wallet. This can help a business
  only if the strategy is actually profitable; no return is promised.

### Browser automation, pagination and data analytics?
**Yes — LIVE.**
- `src/tools.js BROWSER_AUTOMATION`: navigate, snapshot, click, fill,
  screenshot, extract, wait, walkthrough. Intents go through `pfv1:browser-action`.
- Bridge `/api/browser/action` executes an allowlisted tool via the `browse`
  CLI or a local Playwright/Edge fallback; screenshots are written under
  `bridge/records/browser`. No remote browser service or credentials.
- `createPaginator()` provides first/prev/next/last, keyboard navigation and
  `#page=` state.
- `collectAnalytics()` produces local workspace buckets and byte counts,
  rendered as an SVG bar chart, exportable to CSV and an Obsidian note. This is
  workspace analytics, not a hosted BI product.

### Can it scrape data from the internet or wherever needed?
**Partly before this audit; now YES for public pages — LIVE / bounded.**
- New bridge route `/api/web/fetch` reads a public http(s) page and returns
  title, visible text and absolute links. It refuses private/local addresses,
  credentials, non-text content, byte caps at 1 MB and times out at 15 s.
- `src/web.js webFetch(url)` is the page-side helper; event
  `pfv1:web-fetch` is wired in the bridge client.
- Browser `extract` was added to the allowlist and returns visible page text.
- `MCP_SERVERS` still lists a `fetch` server with `fetch_page`/`extract_links`
  as a registry entry only.
- **Limits:** no login/paywall bypass, no robots.txt or ToS violation, no
  authentication scraping, and facts must be verified at the original source.
  Evidence: `app/bridge/test_web.py`, 4 tests; `docs/COMPETITOR-POLSIA-DEEP-RESEARCH.md`.

### Can it reverse engineer anything to build something or an idea for a client?
**Framework YES / autonomous full REA PARTIAL.**
- A 13-phase REA loop with byte-by-byte sweeps, sha256 + offset evidence,
  acceptance criteria, gap records and source links exists in `src/studio.js`
  (`BYTE_SWEEP`, `REVERSE_EVIDENCE`, `reverseApi`, `startDeepResearch`).
- It can orchestrate a research/REA workflow and record evidence locally.
- It cannot independently disassemble arbitrary binaries, break DRM, or
  replace the connected Craft Anything/OpenCode tooling used to do the deep
  REA in this project. No proprietary implementation is copied.

### Can it connect to exchanges, fiat and cryptocurrencies?
**PARTIAL / OPTIONAL — registry + generic env-URL passthrough, no native rails.**
- `src/connectors.js` and `bridge/connectors.py` list Binance, Kraken, Coinbase,
  Bybit (CEX), MetaMask/WalletConnect/Phantom, Uniswap/PancakeSwap,
  marketplaces, KYC/legal and messaging connectors. Nothing is enabled by default.
- `call()` requires env-held keys and a user-supplied endpoint URL; sensitive
  actions (`order`, `send`, `submit`, `dispute`, `refund`) need `confirm: true`.
  There is **no native exchange API client** and no exchange SDK in the app.
- Fiat: Stripe/PayPal checkouts, invoices and receipts (PDF/HTML/JSON) via the
  bridge with per-transaction confirmation.
- Crypto: payment requests with wallet URI + QR; settlement happens in the
  user's own wallet or provider, never in this app.

### Does it have a meta wallet for Web3?
**PARTIAL — a wallet adapter and registry, not a wallet.**
- `connectWallet()` uses EIP-1193 `window.ethereum` to request an address and
  stores only `{kind, address}`. No private keys, seed phrases or signing in
  app state. Every wallet action is approved in the user's wallet.
- The registry includes MetaMask, WalletConnect, Phantom, Uniswap and
  PancakeSwap as optional, user-chosen connectors.
- There is no built-in multi-chain wallet, no transaction builder and no
  custody. That is intentional.

## 2. The rest of the checks

| Area | Status | Evidence / limit |
|---|---|---|
| Role-based team, 58 actions, engines | LIVE | `studio.js`, `registries.js`, 18 smoke tests |
| 10 languages, auto mode hours→years | LIVE | `studio.js LANGUAGES`, `routeLanguage` |
| Human oversight / authorise once | LIVE | `actions.js HUMAN_GATES`, `mechanisms.js approvalFor` |
| 13-phase REA loop + byte evidence | LIVE | `studio.js`, `scripts/rea_evidence.py` |
| Second brain: Obsidian + SQLite | LIVE | `scripts/sync_second_brain.py`, vault mirror |
| Optional bridge (email, payments, media, web, connectors, trading) | LIVE / OPTIONAL | `bridge/server.py` allowlisted routes; missing keys never gate |
| Client-owned backups and GDPR-aligned rights | LIVE | `src/data-ownership.js`, own repo/cloud needs your credentials |
| Competitive-intel and agent-platform registries | REFERENCE | `src/competitive-intel.js`, `src/agent-platforms.js` |
| Contract-intelligence pipeline | LIVE | `src/contract-intel.js`, source links, human go/no-go |
| Commerce / e-learning / fintech / contracts | REFERENCE | registries only; no marketplace keys or custody |
| Security, anti-tampering, quantum readiness | REFERENCE | `src/security.js`; not a security audit |
| Governance, privacy, compliance checklists | REFERENCE | `src/governance.js`; not legal advice |
| Budget ceilings | LIVE | `BUDGET_LIMITS` + `checkBudget()`, 4 tests |
| Local media STT/TTS/image/video | LIVE / PARTIAL | faster-whisper, edge-tts, Pillow/ffmpeg; provider-quality needs your key |
| Model engines: local + cloud pairs | LIVE (registry) | `src/models.js`, Ollama / Workers AI |
| MCP / A2A protocols | LIVE (envelope) + REFERENCE | `PROTOCOLS`, `MCP_SERVERS`; no hosted gateway |
| Monitoring / no-idle restart watcher | LIVE | `aut_20fd8e3db001rJFlKqKd661Qcv`, every 2 minutes |
| Tests, link audits, deep requirement audit | LIVE | 32 JS + 6 Python tests, 41 pages, 0 broken links, 27/27 markers |
| Formal 100-area audit and 12-target benchmark | LIVE | `docs/REQUIREMENT-AUDIT-100.md`, `docs/BENCHMARK-REPORT.md` |
| Visual regression | LIVE | `scripts/visual_regression.py`, 16 captures |
| Hosted identity / multi-device sync | MISSING | needs a free hosted instance you own |

## 3. Safety boundary

No MEV/front-running/sandwich, flash-loan arbitrage, guaranteed returns,
commingling of client funds, offensive security, DRM bypass, paid gates or
credits. No legal, tax or financial advice. No autonomous ad spend, bulk
unsolicited messaging, or irreversible action without a human gate. No
proprietary code, assets, branding or prompts were copied.

## 4. Verification of this pass
32/32 JS tests, 6/6 Python bridge tests, `npm run build` passes, 41 pages,
0 broken links (28 HTML + 42 JS literals), bridge modules compile, repo pushed.
