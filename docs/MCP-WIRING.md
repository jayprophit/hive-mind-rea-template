# Craft Anything ↔ agents (MCP wiring)

This is the fix for the failure that looks like **"the agent sits there for 15
minutes and nothing happens"**. It is almost never the MCP server. Check the
provider first.

## What actually happened (2026-11-23)

Craft Anything's builder was configured to use Hermes Agent. Records from
`build-activity.log` and `%LOCALAPPDATA%\hermes\logs\agent.log`:

| Time | Event |
|---|---|
| 06:01:43 | Builder run starts |
| 06:12:09 | `custom didn't respond in time on any of 3 attempts` — the local provider at `127.0.0.1:11434` was **not running** |
| 06:12:17 | Hermes exits 2, `0 tokens in / 0 out` |
| 06:12:49 | Craft Anything retries automatically |
| 06:21:33 | `Gateway disconnected` — the run was killed while waiting |
| 06:29:19 | Retry again; a second 9,096-character session competes with the first |
| 06:33:24 | Same error; loop continues every ~90 s |

Two independent causes, both fixed:

1. **Provider down.** Ollama had been stopped to free RAM. Hermes' `model.provider:
   custom` points at `http://127.0.0.1:11434/v1`, so every call failed.
2. **Wrong model for an agent.** `bonsai-2:4b` has `TEMPLATE {{ .Prompt }}` — no
   chat template. Measured: **57.7 s and ~200 hidden tokens to answer "OK"**, and
   empty content below 64 tokens. `laya` returns HTTP 400 on chat completions.

MCP itself was never broken: `hermes mcp test craft-anything` reports
**38 tools discovered**, and `hermes mcp list` shows it enabled.

## Use the preflight before every build

```powershell
# checks CLI, MCP handshake, OpenCode config, Hermes config, provider,
# and runs a real model smoke test
.\tools\agent-preflight.ps1 -StartProvider

# wiring only, no model call
.\tools\agent-preflight.ps1 -Quick

# machine-readable
.\tools\agent-preflight.ps1 -Json
```

Exit code `0` = safe to start the agent. `1` = at least one FAIL, with the exact
fix printed. A model that replies with empty content or takes > 60 s for "OK" is
flagged: long build prompts will be far worse.

## (Re)wire any agent

```powershell
.\tools\wire-craft-anything.ps1 -DryRun          # show changes
.\tools\wire-craft-anything.ps1 -Agent opencode,hermes
.\tools\wire-craft-anything.ps1 -Force           # replace an existing entry
```

The script is idempotent and writes a timestamped backup before editing
OpenCode's JSON. For agents it does not know, it prints the exact command.

### Per-agent configuration

| Agent | Where | Entry |
|---|---|---|
| OpenCode | `~/.config/opencode/opencode.json` | `mcp.craft-anything = { type: "local", command: ["<cli>", "mcp"], enabled: true }` |
| Hermes | `hermes mcp add craft-anything --command "<cli>" --args mcp` | managed by `hermes mcp list/test` |
| Claude Code | `claude mcp add craft-anything -- "<cli>" mcp` | user scope |
| Codex CLI | `codex mcp add craft-anything -- "<cli>" mcp` | user scope |
| Gemini CLI | `~/.gemini/settings.json` | `mcpServers.craft-anything = { command, args: ["mcp"] }` |
| Cursor / Windsurf / VS Code | their MCP settings JSON | same command/args |
| Anything else | stdio MCP client | command = CLI path, args = `["mcp"]` |

The CLI path is normally:

```
C:\Program Files\Craft Anything\craft-anything-cli.exe
```

## Model capacity rule

The builder prompt is ~9,000 characters plus Hermes' system prompt and 38 tool
schemas. That is a large prefill for a CPU-only 8 GB laptop.

| Model | Size | Measured on this laptop | Verdict |
|---|---|---|---|
| `bonsai-2:4b` | 1.6 GB | 57.7 s for "OK"; empty below 64 tokens; no chat template | **Do not use as an agent** |
| `laya:latest` | 0.84 GB | HTTP 400 on chat completions | Router only |
| `lfm3:1.7b` | 1.1 GB | "OK" in 15.8–20.8 s; real turn: 2,050 in / 34 out in 46.3 s | **Best available locally** |
| any 7B+ | 4 GB+ | does not fit comfortably beside Chrome + WSL on 8 GB | Desktop only |
| cloud provider | — | sub-second to a few seconds | **Recommended for agentic builds** |

`hermes config set model.default lfm3:1.7b` is the local fallback. On a desktop
with 16 GB+ and a GPU, a 7B–14B model is the right local choice. For multi-step
builds, a cloud provider is faster and more reliable than any local model on
this laptop.

## Concurrency rule

Do **not** run two Hermes one-shots at the same time (Craft Anything's builder
plus a manual `hermes -z ...`, or two Craft Anything retries). They share one
gateway; the second one produces `Gateway disconnected; turn outcome is unknown`.
Craft Anything retries automatically every ~90 s, so a failed build can keep
colliding with itself.

Before starting a manual test, confirm no builder is running:

```powershell
Get-Process hermes -ErrorAction SilentlyContinue
```

## Memory rule

Ollama is Tier 2: it is stopped at boot to save commit charge, and started on
demand. Hermes needs it. So the order is:

```powershell
.\tools\agent-preflight.ps1 -StartProvider   # starts Ollama and waits
# ... run the build ...
Stop-Process -Name 'ollama app','ollama' -Force   # reclaim ~3.6 GB when done
```

Never stop Ollama while a Craft Anything build is running.

## Failure signatures

| Symptom | Meaning | Fix |
|---|---|---|
| `provider did not respond in time` | Ollama/API down or wrong URL | `agent-preflight.ps1 -StartProvider` |
| Empty model output, `finish=length` | model has no chat template / burns hidden tokens | switch model (see table) |
| `Gateway disconnected; turn outcome is unknown` | two Hermes runs collided, or the run was killed | run one at a time; resume the printed session |
| MCP tools missing in the agent | not registered, or wrong CLI path | `wire-craft-anything.ps1`, then `agent-preflight.ps1` |
| MCP `initialize` fails | CLI path wrong or package moved | pass `-Cli "<path>"`; test `craft-anything-cli.exe mcp --help` |
| 15 minutes of silence, 0 tokens | the above, compounded by retries | stop the loop, run preflight, then retry once |

## Verified state

- Craft Anything CLI `0.6.0`
- MCP handshake: **38 tools**, stdio
- OpenCode: `mcp.craft-anything` enabled
- Hermes: `craft-anything` enabled
- Hermes model: `lfm3:1.7b` @ `http://127.0.0.1:11434/v1`
- Preflight: all checks PASS
