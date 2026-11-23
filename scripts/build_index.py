#!/usr/bin/env python3
"""Build a portable, searchable index of this repository.

Outputs
-------
data/index.json    structured, diffable dump (documents, headings, links, facts)
data/knowledge.db  SQLite + FTS5 for fast offline search

Run from anywhere:
    python scripts/build_index.py

The index is deliberately built from files that are safe to publish. Runtime
state (repos/, Hermes caches, *.db, session logs) is excluded.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml  # PyYAML is optional; the index still builds without it
except Exception:  # pragma: no cover
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DB_PATH = DATA / "knowledge.db"
JSON_PATH = DATA / "index.json"

TEXT_SUFFIXES = {
    ".md", ".markdown", ".txt", ".yaml", ".yml", ".json", ".jsonl",
    ".py", ".ps1", ".sh", ".toml", ".ini", ".cfg", ".html", ".css", ".js",
}

EXCLUDE_DIRS = {
    ".git", "repos", "node_modules", "__pycache__", ".venv", "venv",
    ".pytest_cache", ".mypy_cache", "dist", "build", ".next", ".cache",
}

# Hermes profile subtrees that are runtime state, not knowledge.
HERMES_SKIP = (
    "/cache/", "/logs/", "/backups/", "/sessions/", "/runtime/",
    "/audio_cache/", "/image_cache/", "/pairing/", "/plugin-update-checks/",
    "/platforms/",
)

EXCLUDE_FILES = {"data/index.json", "data/knowledge.db", "package-lock.json"}

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
WIKI_RE = re.compile(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")
MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def rel_posix(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def should_skip(path: Path) -> bool:
    rel = rel_posix(path)
    if rel in EXCLUDE_FILES:
        return True
    if any(part in EXCLUDE_DIRS for part in path.relative_to(ROOT).parts):
        return True
    if rel.startswith("hermes/profiles/") and any(s in f"/{rel}" for s in HERMES_SKIP):
        return True
    return False


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def find_headings(text: str):
    """ATX headings outside fenced code blocks, with 1-based line numbers."""
    out = []
    in_fence = False
    for i, line in enumerate(text.splitlines(), 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = HEADING_RE.match(line)
        if m:
            out.append({"level": len(m.group(1)), "text": m.group(2).strip(), "line": i})
    return out


def first_title(text: str, fallback: str) -> str:
    for h in find_headings(text):
        if h["level"] == 1:
            return h["text"]
    return fallback


def split_chunks(text: str, max_chars: int = 1400, overlap: int = 180):
    """Split on headings (outside fences), then hard-wrap long sections."""
    sections = []
    heading, start, buf = "", 1, []
    in_fence = False

    for i, line in enumerate(text.splitlines(keepends=True), 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
        m = None if in_fence else HEADING_RE.match(line)
        if m:
            if buf:
                sections.append((heading, start, "".join(buf)))
            heading, start, buf = m.group(2).strip(), i, [line]
        else:
            buf.append(line)
    if buf:
        sections.append((heading, start, "".join(buf)))

    chunks = []
    for heading, line, body in sections:
        body = body.strip()
        if not body:
            continue
        if len(body) <= max_chars:
            chunks.append((heading, line, body))
            continue
        start_at = 0
        while start_at < len(body):
            piece = body[start_at:start_at + max_chars]
            chunks.append((heading, line, piece))
            if start_at + max_chars >= len(body):
                break
            start_at += max_chars - overlap
    return chunks


def hard_wrap(text: str, max_chars: int = 1400, overlap: int = 180):
    text = text.strip()
    if not text:
        return []
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(("", 1, text[start:start + max_chars]))
        if start + max_chars >= len(text):
            break
        start += max_chars - overlap
    return chunks


def flatten_facts(obj, prefix="", category=""):
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            key = f"{prefix}.{k}" if prefix else k
            out.extend(flatten_facts(v, key, category or k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out.extend(flatten_facts(v, f"{prefix}[{i}]", category))
    else:
        out.append((category or "general", prefix, str(obj)))
    return out


def load_stack_facts():
    path = ROOT / "core" / "stack.yaml"
    if not path.exists() or yaml is None:
        return []
    try:
        stack = yaml.safe_load(read_text(path)) or {}
    except Exception:
        return []
    facts = [
        ("stack", "schema", str(stack.get("schema", ""))),
        ("stack", "name", str(stack.get("name", ""))),
        ("stack", "version", str(stack.get("version", ""))),
    ]
    for comp in stack.get("components", []) or []:
        cid = comp.get("id", "?")
        facts.append(("component", f"{cid}.label", str(comp.get("label", ""))))
        facts.append(("component", f"{cid}.required", str(comp.get("required", ""))))
        facts.append(("component", f"{cid}.role", str(comp.get("role", ""))))
        facts.append(("component", f"{cid}.detect", json.dumps(comp.get("detect", {}))))
    return facts


def build():
    DATA.mkdir(parents=True, exist_ok=True)
    documents = []
    all_facts = []

    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if should_skip(path):
            continue

        text = read_text(path)
        if not text.strip():
            continue

        rel = rel_posix(path)
        is_markdown = path.suffix.lower() in {".md", ".markdown"}
        title = first_title(text, path.stem) if is_markdown else path.stem
        headings = find_headings(text) if is_markdown else []
        links = sorted({m.group(1).strip() for m in WIKI_RE.finditer(text)} |
                       {m.group(1).strip() for m in MD_LINK_RE.finditer(text)})
        chunks = split_chunks(text) if is_markdown else hard_wrap(text)
        words = len(re.findall(r"\w+", text))

        documents.append({
            "path": rel,
            "kind": path.suffix.lower().lstrip("."),
            "title": title,
            "modified": datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat(timespec="seconds"),
            "sha256": hashlib.sha256(text.encode("utf-8", "ignore")).hexdigest(),
            "words": words,
            "headings": headings,
            "links": links,
            "chunks": [{"heading": h, "line": ln, "text": t} for h, ln, t in chunks],
        })

    facts_path = DATA / "build-facts.json"
    if facts_path.exists():
        try:
            facts = json.loads(read_text(facts_path))
            all_facts.extend(flatten_facts(facts))
        except json.JSONDecodeError as exc:
            print(f"WARN: data/build-facts.json is not valid JSON: {exc}", file=sys.stderr)
    all_facts.extend(load_stack_facts())

    index = {
        "schema": "knowledge-index/v1",
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "root": str(ROOT),
        "counts": {
            "documents": len(documents),
            "headings": sum(len(d["headings"]) for d in documents),
            "chunks": sum(len(d["chunks"]) for d in documents),
            "facts": len(all_facts),
        },
        "documents": documents,
        "facts": [{"category": c, "key": k, "value": v} for c, k, v in all_facts],
    }
    JSON_PATH.write_text(json.dumps(index, indent=2, ensure_ascii=False), encoding="utf-8")

    if DB_PATH.exists():
        DB_PATH.unlink()
    con = sqlite3.connect(DB_PATH)
    con.execute("PRAGMA journal_mode=DELETE")
    con.executescript(
        """
        CREATE TABLE documents(
            id INTEGER PRIMARY KEY, path TEXT UNIQUE, kind TEXT, title TEXT,
            modified TEXT, sha256 TEXT, words INTEGER);
        CREATE TABLE headings(
            id INTEGER PRIMARY KEY, doc_id INTEGER, level INTEGER,
            text TEXT, line INTEGER,
            FOREIGN KEY(doc_id) REFERENCES documents(id));
        CREATE TABLE chunks(
            id INTEGER PRIMARY KEY, doc_id INTEGER, heading TEXT,
            line_start INTEGER, text TEXT,
            FOREIGN KEY(doc_id) REFERENCES documents(id));
        CREATE TABLE links(
            id INTEGER PRIMARY KEY, doc_id INTEGER, target TEXT);
        CREATE TABLE facts(
            id INTEGER PRIMARY KEY, category TEXT, key TEXT, value TEXT);
        CREATE VIRTUAL TABLE chunks_fts USING fts5(
            text, heading, path UNINDEXED, doc_id UNINDEXED,
            tokenize='porter unicode61');
        """
    )

    for doc in documents:
        cur = con.execute(
            "INSERT INTO documents(path,kind,title,modified,sha256,words) VALUES(?,?,?,?,?,?)",
            (doc["path"], doc["kind"], doc["title"], doc["modified"], doc["sha256"], doc["words"]),
        )
        doc_id = cur.lastrowid
        for h in doc["headings"]:
            con.execute("INSERT INTO headings(doc_id,level,text,line) VALUES(?,?,?,?)",
                        (doc_id, h["level"], h["text"], h["line"]))
        for link in doc["links"]:
            con.execute("INSERT INTO links(doc_id,target) VALUES(?,?)", (doc_id, link))
        for chunk in doc["chunks"]:
            con.execute("INSERT INTO chunks(doc_id,heading,line_start,text) VALUES(?,?,?,?)",
                        (doc_id, chunk["heading"], chunk["line"], chunk["text"]))
            con.execute("INSERT INTO chunks_fts(text,heading,path,doc_id) VALUES(?,?,?,?)",
                        (chunk["text"], chunk["heading"], doc["path"], doc_id))

    for category, key, value in all_facts:
        con.execute("INSERT INTO facts(category,key,value) VALUES(?,?,?)", (category, key, value))

    con.commit()
    con.close()

    print(f"documents : {index['counts']['documents']}")
    print(f"headings  : {index['counts']['headings']}")
    print(f"chunks    : {index['counts']['chunks']}")
    print(f"facts     : {index['counts']['facts']}")
    print(f"json      : {JSON_PATH.relative_to(ROOT)} "
          f"({JSON_PATH.stat().st_size / 1024:.0f} KB)")
    print(f"database  : {DB_PATH.relative_to(ROOT)} "
          f"({DB_PATH.stat().st_size / 1024:.0f} KB)")


def main():
    parser = argparse.ArgumentParser(description="Build data/index.json and data/knowledge.db")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()
    build()


if __name__ == "__main__":
    main()
