#!/usr/bin/env python3
"""Query data/knowledge.db (built by scripts/build_index.py).

Examples
--------
    python scripts/query.py --stats
    python scripts/query.py --search "bios ram"
    python scripts/query.py --search "mcp hermes" --limit 5
    python scripts/query.py --facts
    python scripts/query.py --facts toolchain
    python scripts/query.py --docs
    python scripts/query.py --doc docs/TROUBLESHOOTING.md
    python scripts/query.py --db projects/polsia-free-v1/knowledge.db --stats
    python scripts/query.py --db projects/polsia-free-v1/knowledge.db --runs 10
    python scripts/query.py --db projects/polsia-free-v1/knowledge.db --assets
"""
from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "knowledge.db"


def connect(path=None):
    target = Path(path).resolve() if path else DB
    if not target.exists():
        sys.exit(f"{target} is missing. Run: python scripts/build_index.py")
    con = sqlite3.connect(target)
    con.row_factory = sqlite3.Row
    return con


def fts_query(text: str) -> str:
    tokens = [t for t in re.split(r"[^0-9A-Za-z_]+", text) if len(t) >= 2]
    if not tokens:
        return '""'
    return " AND ".join(f'"{t}"*' for t in tokens)


def cmd_stats(con):
    counts = {
        "documents": con.execute("SELECT count(*) FROM documents").fetchone()[0],
        "headings": con.execute("SELECT count(*) FROM headings").fetchone()[0],
        "chunks": con.execute("SELECT count(*) FROM chunks").fetchone()[0],
        "links": con.execute("SELECT count(*) FROM links").fetchone()[0],
        "facts": con.execute("SELECT count(*) FROM facts").fetchone()[0],
    }
    print("knowledge.db")
    for k, v in counts.items():
        print(f"  {k:<10} {v}")
    print("\nfacts by category")
    for row in con.execute(
        "SELECT category, count(*) n FROM facts GROUP BY category ORDER BY n DESC"
    ):
        print(f"  {row['category']:<14} {row['n']}")


def cmd_search(con, query, limit):
    rows = con.execute(
        """
        SELECT path, heading,
               snippet(chunks_fts, 0, '«', '»', '…', 14) AS snip,
               bm25(chunks_fts) AS score
        FROM chunks_fts
        WHERE chunks_fts MATCH ?
        ORDER BY
            CASE
                WHEN path LIKE 'docs/%' OR path LIKE 'obsidian-vault/%'
                  OR path LIKE 'data/%' OR path = 'README.md' THEN 0
                WHEN path LIKE 'hermes/%' OR path LIKE 'platforms/%' THEN 1
                ELSE 2
            END,
            score
        LIMIT ?
        """,
        (fts_query(query), limit),
    ).fetchall()
    if not rows:
        print("no matches")
        return
    for r in rows:
        head = f" › {r['heading']}" if r["heading"] else ""
        print(f"\n{r['path']}{head}")
        print(f"  {r['snip']}")


def cmd_docs(con):
    for row in con.execute(
        "SELECT path, title, kind, words FROM documents ORDER BY path"
    ):
        print(f"{row['path']:<48} {row['kind']:<5} {row['words']:>6}w  {row['title']}")


def cmd_doc(con, path):
    doc = con.execute(
        "SELECT id, path, title, words, modified FROM documents WHERE path = ?", (path,)
    ).fetchone()
    if not doc:
        matches = con.execute(
            "SELECT path FROM documents WHERE path LIKE ? LIMIT 5", (f"%{path}%",)
        ).fetchall()
        if matches:
            print("not found; did you mean:")
            for m in matches:
                print(f"  {m['path']}")
        else:
            print("not found")
        return
    print(f"{doc['path']}  ({doc['words']} words, modified {doc['modified']})")
    print(f"title: {doc['title']}\n")
    for h in con.execute(
        "SELECT level, text, line FROM headings WHERE doc_id = ? ORDER BY line", (doc["id"],)
    ):
        print(f"  {'  ' * (h['level'] - 1)}{h['text']}  (line {h['line']})")


def cmd_facts(con, category):
    if category:
        rows = con.execute(
            "SELECT category, key, value FROM facts WHERE lower(category) = lower(?) ORDER BY key",
            (category,),
        ).fetchall()
    else:
        rows = con.execute(
            "SELECT category, key, value FROM facts ORDER BY category, key"
        ).fetchall()
    if not rows:
        print("no facts")
        return
    current = None
    for r in rows:
        if r["category"] != current:
            current = r["category"]
            print(f"\n[{current}]")
        print(f"  {r['key']}: {r['value']}")


def cmd_runs(con, limit):
    try:
        rows = con.execute("SELECT time, kind, substr(text,1,180) text FROM runs ORDER BY id DESC LIMIT ?",
                           (limit,)).fetchall()
    except sqlite3.OperationalError:
        print("no runs table (this is the template database)")
        return
    if not rows:
        print("no runs recorded")
        return
    for r in rows:
        print(f"  {r['time']} {r['kind']:<6} {r['text']}")


def cmd_assets(con):
    try:
        rows = con.execute(
            "SELECT path, kind, bytes, width, height, substr(sha256,1,12) hash "
            "FROM assets ORDER BY bytes DESC LIMIT 40"
        ).fetchall()
    except sqlite3.OperationalError:
        print("no assets table (this is the template database)")
        return
    for r in rows:
        dims = f" {r['width']}x{r['height']}" if r["width"] else ""
        print(f"  {r['path']:<58} {r['kind']:<5} {r['bytes']:>9,} B{dims}  {r['hash']}")


def cmd_sources(con):
    try:
        rows = con.execute(
            "SELECT path, kind, bytes FROM sources ORDER BY bytes DESC LIMIT 40"
        ).fetchall()
    except sqlite3.OperationalError:
        print("no sources table (this is the template database)")
        return
    for r in rows:
        print(f"  {r['kind']:<11} {r['bytes']:>11,} B  {r['path']}")


def main():
    # Windows consoles default to cp1252 and crash on arrows from the docs.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description="Query a template or project knowledge base")
    parser.add_argument("--db", help="Database file (default: data/knowledge.db)")
    parser.add_argument("--stats", action="store_true")
    parser.add_argument("--search", metavar="QUERY")
    parser.add_argument("--limit", type=int, default=8)
    parser.add_argument("--docs", action="store_true")
    parser.add_argument("--doc", metavar="PATH")
    parser.add_argument("--facts", nargs="?", const="", metavar="CATEGORY")
    parser.add_argument("--runs", nargs="?", const=10, type=int, metavar="N")
    parser.add_argument("--assets", action="store_true")
    parser.add_argument("--sources", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    con = connect(args.db)
    if args.stats:
        cmd_stats(con)
    elif args.runs is not None:
        cmd_runs(con, args.runs)
    elif args.assets:
        cmd_assets(con)
    elif args.sources:
        cmd_sources(con)
    elif args.search:
        cmd_search(con, args.search, args.limit)
    elif args.docs:
        cmd_docs(con)
    elif args.doc:
        cmd_doc(con, args.doc)
    elif args.facts is not None:
        cmd_facts(con, args.facts)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
