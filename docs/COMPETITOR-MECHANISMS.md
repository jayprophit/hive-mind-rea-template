# REA of Polsia alternatives — mechanisms added 2026-11-24

Sources: NanoCorp "What is Polsia", Willo vs Polsia, Baljia alternatives,
Launchyard comparisons, Sistava comparison, Vybe cofounder comparison, and the
PolsiaAI GitHub README. These are competing vendors' pages; claims are attributed
to them, not assumed true. No competitor code, assets or prompts were copied.

## Mechanisms found

| Mechanism | Seen in | Implemented here |
|---|---|---|
| Public live activity feed / live counter | Polsia `/live`, NanoCorp live feed | `LIVE_FEED`: static local-bus feed, hides secrets, `/live/` path reserved |
| Public revenue dashboard | NanoCorp | Local analytics + bridge payment records; no cloud tracking |
| Company directory / unlimited businesses | NanoCorp, Polsia multi-company | `FLEET` (up to 12 local companies, isolated state namespaces) |
| Decision Register with reasoning | Willo | `DECISION_REGISTER.record/list` in `mechanisms.js` |
| Approval levels (plan / ask / auto) | Teammates.ai, Sintra, Baljia | `APPROVAL_LEVELS` + `approvalFor()`; sensitive actions always ask |
| Free fixes / refunded retries when the agent breaks something | Launchyard Policy | `RELIABILITY_POLICY` + `freeFix()`: repair logged as free fix, different owner retry |
| Per-business data isolation | Willo (RLS) | Per-company local state namespaces (not hosted RLS) |
| Nine fixed agent roles sharing memory + MCP | Polsia | Our 58 role registry, `AUTO_MEMORY`, `MCP_SERVERS` already cover this |
| Self-improving skills | Polsia, Vybe | `SKILLS`, `skill-retro` pattern, retrospective already present |
| Agents build custom internal apps | Vybe | `CUSTOM_APP_TEMPLATES` (deal board, content calendar, invoice list, task queue) |
| SOC2 / SSO / RBAC / audit logs | Vybe | RBAC + audit log present; SSO optional via `LOGIN_PROVIDERS`; **SOC2 false, not claimed** |
| Multi-campaign Meta Ads | Launchyard | `AD_CAMPAIGNS` model; real delivery needs your own key via bridge |
| AI co-founder that pushes back | Polsia README | `COFOUNDER_PERSONA` rules tied to acceptance criteria and proof |
| Credit add-ons, 3% payment fee, 20% ad fee, 31-day payout | Polsia terms (per competitors) | Deliberately absent: no credits, no revenue share, no feature gates |
| Data export before leaving | switch guides | `EXPORT_CHECKLIST` + existing Obsidian/JSON/git exports |

## What we deliberately do NOT copy

- Revenue share, withdrawal fees or credit packs — the brief forbids paid gates.
- "Autonomy theater" counters — our activity log records real dispatched actions.
- Claims of SOC2/enterprise certification without the organisational work.
- Vendor pricing or marketing copy.

## Verification

`app/src/mechanisms.js` is imported by `main.js` and exposed as
`window.PFV1_MECHANISMS`. Build and tests must stay green; the registry is
additive and changes no existing behaviour.
