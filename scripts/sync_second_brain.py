#!/usr/bin/env python3
"""Automatic second-brain sync for Polsia Free v1.

Keeps the three copies of the project's memory consistent after each round:

  1. project DB   -> workspace .hive/ copy
  2. obsidian-vault/ -> the live Obsidian vault mirror
  3. writes a timestamped line to Work/SYNC_LOG.md

Idempotent: files are copied only when size or mtime differs. Cross-platform
(pathlib/shutil), standard library only. Use --check to report without writing.

Usage:
  python scripts/sync_second_brain.py
  python scripts/sync_second_brain.py --check
  PFV1_WORKSPACE="D:\\projects\\polsia free v1" python scripts/sync_second_brain.py
"""
from __future__ import annotations

import argparse
import filecmp
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PROJECT_DB = REPO / "projects" / "polsia-free-v1" / "knowledge.db"
VAULT = REPO / "obsidian-vault"
DEFAULT_WORKSPACE = Path(os.environ.get(
    "PFV1_WORKSPACE", r"C:\Users\jpowe\Desktop\projects\polsia free v1"))
DEFAULT_MIRROR = Path(os.environ.get(
    "PFV1_VAULT_MIRROR", r"C:\Users\jpowe\Documents\ObsidianVault"))


def needs_copy(src: Path, dst: Path) -> bool:
    if not dst.exists():
        return True
    if src.stat().st_size != dst.stat().st_size:
        return True
    try:
        return not filecmp.cmp(src, dst, shallow=False)
    except OSError:
        return True


def sync_project_db(workspace: Path, apply: bool, lines: list[str]) -> None:
    target = workspace / ".hive" / "knowledge.db"
    if not PROJECT_DB.exists():
        lines.append(f"- SKIP project DB (missing: {PROJECT_DB})")
        return
    if not workspace.exists():
        lines.append(f"- SKIP workspace copy (missing: {workspace})")
        return
    if needs_copy(PROJECT_DB, target):
        lines.append(f"- COPY project DB -> {target}")
        if apply:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(PROJECT_DB, target)
    else:
        lines.append(f"- OK project DB already current ({target.name})")


def sync_vault(mirror: Path, apply: bool, lines: list[str]) -> None:
    if not VAULT.exists():
        lines.append(f"- SKIP vault (missing: {VAULT})")
        return
    copied = skipped = 0
    for src in sorted(VAULT.rglob("*")):
        if not src.is_file():
            continue
        dst = mirror / src.relative_to(VAULT)
        if needs_copy(src, dst):
            copied += 1
            if apply:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
        else:
            skipped += 1
    lines.append(f"- VAULT: {copied} to copy, {skipped} already current -> {mirror}")


def write_log(apply: bool, lines: list[str], mirror: Path) -> None:
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    note = VAULT / "Work" / "SYNC_LOG.md"
    body = [f"\n## {stamp}\n"] + lines + [""]
    lines.append(f"- LOG {note.name}")
    if apply and note.parent.exists():
        with note.open("a", encoding="utf-8") as f:
            f.write("\n".join(body))
        # Mirror the log immediately so the live vault never lags one run.
        dst = mirror / "Work" / "SYNC_LOG.md"
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(note, dst)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="report what would change without writing anything")
    ap.add_argument("--workspace", type=Path, default=DEFAULT_WORKSPACE)
    ap.add_argument("--mirror", type=Path, default=DEFAULT_MIRROR)
    args = ap.parse_args()

    apply = not args.check
    lines: list[str] = []
    sync_project_db(args.workspace, apply, lines)
    sync_vault(args.mirror, apply, lines)
    write_log(apply, lines, args.mirror)

    print("Second-brain sync " + ("(check only)" if args.check else "(applied)"))
    for line in lines:
        print("  " + line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
