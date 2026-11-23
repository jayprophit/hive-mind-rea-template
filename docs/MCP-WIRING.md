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

## Model policy: free cloud for builds

The builder prompt is ~9,000 characters plus the system prompt and 38 tool
schemas. On an 8 GB CPU-only laptop, no local model can prefill and iterate
fast enough. **Use free cloud models; keep local models as fallback only.**

| Model | Where | Evidence | Verdict |
|---|---|---|---|
| `stepfun/step-3.7-flash:free` | Hermes via Nous API | tool call succeeded; 9k prompt answered in 2.6 s | **chosen for Hermes** |
| `opencode/hy4-flash-free` | OpenCode built-in | `opencode run` replied in 2.7 s, no credits needed | **chosen for OpenCode / Craft Anything** |
| `tencent/hy4-flash:free` | Nous free | no usable tool call | rejected |
| `upstage/solar-mini4:free` | Nous free | no tool call | rejected |
| `meituan/longcat-2.5:free` | Nous free | no tool call; 27 s on a long prompt | rejected |
| `qwen/qwen4-max:free` | Nous free | upstream capacity errors | rejected |
| any `...` paid model on Nous | Nous | HTTP 404: account has no credits | unavailable |
| `bonsai-2:4b` | local | 57.7 s for "OK", empty below 64 tokens, no chat template | **do not use as an agent** |
| `lfm3:1.7b` | local | "OK" in 15.8–20.8 s | fallback only |
| any 7B+ local | local | does not fit beside Chrome + WSL on 8 GB | desktop only |

Applied configuration:

```powershell
# Hermes - Nous free tier, tool-capable model
hermes config set model.default stepfun/step-3.7-flash:free
hermes config set model.provider nous
hermes config set model.base_url https://inference-api.nousresearch.com/v1
hermes config set model.api_mode chat_completions
hermes config set auxiliary.coder.provider nous
hermes config set auxiliary.coder.model stepfun/step-3.7-flash:free
hermes config set auxiliary.group_router.provider nous
hermes config set auxiliary.group_router.model stepfun/step-3.7-flash:free
```

OpenCode uses `~/.config/opencode/opencode.json`:
`"model": "opencode/hy4-flash-free"` (MCP entries preserved).

Craft Anything's `craft.json` sets `"builder": "OpenCode"`, and CLI runs use
`--backend OpenCode`. Craft Anything's doctor reports all backends registered
and the MCP self-test healthy.

Nous access tokens are short-lived and Hermes refreshes them itself. Never copy
a token into the repo, an `opencode.json`, or an environment variable file.
Verify tool support before choosing any free model — most do not support it.

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
- Hermes model: `stepfun/step-3.7-flash:free` @ Nous inference API (free tier)
- OpenCode model: `opencode/hy4-flash-free` (no credits required)
- Craft Anything builder: OpenCode (verified building the `polsia free v1` site)
- Preflight: all checks PASS; remote provider is reported as WARN (not probed)
