#!/usr/bin/env python3
"""Track project work items in the project database.

board.json is the editable source; this script syncs it into the
`work_items` table of projects/polsia-free-v1/knowledge.db and regenerates
the Obsidian live board from the database. No network, no credentials.

Usage:
    python scripts/track_status.py                # sync + regenerate board
    python scripts/track_status.py --report       # print status counts
    python scripts/track_status.py --status done  # list one status

Statuses: done, active, next, blocked, owner, missing.
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "projects" / "polsia-free-v1"
DB = PROJECT / "knowledge.db"
BOARD = ROOT / "data" / "board-polsia-free-v1.json"
NOTE = ROOT / "obsidian-vault" / "Projects" / "polsia-live-board.md"

ORDER = ["active", "next", "blocked", "owner", "missing", "done"]
TITLES = {
    "active": "Active now",
    "next": "Next — no user input needed",
    "blocked": "Blocked",
    "owner": "Owner-only — cannot be closed locally",
    "missing": "Missing by design or hardware",
    "done": "Done and verified",
}


def connect() -> sqlite3.Connection:
    DB.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB)
    con.execute(
        """CREATE TABLE IF NOT EXISTS work_items (
            key TEXT PRIMARY KEY,
            area TEXT NOT NULL,
            title TEXT NOT NULL,
            status TEXT NOT NULL,
            detail TEXT DEFAULT '',
            evidence TEXT DEFAULT '',
            owner INTEGER DEFAULT 0,
            updated TEXT NOT NULL
        )"""
    )
    con.commit()
    return con


def load(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    items = data.get("items", [])
    valid = set(ORDER)
    for item in items:
        if item.get("status") not in valid:
            raise SystemExit(f"invalid status {item.get('status')!r} for {item.get('key')}")
        for field in ("key", "area", "title"):
            if not item.get(field):
                raise SystemExit(f"missing {field} in item {item!r}")
    return data


def sync(con: sqlite3.Connection, data: dict) -> tuple[int, int]:
    today = date.today().isoformat()
    keys = {item["key"] for item in data["items"]}
    before = con.execute("select count(*) from work_items").fetchone()[0]
    for item in data["items"]:
        con.execute(
            """INSERT INTO work_items (key, area, title, status, detail, evidence, owner, updated)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(key) DO UPDATE SET
                 area=excluded.area, title=excluded.title, status=excluded.status,
                 detail=excluded.detail, evidence=excluded.evidence,
                 owner=excluded.owner, updated=excluded.updated""",
            (
                item["key"], item["area"], item["title"], item["status"],
                item.get("detail", ""), item.get("evidence", ""),
                1 if item.get("owner") else 0, today,
            ),
        )
    stale = [row[0] for row in con.execute("select key from work_items")]
    removed = [key for key in stale if key not in keys]
    for key in removed:
        con.execute("delete from work_items where key = ?", (key,))
    con.commit()
    return before, len(removed)


def rows(con: sqlite3.Connection, status: str | None = None) -> list[sqlite3.Row]:
    con.row_factory = sqlite3.Row
    sql = "select * from work_items"
    args: tuple = ()
    if status:
        sql += " where status = ?"
        args = (status,)
    sql += " order by area, title"
    return list(con.execute(sql, args))


def write_note(con: sqlite3.Connection, project: str) -> int:
    all_rows = rows(con)
    counts = {status: 0 for status in ORDER}
    for row in all_rows:
        counts[row["status"]] = counts.get(row["status"], 0) + 1

    lines = [
        "---",
        "type: board",
        f"date: {date.today().isoformat()}",
        f'project: "{project}"',
        "status: live",
        "generated: track_status.py",
        "---",
        "",
        f"# {project.title()} — live board",
        "",
        "Generated from `work_items` in the project database. Edit",
        "`data/board-polsia-free-v1.json`, then run",
        "`python scripts/track_status.py`. Do not hand-edit this note.",
        "",
        "Counts: " + ", ".join(f"{status} {counts.get(status, 0)}" for status in ORDER) + ".",
        "",
    ]
    for status in ORDER:
        group = [row for row in all_rows if row["status"] == status]
        if not group:
            continue
        lines.append(f"## {TITLES[status]}")
        lines.append("")
        lines.append("| Area | Item | Detail | Evidence |")
        lines.append("|---|---|---|---|")
        for row in group:
            detail = (row["detail"] or "").replace("|", "/")
            evidence = (row["evidence"] or "").replace("|", "/")
            lines.append(f"| {row['area']} | {row['title']} | {detail} | `{evidence}` |")
        lines.append("")
    lines.extend([
        "## Rules that keep this honest",
        "",
        "- Free/open-source by default; paid only with the owner's own keys and",
        "  explicit approval. No gates, credits or subscriptions.",
        "- No claims of consciousness, guaranteed returns, or a self-trained model",
        "  where none exists.",
        "- Human gate for sensitive/irreversible actions; secrets only in bridge env.",
        "- Research and competitor material stays attributed; no copied proprietary",
        "  code, assets, branding or prompts.",
        "",
    ])
    NOTE.parent.mkdir(parents=True, exist_ok=True)
    NOTE.write_text("\n".join(lines), encoding="utf-8")
    return len(all_rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", type=Path, default=DB)
    parser.add_argument("--board", type=Path, default=BOARD)
    parser.add_argument("--out", type=Path, default=NOTE)
    parser.add_argument("--report", action="store_true")
    parser.add_argument("--status", choices=ORDER)
    args = parser.parse_args()

    con = connect()
    if args.report or args.status:
        selected = rows(con, args.status)
        for row in selected:
            print(f"{row['status']:>8}  {row['area']:<10}  {row['title']}")
        if args.report:
            counts = {s: len(rows(con, s)) for s in ORDER}
            print("\n" + "  ".join(f"{s}={n}" for s, n in counts.items()))
        return 0

    data = load(args.board)
    before, removed = sync(con, data)
    written = write_note(con, data.get("project", "project"))
    print(f"work_items: {before} -> {written} rows ({removed} removed)")
    print(f"board note: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
