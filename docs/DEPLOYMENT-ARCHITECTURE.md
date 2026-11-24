# Deployment architecture — solo business runner

Date: 2026-11-24. Decision record for how the team runs, with free defaults.

## Decision

**One team VM + per-bot sandboxed workspaces. Serverless only for glue.**

- Do **not** give every bot its own full virtual machine. Grok Bot's paid tiers
  sell that, but even Orgo Teammates shares one VM per account with up to four
  bot desktops active at once, sleeping idle ones. Our 8 GB Windows laptop
  cannot host four VMs; one VM with isolated workspaces can.
- Run the hub locally (shared bus, SQLite state, bridge, browser control) so the
  person's data, secrets and logged-in browser stay on their machine.
- Run bot desktops in one WSL2/Linux VM locally, or one Oracle Always Free ARM
  VM (4 cores / 24 GB, permanently free) in the cloud for 24/7 operation.
- Isolate bots with containers, separate OS users or separate working
  directories and browser profiles — not separate hypervisors.
- Use serverless only for stateless glue: OAuth callbacks, cron wake-ups,
  report webhooks and a public status endpoint.

## Topology

| Layer | Location | Notes |
|---|---|---|
| Team hub (bus, state DB, bridge, browser tools) | Local Windows machine | Local-first; no cloud required |
| Bot desktops | One Linux VM (local WSL2 or Oracle free ARM) | One VM for the team, many workspaces |
| Isolation | Containers / users / workdirs / browser profiles | Per-bot memory and skills stay separate |
| Serverless glue | Cloudflare Workers / GitHub Actions free | Short-lived, stateless only |
| Auth, DB, storage | Supabase / Firebase / Neon / Cloudflare R2 free | Optional; local SQLite is source of truth |
| Inference | Nous free, OpenCode free, local Ollama, Groq, AI Studio | No paid key needed to finish work |
| Payments | Stripe/PayPal with the person's own key | `confirm: true`; no feature gates |

## Free substitutes for paid tiers

| Capability usually paid | Free/open substitute |
|---|---|
| Own cloud computer per bot | Oracle Always Free ARM VM (24 GB), Google e2-micro, Codespaces 60 h/mo |
| Managed Postgres + auth + storage | Supabase / Firebase / Neon / Cloudflare R2 |
| Serverless compute | Cloudflare Workers (100k req/day), Vercel free, GitHub Actions |
| Email delivery | Resend 3k/mo, Brevo 300/day, own SMTP/bridge |
| Browser automation | Local Playwright + `browse` bridge (already in this build) |
| Observability | Grafana Cloud free, UptimeRobot, Sentry free |
| Models / inference | Nous free, OpenCode free, local Ollama, Groq, Google AI Studio |
| Messaging / meetings | Telegram, Discord, Matrix, Slack free; local STT/TTS for calls |
| Media generation | ffmpeg, Pillow, edge-tts, faster-whisper, Canvas/SVG (all local, already built) |
| Payments | Stripe/PayPal live with own keys; Web3 via own wallet/bridge |

## Honest limitation

Free tiers cannot match a paid per-bot GPU-backed cloud desktop 24/7. They can
provide one always-on 24 GB ARM machine plus local compute — sufficient for a
solo business runner doing research, planning, building, design, media, email,
phone assistance and reporting, with no locked features.

## Sources

- `docs/GROKBOT-TEAM-REA.md` — x.ai/bot product shape; `harsipsum/grokbot-rea`
  method; `nickvasilescu/orgo-teammates` shared-VM architecture;
  `unicodef1wn/grokbot-field-notes` operating rules.
- `docs/SKILL-MARKET-ANALYSIS.md` — free discovery/API sources.
- `app/bridge/` — local bridge holding env secrets, local media and payments.
