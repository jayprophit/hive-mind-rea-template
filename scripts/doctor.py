#!/usr/bin/env python3
"""
Cross-platform health check for the Hive Mind REA stack.

Works on Windows, macOS, Linux and WSL. No third-party packages required.

    python scripts/doctor.py            # human readable
    python scripts/doctor.py --json     # machine readable (for CI / Grafana)
    python scripts/doctor.py --fix-hints  # only print things that need action

Exit codes: 0 = all required checks pass, 1 = a required check failed.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import socket
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# --------------------------------------------------------------------------
# Terminal handling. Windows 10 needs VT mode turned on explicitly.
# --------------------------------------------------------------------------
IS_WINDOWS = os.name == "nt"
IS_MAC = sys.platform == "darwin"
IS_LINUX = sys.platform.startswith("linux")
IS_WSL = IS_LINUX and "microsoft" in platform.release().lower()

if IS_WINDOWS:
    try:  # pragma: no cover - cosmetic only
        import ctypes

        k = ctypes.windll.kernel32
        k.SetConsoleMode(k.GetStdHandle(-11), 7)
    except Exception:
        pass

_COLOR = sys.stdout.isatty() and os.environ.get("NO_COLOR") is None


def paint(text: str, code: str) -> str:
    return f"\033[{code}m{text}\033[0m" if _COLOR else text


OK, WARN, BAD, DIM, BOLD = "32", "33", "31", "90", "1"

STATUS_ICON = {"pass": "[ok]", "warn": "[warn]", "fail": "[fail]", "skip": "[skip]"}


@dataclass
class Result:
    name: str
    status: str  # pass | warn | fail | skip
    detail: str = ""
    fix: str = ""


@dataclass
class Report:
    results: list[Result] = field(default_factory=list)

    def add(self, *a, **kw) -> None:
        self.results.append(Result(*a, **kw))

    def count(self, status: str) -> int:
        return sum(1 for r in self.results if r.status == status)

    @property
    def failed_required(self) -> bool:
        return self.count("fail") > 0


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------
def run(cmd: list[str], timeout: int = 15) -> tuple[int, str]:
    """Run a command, return (exit code, combined output). Never raises."""
    try:
        p = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=False,
        )
        return p.returncode, (p.stdout or "").strip() or (p.stderr or "").strip()
    except FileNotFoundError:
        return 127, "not found"
    except subprocess.TimeoutExpired:
        return 124, f"timed out after {timeout}s"
    except Exception as exc:  # noqa: BLE001 - diagnostic tool, stay alive
        return 1, str(exc)


# GUI installers rarely add themselves to PATH, so probe the conventional
# install roots as well. This is why a "not installed" result can be wrong.
_EXTRA_BIN_DIRS = [
    # Windows
    r"C:\Program Files\Craft Anything",
    r"C:\Program Files\Ollama",
    r"C:\Program Files\Git\cmd",
    r"C:\Program Files\Git\bin",
    r"C:\Program Files\GrafanaLabs\grafana\bin",
    # macOS
    "/Applications/Craft Anything.app/Contents/MacOS",
    "/opt/homebrew/bin",
    "/usr/local/bin",
    # Linux
    "/usr/local/bin",
    "/usr/bin",
    "/snap/bin",
    "~/.local/bin",
    "~/.opencode/bin",
]

_EXE_SUFFIXES = [".exe", ".cmd", ".bat", ""] if IS_WINDOWS else [""]


def which(name: str) -> str | None:
    """Resolve a binary on PATH or in a conventional install root."""
    hit = shutil.which(name)
    if hit:
        return hit
    for raw in _EXTRA_BIN_DIRS:
        base = Path(raw).expanduser()
        if not base.is_dir():
            continue
        for suffix in _EXE_SUFFIXES:
            candidate = base / f"{name}{suffix}"
            if candidate.is_file():
                return str(candidate)
    return None


def port_open(host: str, port: int, timeout: float = 0.6) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def human(n: float) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if abs(n) < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} PB"


def total_ram_gb() -> float:
    try:
        if IS_WINDOWS:
            code, out = run(
                ["powershell", "-NoProfile", "-Command",
                 "(Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory"]
            )
            return int(out) / 1024**3
        if IS_MAC:
            code, out = run(["sysctl", "-n", "hw.memsize"])
            return int(out) / 1024**3
        with open("/proc/meminfo") as fh:
            for line in fh:
                if line.startswith("MemTotal:"):
                    return int(line.split()[1]) / 1024**2
    except Exception:
        pass
    return 0.0


def data_dir() -> Path:
    """
    One writable location per OS, matching each platform's convention.
    Override with HIVE_DATA_DIR.
    """
    env = os.environ.get("HIVE_DATA_DIR")
    if env:
        return Path(env).expanduser()
    if IS_WINDOWS:
        base = os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local")
        return Path(base) / "hive-mind"
    if IS_MAC:
        return Path.home() / "Library" / "Application Support" / "hive-mind"
    return Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share")) / "hive-mind"


def config_dir() -> Path:
    env = os.environ.get("HIVE_CONFIG_DIR")
    if env:
        return Path(env).expanduser()
    if IS_WINDOWS:
        return Path(os.environ.get("APPDATA", Path.home())) / "hive-mind"
    if IS_MAC:
        return Path.home() / "Library" / "Application Support" / "hive-mind"
    return Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "hive-mind"


# --------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------
def check_platform(r: Report) -> None:
    name = {
        "windows": "Windows",
        "macos": "macOS",
        "linux": "Linux",
        "wsl": "Windows (WSL)",
    }.get("wsl" if IS_WSL else "windows" if IS_WINDOWS else "macos" if IS_MAC else "linux", "unknown")
    r.add("platform", "pass", f"{name} / {platform.machine()} / Python {platform.python_version()}")


def check_python(r: Report) -> None:
    major, minor = sys.version_info[:2]
    if (major, minor) < (3, 10):
        r.add("python", "fail", f"{major}.{minor} is too old",
              "install Python 3.10 or newer")
    else:
        r.add("python", "pass", f"{major}.{minor}")


def check_resources(r: Report) -> None:
    ram = total_ram_gb()
    if ram == 0:
        r.add("memory", "skip", "could not determine installed RAM")
    elif ram < 7:
        # 8 GB machines report ~7.7 GB usable; only 4 GB boxes should hard-fail.
        r.add("memory", "fail", f"{ram:.1f} GB installed",
              "8 GB minimum. Add RAM before running a local model.")
    elif ram < 16:
        r.add("memory", "warn", f"{ram:.1f} GB installed",
              "fine for 1.5-4B models. Run one model at a time; close browsers.")
    else:
        r.add("memory", "pass", f"{ram:.1f} GB installed")

    try:
        anchor = Path.home()
        free = shutil.disk_usage(anchor).free
        if free < 10 * 1024**3:
            r.add("disk", "fail", f"{human(free)} free on {anchor.anchor}",
                  "free at least 10 GB; model weights need room")
        elif free < 25 * 1024**3:
            r.add("disk", "warn", f"{human(free)} free on {anchor.anchor}",
                  "tight. Clear caches; see docs/TROUBLESHOOTING.md")
        else:
            r.add("disk", "pass", f"{human(free)} free")
    except Exception as exc:
        r.add("disk", "skip", str(exc))


def check_core_binaries(r: Report) -> None:
    for name, path_key, required, fix in [
        ("git", "git", True, "install Git"),
        ("node", "node", True, "install Node.js LTS"),
        ("npx", "npx", True, "ships with Node.js"),
        ("ollama", "ollama", True, "install Ollama"),
    ]:
        p = which(name)
        if p:
            code, out = run([p, "--version"], timeout=20)
            r.add(name, "pass", (out.splitlines() or [p])[0][:70])
        else:
            r.add(name, "fail" if required else "warn", "not on PATH", fix)


def check_optional_binaries(r: Report) -> None:
    # (name, args, hint shown when the binary is absent)
    optional = [
        ("opencode", ["--version"], "npm install -g opencode-ai"),
        ("hermes", ["--version"], "see https://hermes-agent.nousresearch.com"),
        ("docker", ["version", "--format", "{{.Server.Version}}"], "install Docker"),
        ("uvx", ["--version"], "pip install uv"),
        ("craft-anything-cli", ["--version"], "install Craft Anything"),
        ("ffmpeg", ["-version"], "install ffmpeg"),
        ("yt-dlp", ["--version"], "pip install yt-dlp"),
        ("mitmdump", ["--version"], "pip install mitproxy"),
        ("frida", ["--version"], "pip install frida-tools"),
        ("java", ["-version"], "install a JDK 21 for Ghidra / JADX"),
    ]
    for name, args, hint in optional:
        p = which(name)
        if not p:
            r.add(name, "warn", "not installed", hint)
            continue
        code, out = run([p, *args], timeout=12)
        first = (out.splitlines() or [""])[0][:70]
        if code == 0:
            r.add(name, "pass", first)
        elif code == 124:
            # Installed but hangs on --version; still usable.
            r.add(name, "pass", f"installed at {p} (slow --version)")
        elif name == "docker":
            r.add(name, "warn", "installed, daemon not running",
                  "start Docker Desktop only when you need the optional services")
        else:
            r.add(name, "warn", f"installed but returned {code}: {first[:60]}",
                  "run it by hand to see the real error")


def check_ollama(r: Report) -> None:
    if not port_open("127.0.0.1", 11434):
        r.add("ollama service", "warn", "not listening on :11434",
              "run 'ollama serve' (or start the app)")
        return
    r.add("ollama service", "pass", "listening on :11434")
    code, out = run(["ollama", "list"], timeout=20)
    if code != 0:
        r.add("ollama models", "warn", "could not list models", "run 'ollama list'")
        return
    lines = [l for l in out.splitlines()[1:] if l.strip()]
    if not lines:
        r.add("ollama models", "warn", "no models pulled",
              "ollama pull lfm3:1.7b")
    else:
        r.add("ollama models", "pass", f"{len(lines)} model(s): " +
              ", ".join(l.split()[0] for l in lines[:4]))


def check_ports(r: Report) -> None:
    for label, port in [("grafana", 3000), ("lmstudio", 1234), ("openclaw", 18789)]:
        if port_open("127.0.0.1", port):
            r.add(f"port {label}", "pass", f":{port} responding")
        else:
            r.add(f"port {label}", "skip", f":{port} not running (optional)")


def check_mcp(r: Report) -> None:
    """Verify Craft Anything answers an MCP initialize handshake."""
    p = which("craft-anything-cli")
    if not p:
        r.add("craft-anything mcp", "skip", "CLI not installed")
        return
    payload = json.dumps({
        "jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "doctor", "version": "1.0"},
        },
    })
    try:
        proc = subprocess.run(
            [p, "mcp"], input=payload + "\n",
            capture_output=True, text=True, timeout=25,
        )
        line = next((l for l in proc.stdout.splitlines() if '"result"' in l), "")
        if not line:
            r.add("craft-anything mcp", "fail", "no JSON-RPC response",
                  "run 'craft-anything-cli mcp' by hand and watch stderr")
            return
        info = json.loads(line)["result"].get("serverInfo", {})
        r.add("craft-anything mcp", "pass",
              f"serverInfo {info.get('name')} {info.get('version')}")
    except subprocess.TimeoutExpired:
        r.add("craft-anything mcp", "fail", "handshake timed out",
              "the CLI may be blocked on first-run download; run it once by hand")
    except Exception as exc:  # noqa: BLE001
        r.add("craft-anything mcp", "fail", str(exc)[:90], "")


def check_layout(r: Report) -> None:
    """Config and data locations, plus whether an agent config exists."""
    cfg, dat = config_dir(), data_dir()
    r.add("config dir", "pass" if cfg.exists() else "skip", str(cfg))
    r.add("data dir", "pass" if dat.exists() else "skip", str(dat))

    candidates = [
        Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "opencode" / "opencode.json",
        Path.home() / ".config" / "opencode" / "opencode.json",
        Path(os.environ.get("APPDATA", "")) / "opencode" / "opencode.json",
    ]
    found = next((c for c in candidates if c.is_file()), None)
    if found:
        try:
            cfg_json = json.loads(found.read_text(encoding="utf-8"))
            servers = list((cfg_json.get("mcp") or {}).keys())
            r.add("opencode config", "pass",
                  f"{found} (mcp: {', '.join(servers) or 'none'})")
            if "craft-anything" in servers:
                r.add("opencode -> craft-anything", "pass", "registered")
            else:
                r.add("opencode -> craft-anything", "warn", "not registered",
                      "run scripts/bootstrap.py --write-config")
        except Exception as exc:
            r.add("opencode config", "warn", f"{found}: {exc}", "")
    else:
        r.add("opencode config", "skip", "no opencode.json found",
              "run scripts/bootstrap.py --write-config")


def check_vault(r: Report) -> None:
    """One canonical vault. A second vault silently splits the second brain."""
    workspace = Path(os.environ.get("HIVE_WORKSPACE", Path.cwd()))
    vault = workspace / "obsidian-vault"
    if vault.is_dir():
        notes = list(vault.rglob("*.md"))
        r.add("second brain", "pass", f"{vault} ({len(notes)} notes)")
    else:
        r.add("second brain", "warn", f"no vault at {vault}",
              "run scripts/bootstrap.py --scaffold-vault")

    # Detect the split-brain failure mode.
    dupes = []
    for root in [Path.home() / "Documents", Path.home()]:
        if root.is_dir():
            dupes += [p for p in root.glob("*bsidian*") if p.is_dir()]
    extra = [d for d in dupes if d.resolve() != vault.resolve()]
    if len(extra) > 0:
        r.add("vault duplicates", "warn",
              "also found: " + ", ".join(str(d) for d in extra[:3]),
              "keep one vault; merge or archive the others")


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser(description="Hive Mind REA doctor")
    ap.add_argument("--json", action="store_true", help="emit JSON")
    ap.add_argument("--fix-hints", action="store_true",
                    help="print only checks that need action")
    args = ap.parse_args()

    report = Report()
    for fn in (
        check_platform, check_python, check_resources,
        check_core_binaries, check_optional_binaries,
        check_ollama, check_ports, check_mcp,
        check_layout, check_vault,
    ):
        try:
            fn(report)
        except Exception as exc:  # noqa: BLE001
            report.add(fn.__name__, "skip", f"check crashed: {exc}")

    if args.json:
        print(json.dumps({
            "platform": platform.platform(),
            "summary": {s: report.count(s) for s in ("pass", "warn", "fail", "skip")},
            "results": [r.__dict__ for r in report.results],
        }, indent=2))
        return 1 if report.failed_required else 0

    show = [r for r in report.results if r.status != "pass"] if args.fix_hints else report.results

    print()
    print(paint("  Hive Mind REA - system doctor", BOLD))
    print(paint(f"  {platform.platform()}", DIM))
    print()

    for res in show:
        icon = STATUS_ICON.get(res.status, "[?]")
        colour = {"pass": OK, "warn": WARN, "fail": BAD, "skip": DIM}[res.status]
        print(f"  {paint(icon, colour)} {res.name:<28} {res.detail}")
        if res.fix and res.status in ("warn", "fail"):
            print(f"        {paint('-> ' + res.fix, DIM)}")

    print()
    p, w, f, s = (report.count(x) for x in ("pass", "warn", "fail", "skip"))
    print(f"  {paint(str(p), OK)} pass   {paint(str(w), WARN)} warn   "
          f"{paint(str(f), BAD)} fail   {paint(str(s), DIM)} skip")

    if report.failed_required:
        print()
        print(paint("  Required checks failed. Fix the [fail] lines above.", BAD))
    else:
        print()
        print(paint("  No blocking problems. The stack can run.", OK))
    print()
    return 1 if report.failed_required else 0


if __name__ == "__main__":
    sys.exit(main())
