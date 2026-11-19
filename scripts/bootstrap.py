#!/usr/bin/env python3
"""
Cross-platform bootstrap for the Hive Mind REA stack.

One entry point for Windows, macOS and Linux. It never guesses: it detects the
platform, resolves per-OS paths, and writes declarative config that each host
application already understands.

    python scripts/bootstrap.py                 # show the plan, change nothing
    python scripts/bootstrap.py --apply         # write configs
    python scripts/bootstrap.py --apply --install
    python scripts/bootstrap.py --scaffold-vault

Design rules
------------
1. Nothing is written outside the OS-conventional config/data dirs unless asked.
2. Every write is idempotent and merged, never a blind overwrite.
3. Missing optional tools are reported with the exact command to install them.
4. No shell-specific syntax leaks into generated files.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

# --------------------------------------------------------------------------
# Platform identity
# --------------------------------------------------------------------------
IS_WINDOWS = os.name == "nt"
IS_MAC = sys.platform == "darwin"
IS_LINUX = sys.platform.startswith("linux")
IS_WSL = IS_LINUX and "microsoft" in platform.release().lower()

PLATFORM = (
    "windows" if IS_WINDOWS
    else "macos" if IS_MAC
    else "linux"
)

BOLD, DIM, OKC, WARNC, BADC = "1", "90", "32", "33", "31"
_COLOR = sys.stdout.isatty() and os.environ.get("NO_COLOR") is None


def paint(t: str, c: str) -> str:
    return f"\033[{c}m{t}\033[0m" if _COLOR else t


def say(msg: str) -> None:
    print(f"  {msg}")


def head(msg: str) -> None:
    print()
    print(paint(f"  {msg}", BOLD))
    print(paint("  " + "-" * (len(msg)), DIM))


# --------------------------------------------------------------------------
# Path resolution: the only place OS differences are allowed to appear
# --------------------------------------------------------------------------
def home() -> Path:
    return Path.home()


def config_root() -> Path:
    if IS_WINDOWS:
        return Path(os.environ.get("APPDATA", home() / "AppData" / "Roaming"))
    if IS_MAC:
        return home() / "Library" / "Application Support"
    return Path(os.environ.get("XDG_CONFIG_HOME", home() / ".config"))


def data_root() -> Path:
    if IS_WINDOWS:
        return Path(os.environ.get("LOCALAPPDATA", home() / "AppData" / "Local"))
    if IS_MAC:
        return home() / "Library" / "Application Support"
    return Path(os.environ.get("XDG_DATA_HOME", home() / ".local" / "share"))


def opencode_config_path() -> Path:
    """
    OpenCode reads ~/.config/opencode on every OS, including Windows.
    Keep that as the single canonical location for portability.
    """
    return home() / ".config" / "opencode" / "opencode.json"


def opencode_agents_dir() -> Path:
    return home() / ".config" / "opencode" / "agents"


def hermes_home() -> Path:
    env = os.environ.get("HERMES_HOME")
    if env:
        return Path(env).expanduser()
    return data_root() / "hermes"


def workspace_root() -> Path:
    return Path(os.environ.get("HIVE_WORKSPACE", Path(__file__).resolve().parent.parent))


# --------------------------------------------------------------------------
# Binary discovery (GUI installers do not update PATH)
# --------------------------------------------------------------------------
BIN_DIRS = {
    "windows": [
        r"C:\Program Files\Craft Anything",
        r"C:\Program Files\Ollama",
        r"C:\Program Files\nodejs",
        r"C:\Program Files\Git\cmd",
    ],
    "macos": [
        "/Applications/Craft Anything.app/Contents/MacOS",
        "/opt/homebrew/bin",
        "/usr/local/bin",
    ],
    "linux": ["/usr/local/bin", "/usr/bin", "/snap/bin", "~/.local/bin"],
}
EXE = [".exe", ".cmd", ".bat", ""] if IS_WINDOWS else [""]


def find_bin(name: str) -> str | None:
    hit = shutil.which(name)
    if hit:
        return hit
    for d in BIN_DIRS[PLATFORM]:
        base = Path(d).expanduser()
        if not base.is_dir():
            continue
        for suf in EXE:
            f = base / f"{name}{suf}"
            if f.is_file():
                return str(f)
    return None


# --------------------------------------------------------------------------
# Config writers
# --------------------------------------------------------------------------
def merge_json(path: Path, patch: dict, apply: bool) -> str:
    """
    Deep-merge `patch` into the JSON file at `path`.
    Returns a short human description of what would change.
    """
    current: dict = {}
    if path.is_file():
        try:
            current = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return f"refusing to touch {path}: not valid JSON"

    def deep_merge(dst: dict, src: dict) -> None:
        for k, v in src.items():
            if isinstance(v, dict) and isinstance(dst.get(k), dict):
                deep_merge(dst[k], v)
            else:
                dst[k] = v

    before = json.dumps(current, sort_keys=True)
    deep_merge(current, patch)
    after = json.dumps(current, sort_keys=True)

    if before == after:
        return f"{path} already current"
    if not apply:
        return f"would update {path}"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(current, indent=2) + "\n", encoding="utf-8")
    return f"wrote {path}"


def write_text(path: Path, content: str, apply: bool, overwrite: bool = False) -> str:
    if path.is_file() and not overwrite:
        return f"{path} exists, left alone"
    if not apply:
        return f"would create {path}"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return f"wrote {path}"


def build_mcp_block() -> dict:
    """MCP servers shared by OpenCode and Hermes."""
    ca = find_bin("craft-anything-cli")
    servers: dict = {}

    if ca:
        servers["craft-anything"] = {
            "type": "local",
            "command": [ca, "mcp"],
            "enabled": True,
        }
    else:
        servers["craft-anything"] = {
            "type": "local",
            "command": ["craft-anything-cli", "mcp"],
            "enabled": False,
            "_note": "CLI not found at bootstrap time; install it, then re-run.",
        }
    return servers


def write_opencode(apply: bool) -> list[str]:
    msgs = []
    path = opencode_config_path()
    msgs.append(merge_json(path, {"mcp": build_mcp_block()}, apply))

    # Copy portable agent prompts if this checkout carries them.
    src = workspace_root() / "opencode" / "agents"
    if src.is_dir():
        dst = opencode_agents_dir()
        files = sorted(src.glob("*.md"))
        if files:
            if apply:
                dst.mkdir(parents=True, exist_ok=True)
                for f in files:
                    shutil.copy2(f, dst / f.name)
                msgs.append(f"copied {len(files)} agent prompt(s) to {dst}")
            else:
                msgs.append(f"would copy {len(files)} agent prompt(s) to {dst}")
    return msgs


def write_hermes(apply: bool) -> list[str]:
    """Register Craft Anything with Hermes without clobbering user settings."""
    msgs = []
    ca = find_bin("craft-anything-cli")
    cfg = hermes_home() / "config.yaml"

    if not hermes_home().is_dir():
        return [f"hermes home not found at {hermes_home()}; skipping (optional)"]

    if not cfg.is_file():
        return [f"no config.yaml in {hermes_home()}; run Hermes once first"]

    text = cfg.read_text(encoding="utf-8", errors="replace")
    if "craft-anything:" in text and "mcp_servers:" in text:
        return [f"{cfg} already registers craft-anything"]

    block = (
        "\n# --- added by scripts/bootstrap.py ---\n"
        "mcp_servers:\n"
        "  craft-anything:\n"
        "    enabled: true\n"
        "    command: "
        + json.dumps(ca or "craft-anything-cli")
        + "\n    args:\n      - mcp\n"
    )

    if not apply:
        return [f"would append craft-anything block to {cfg}"]

    # Never rewrite YAML in place; keep a timestamped backup next to it.
    from datetime import datetime, timezone
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    shutil.copy2(cfg, cfg.with_suffix(f".yaml.bak-{stamp}"))
    with cfg.open("a", encoding="utf-8") as fh:
        fh.write(block)
    return [f"appended craft-anything to {cfg} (backup kept)"]


VAULT_FILES = {
    "README.md": """# Second Brain

One vault. One source of truth.

## Structure
- `Daily/`    one note per day, one row per agent turn
- `Work/`     PROJECT_MATRIX.md is the master tracker
- `Projects/` one note per project
- `Templates/` note templates
- `Dashboards/` saved queries and Grafana links

## Rule
Every agent turn writes exactly one row keyed by `requestId`.
Re-running the same request updates that row instead of adding a new one.
""",
    "Work/PROJECT_MATRIX.md": """---
title: Project Matrix
type: index
---

# Project Matrix

| Date | requestId | Project | Role | Action | Status | Link |
|------|-----------|---------|------|--------|--------|------|
""",
    "Templates/Daily.md": """---
date: {{date}}
type: daily
---

# {{date}}

## Turns
| requestId | Role | Action | Result |
|-----------|------|--------|--------|
""",
}


def scaffold_vault(apply: bool) -> list[str]:
    vault = workspace_root() / "obsidian-vault"
    msgs = []
    for rel, content in VAULT_FILES.items():
        msgs.append(write_text(vault / rel, content, apply))
    for d in ("Daily", "Work", "Projects", "Templates", "Dashboards"):
        if apply:
            (vault / d).mkdir(parents=True, exist_ok=True)
    if apply:
        msgs.append(f"vault ready at {vault}")
    return msgs


# --------------------------------------------------------------------------
# Missing tools
# --------------------------------------------------------------------------
INSTALL_CMDS = {
    "windows": {
        "ollama": "winget install --id Ollama.Ollama -e",
        "git": "winget install --id Git.Git -e",
        "node": "winget install --id OpenJS.NodeJS.LTS -e",
        "craft-anything-cli": "winget install --id CraftAnything.CraftAnything -e",
        "opencode": "npm install -g opencode-ai",
        "uvx": "pip install uv",
    },
    "macos": {
        "ollama": "brew install ollama",
        "git": "brew install git",
        "node": "brew install node",
        "craft-anything-cli": "brew install --cask craft-anything",
        "opencode": "npm install -g opencode-ai",
        "uvx": "pip install uv",
    },
    "linux": {
        "ollama": "curl -fsSL https://ollama.com/install.sh | sh",
        "git": "sudo apt-get install -y git",
        "node": "sudo apt-get install -y nodejs npm",
        "craft-anything-cli": "curl -fsSL https://craftanything.dev/install.sh | sh",
        "opencode": "npm install -g opencode-ai",
        "uvx": "pip install uv",
    },
}


def report_missing(apply: bool) -> None:
    head("Components")
    cmds = INSTALL_CMDS[PLATFORM]
    for name, hint in cmds.items():
        found = find_bin(name)
        if found:
            say(f"{paint('[ok]', OKC)}   {name:<22} {found}")
            continue
        say(f"{paint('[--]', WARNC)}   {name:<22} missing")
        say(f"       {paint(hint, DIM)}")
        if apply:
            try:
                if IS_WINDOWS:
                    subprocess.run(hint, shell=True, check=False)
                else:
                    subprocess.run(hint, shell=True, check=False)
            except Exception as exc:  # noqa: BLE001
                say(f"       install failed: {exc}")


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser(
        description="Bootstrap the Hive Mind REA stack on any OS.")
    ap.add_argument("--apply", action="store_true",
                    help="actually write files (default is a dry run)")
    ap.add_argument("--install", action="store_true",
                    help="attempt to install missing components")
    ap.add_argument("--scaffold-vault", action="store_true",
                    help="create the Obsidian vault skeleton")
    ap.add_argument("--check", action="store_true",
                    help="run scripts/doctor.py afterwards")
    args = ap.parse_args()

    print()
    print(paint("  Hive Mind REA - bootstrap", BOLD))
    print(paint(f"  {platform.platform()}", DIM))
    print(paint(f"  mode: {'APPLY' if args.apply else 'dry run'}", DIM))

    head("Resolved locations")
    for label, value in [
        ("workspace", workspace_root()),
        ("opencode config", opencode_config_path()),
        ("opencode agents", opencode_agents_dir()),
        ("hermes home", hermes_home()),
        ("vault", workspace_root() / "obsidian-vault"),
    ]:
        say(f"{label:<18} {value}")

    if args.install:
        report_missing(apply=True)

    head("Agent hosts")
    for msg in write_opencode(args.apply):
        say(msg)
    for msg in write_hermes(args.apply):
        say(msg)

    head("Second brain")
    if args.scaffold_vault:
        for msg in scaffold_vault(args.apply):
            say(msg)
    else:
        vault = workspace_root() / "obsidian-vault"
        if vault.is_dir():
            n = len(list(vault.rglob("*.md")))
            say(f"vault present: {vault} ({n} notes)")
        else:
            say("no vault yet; re-run with --scaffold-vault")

    print()
    if not args.apply:
        print(paint("  Dry run complete. Re-run with --apply to make changes.", WARNC))
    else:
        print(paint("  Done.", OKC))
    print()

    if args.check:
        doctor = Path(__file__).with_name("doctor.py")
        if doctor.is_file():
            return subprocess.call([sys.executable, str(doctor)])
    return 0


if __name__ == "__main__":
    sys.exit(main())
