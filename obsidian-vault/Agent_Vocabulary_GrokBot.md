---
type: vocab
date: 2026-11-09
supervisor: "bonsai-2:4b / @supervisor"
router: "laya"
grafana_dashboard: "http://127.0.0.1:3000/d/work-matrix"
---

# Grok Bot Terms & Skills — Added to Hive Mind

*Grok Bot Teams are the xAI equivalent of Hermes Bot Mode. Same pattern, different product words. All map to bots you already have.*

| Grok term | Hermes equivalent (what you have) |
|-----------|-----------------------------------|
| **Bot / Agent** | Hermes profile = `~/.hermes/profiles/<name>/` (isolated config/memory/skills/chat) — one process serves many profiles, `HERMES_HOME` scoped |
| **Team / Group Chat** | Hermes Bot Mode — 2-6 Bots, 3 serial rounds, `message_agent(target="@coder")` fire-and-forget |
| **Roster** | Hermes Bots pane — avatar, latest msg, unread, Activity now |
| **Routines** | Hermes cron `[bot:<name>] <routine>` — "summarize inbox 09:00" docked beside Bot Chat |
| **@mention** | `@coder hello` in any chat → composer autocomplete → teammate composes own message (your text never forwarded verbatim) |
| **Poll / Pin / Set Reminder** | Polls, pins, reminders = built-in tools in Hermes Bot Chat composer (`/poll`, `/pin`, `/remind`) |
| **Imagine** | `image.generate` plugin (FAL.ai / Replicate) — Hermes `image_gen_provider.py` |
| **Deep Search / Deeper Search** | `web_search` tool + `hermes research` skill — fan-out + adversarial verify |
| **Character / Personas / Rankings** | `SOUL.md` per Bot, `DEFAULT_SOUL.md` may be auto-written by Hermes |
| **Memory** | Hermes `MemoryProvider` ABC (`agent/memory_provider.py`) + FTS5 cross-session recall + LLM summarisation. `hermes memory index --force` |
| **Voice Mode** | `STT` local faster-whisper + `TTS` Edge TTS (free) — set `stt.enabled: true` |
| **Tasks / Scheduled tasks** | Hermes `cron` with delivery to Telegram/Discord/Slack/WhatsApp/Teams (~20 platforms) |
| **Kanban** | `kanban/` — multi-profile collaboration board, dispatch workers in worktrees |
| **Fleet / Swarm** | `kanban_swarm`, `delegation` plugin — ephemeral subagents per task |

## Skills added to Office suite (Grok parity)

- **Vibe Coding** — `/vibe` (persistent coding session)
- **Research Agent** — browser + web_search deep dive, returns cited report
- **Code Review Agent** — `/review-pr` checks diff, runs tests
- **PDF Cleanup Agent** — strips IDs/names from PDFs
- **Companion Agent** — personal assistant, memory notes
- **Imagine Agent** — image gen via FAL.ai
- **Researcher** — `websearch`/`my-mcp` database lookup

## How it maps

| Grok Bot term | Hermes Bot Mode |
|---------------|-----------------|
| Roster row (avatar + preview + unread) | Bots tab roster (same) |
| Group Chat rooms 2-6 bots | Group chats (msgs queued behind active room drive) |
| Rooms follow gateways, not one Desktop | Mirrored to shared profile metadata |
| @name / @hermes / @user / @all | Mentions read as identities, inline accent text |
| Compress history | Same `/compress` per member hidden session |

Update your Grafana `Work Tracking Matrix` with frontmatter `model_used: "bonsai-2:4b"` and `tokens_total` after each turn — same as before.
