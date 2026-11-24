# Paid tiers for a public service — 2026-11-24

Context: Polsia Free v1 itself must stay free and ungated. Money comes from
**selling work the solo runner does for clients** (invoices, receipts, services),
not from locking features. All keys stay yours in the bridge environment.

## Rule before spending

1. Stay on free tiers until a real limit blocks paying work.
2. Prefer **metered pay-as-you-go** over fixed subscriptions while demand is unknown.
3. One provider per job, plus one fallback. Never subscribe to every tool at once.
4. Check commercial licensing of generated media before reselling it.

## Stage 1 — first paying clients (spend almost nothing)

| Need | Paid tier? | Why |
|---|---|---|
| Hosting / static site | No — GitHub Pages / Cloudflare free | Already working |
| Team VM | No — Oracle Always Free ARM (24 GB) | Enough for one team VM |
| Models | **Yes, metered** — one API key (Anthropic Claude, OpenAI, xAI Grok or Google Gemini) | Local Ollama covers routine work; pay only for high-quality client deliverables |
| Media | **Yes, credits** — Higgsfield for video/image when a client deliverable needs production quality | Local Pillow/SVG/ffmpeg is the free default |
| Payments | **Yes, fees only** — Stripe (and PayPal for consumer trust) | You already have invoice/receipt/crypto endpoints; fees are per transaction |
| Email | No — bridge SMTP / Resend free | Fine at low volume |

## Stage 2 — hundreds of users (upgrade these, in this order)

| Priority | Service | Tier | Why now |
|---|---|---|---|
| 1 | **Supabase Pro** (~$25/mo) | Auth + Postgres + Storage + Edge | Free limits hit; one service replaces several |
| 2 | **Cloudflare Workers Paid** ($5/mo + usage) | More requests, longer CPU | Serverless glue for webhooks, cron, routing |
| 3 | **Cloudflare R2** | Storage with cheap egress | Client deliverables and media at volume |
| 4 | **Resend Pro** (~$20/mo) or Postmark | Transactional email | Deliverability and volume |
| 5 | **Sentry / Grafana Cloud** | Error and uptime monitoring | You now have a reputation to protect |

## Stage 3 — mass adoption

| Need | Choice | Note |
|---|---|---|
| Agent runtime | Containers on Cloud Run / Fly.io / Hetzner, one team VM or per-bot workspaces | Scale horizontally; keep local hub as source of truth |
| Model routing | Two metered providers + local Ollama, chosen per task by `ENGINES` | Never show model names as teammates |
| Media pipeline | Higgsfield / Replicate / fal.ai per-use + local baseline | Pick by output quality and commercial licence |
| Payments | Stripe as primary, PayPal for consumers, BTCPay/Coinbase Commerce for Web3 | Already implemented in the bridge |
| Data | Supabase/Postgres with local SQLite mirror | Keep the vault and DBs synced |
| Support | Help centre, chat, ticketing (e.g. Slack/Telegram free→paid) | Human escalation for gates |

## What NOT to pay for early

- Fixed "Pro/Ultra" AI subscriptions for every model — use metered APIs instead.
- Multiple cloud VMs per bot — one team VM with isolated workspaces is enough.
- Paid marketplace/data exports — most catalogue data is free to browse.
- Any tier that gates a feature in Polsia Free v1 — that breaks the core rule.

## Commercial and legal cautions (important)

- The UI was reconstructed clean-room from observed behaviour, but a public
  commercial service resembling a target product carries **trademark and
  look-and-feel risk**. `docs/LEGAL-REVIEW.md` records the posture; a lawyer has
  **not** reviewed it. Get counsel before mass adoption.
- Generated media licences vary by provider and plan. Confirm you may resell
  outputs before putting them in paid deliverables.
- Provider ToS (xAI, Anthropic, OpenAI, Google, Higgsfield, Stripe) must be
  complied with; you are responsible for keys and costs.

## Decision

Start Stage 1: one metered model API, Higgsfield credits only for paid media
work, Stripe fees, everything else free. Upgrade in the Stage 2 order as real
limits appear. Revisit legal review before any public launch.
