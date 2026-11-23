#!/usr/bin/env python3
"""Build a portable, searchable index of a repository OR a project workspace.

Outputs
-------
<root>/data/index.json    structured, diffable dump
<root>/data/knowledge.db  SQLite + FTS5 for fast offline search

Run from anywhere:
    python scripts/build_index.py                       # this template
    python scripts/build_index.py --root "C:\\path\\project" --project \
        --out "C:\\repo\\projects\\name\\knowledge.db"   # project copy

The project mode uses the same schema as the template (so it is a copy of the
template database), then adds project-only tables: assets, sources, runs,
approvals. Every file is recorded once in `sources` with a sha256 so nothing is
duplicated or silently missed.
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

# Set by main(); project mode builds a separate database from the same schema.
PROJECT_MODE = False

TEXT_SUFFIXES = {
    ".md", ".markdown", ".txt", ".yaml", ".yml", ".json", ".jsonl",
    ".py", ".ps1", ".sh", ".toml", ".ini", ".cfg", ".html", ".css", ".js",
    ".svg", ".csv", ".xml",
}

ASSET_SUFFIXES = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".ico", ".avif",
    ".otf", ".ttf", ".woff", ".woff2", ".eot", ".pdf", ".mp3", ".mp4",
    ".wav", ".zip", ".glb", ".gltf",
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
    if (rel in EXCLUDE_FILES or rel.endswith("knowledge.db")
            or rel.endswith("index.json") or rel.endswith("knowledge.json")):
        return True
    dirs = set(EXCLUDE_DIRS)
    if PROJECT_MODE:
        # A project's dist/ is output worth recording, not runtime state.
        dirs.discard("dist")
        dirs.discard("build")
    if any(part in dirs for part in path.relative_to(ROOT).parts):
        return True
    if not PROJECT_MODE and rel.startswith("hermes/profiles/") and any(
        s in f"/{rel}" for s in HERMES_SKIP
    ):
        return True
    if rel.endswith(".db-shm") or rel.endswith(".db-wal"):
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


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    try:
        with path.open("rb") as fh:
            for block in iter(lambda: fh.read(65536), b""):
                h.update(block)
    except OSError:
        return ""
    return h.hexdigest()


def parse_activity(path: Path):
    """build-activity.log -> (time, kind, text) rows."""
    rows = []
    if not path.exists():
        return rows
    for line in read_text(path).splitlines():
        m = re.match(r"^(\d\d:\d\d:\d\d)\s+(\w+)\s+(.*)$", line)
        if m:
            rows.append((m.group(1), m.group(2), m.group(3)[:2000]))
    return rows


def parse_inbox(root: Path):
    """Inbox questions/approvals -> rows with answered/waiting status."""
    rows = []
    inbox = root / "inbox"
    if not inbox.exists():
        return rows
    for p in sorted(inbox.glob("*.json")):
        if p.name == "build-progress.json":
            continue
        try:
            d = json.loads(read_text(p))
        except json.JSONDecodeError:
            continue
        answered = list(inbox.glob(str(p.stem.split("-request")[0]) + "*.answer.json"))
        rows.append((
            d.get("id", p.stem), d.get("kind", ""), d.get("title", ""),
            d.get("action", ""), d.get("created_ms", ""),
            "answered" if answered else "waiting",
        ))
    return rows


def project_facts(root: Path):
    """Curated facts pulled from a project's own state files."""
    facts = []
    cp = root / "craft.json"
    if cp.exists():
        try:
            d = json.loads(read_text(cp))
            for key in ("name", "builder", "status", "stack", "questions"):
                if key in d:
                    facts.append(("project", f"craft.{key}", str(d[key])))
            if d.get("request"):
                facts.append(("project", "craft.request", str(d["request"])[:4000]))
            if d.get("note"):
                facts.append(("project", "craft.note", str(d["note"])[:1000]))
            approvals = d.get("approvals", {})
            for k, v in approvals.items():
                facts.append(("project", f"approval.{k}", str(v)))
            for i, c in enumerate(d.get("checks", []) or []):
                facts.append(("check", f"check[{i}]", json.dumps(c)[:1000]))
        except json.JSONDecodeError:
            pass
    return facts


def build():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    documents = []
    assets = []
    sources = []
    all_facts = []

    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or should_skip(path):
            continue

        suffix = path.suffix.lower()
        rel = rel_posix(path)
        stat = path.stat()
        modified = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(timespec="seconds")

        # Binary evidence is recorded, never duplicated into text chunks.
        if suffix in ASSET_SUFFIXES:
            digest = sha256_file(path)
            width = height = None
            try:
                from PIL import Image
                with Image.open(path) as im:
                    width, height = im.size
            except Exception:
                pass
            assets.append({
                "path": rel, "kind": suffix.lstrip("."), "bytes": stat.st_size,
                "modified": modified, "sha256": digest,
                "width": width, "height": height,
            })
            sources.append((rel, "asset", digest, stat.st_size, modified))
            continue

        # Very large evidence captures are recorded by hash, never chunked.
        # Their content is already in the project; duplicating it here only
        # inflates the database. The path + sha256 prevents anything being lost.
        if PROJECT_MODE and ("evidence/" in rel or stat.st_size > 1_000_000):
            digest = sha256_file(path)
            sources.append((rel, "evidence" if "evidence/" in rel else "large_text",
                            digest, stat.st_size, modified))
            continue

        if suffix not in TEXT_SUFFIXES:
            digest = sha256_file(path)
            sources.append((rel, "other", digest, stat.st_size, modified))
            continue

        text = read_text(path)
        if not text.strip():
            sources.append((rel, "empty", sha256_file(path), stat.st_size, modified))
            continue

        digest = hashlib.sha256(text.encode("utf-8", "ignore")).hexdigest()
        sources.append((rel, "text", digest, stat.st_size, modified))
        is_markdown = suffix in {".md", ".markdown"}
        title = first_title(text, path.stem) if is_markdown else path.stem
        headings = find_headings(text) if is_markdown else []
        links = sorted({m.group(1).strip() for m in WIKI_RE.finditer(text)} |
                       {m.group(1).strip() for m in MD_LINK_RE.finditer(text)})
        chunks = split_chunks(text) if is_markdown else hard_wrap(text)
        words = len(re.findall(r"\w+", text))

        documents.append({
            "path": rel,
            "kind": suffix.lstrip("."),
            "title": title,
            "modified": modified,
            "sha256": digest,
            "words": words,
            "headings": headings,
            "links": links,
            "chunks": [{"heading": h, "line": ln, "text": t} for h, ln, t in chunks],
        })

    facts_path = ROOT / "data" / "build-facts.json"
    if facts_path.exists():
        try:
            facts = json.loads(read_text(facts_path))
            all_facts.extend(flatten_facts(facts))
        except json.JSONDecodeError as exc:
            print(f"WARN: data/build-facts.json is not valid JSON: {exc}", file=sys.stderr)
    all_facts.extend(load_stack_facts())

    runs = []
    approvals = []
    if PROJECT_MODE:
        all_facts.extend(project_facts(ROOT))
        runs = parse_activity(ROOT / "build-activity.log")
        approvals = parse_inbox(ROOT)

    index = {
        "schema": "knowledge-index/v1",
        "mode": "project" if PROJECT_MODE else "template",
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "root": str(ROOT),
        "database": str(DB_PATH),
        "counts": {
            "documents": len(documents),
            "headings": sum(len(d["headings"]) for d in documents),
            "chunks": sum(len(d["chunks"]) for d in documents),
            "facts": len(all_facts),
            "assets": len(assets),
            "sources": len(sources),
            "runs": len(runs),
            "approvals": len(approvals),
        },
        # Project JSON stays a manifest; the DB holds the full text and FTS.
        "documents": documents if not PROJECT_MODE else [
            {k: d[k] for k in ("path", "kind", "title", "modified", "sha256", "words")}
            for d in documents
        ],
        "assets": assets,
        "sources": [
            {"path": p, "kind": k, "sha256": h, "bytes": b, "modified": m}
            for p, k, h, b, m in sources
        ],
        "runs": [
            {"time": t, "kind": k, "text": x} for t, k, x in runs
        ],
        "approvals": [
            {"id": a, "kind": b, "title": c, "action": d, "created_ms": e, "status": f}
            for a, b, c, d, e, f in approvals
        ],
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
        CREATE TABLE assets(
            id INTEGER PRIMARY KEY, path TEXT UNIQUE, kind TEXT, bytes INTEGER,
            modified TEXT, sha256 TEXT, width INTEGER, height INTEGER);
        CREATE TABLE sources(
            id INTEGER PRIMARY KEY, path TEXT UNIQUE, kind TEXT, sha256 TEXT,
            bytes INTEGER, modified TEXT);
        CREATE TABLE runs(
            id INTEGER PRIMARY KEY, time TEXT, kind TEXT, text TEXT);
        CREATE TABLE approvals(
            id TEXT PRIMARY KEY, kind TEXT, title TEXT, action TEXT,
            created_ms TEXT, status TEXT);
        CREATE VIRTUAL TABLE chunks_fts USING fts5(
            text, heading, path UNINDEXED, doc_id UNINDEXED,
            tokenize='porter unicode61');
        CREATE UNIQUE INDEX idx_facts ON facts(category, key);
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
        con.execute("INSERT OR REPLACE INTO facts(category,key,value) VALUES(?,?,?)",
                    (category, key, value))
    for a in assets:
        con.execute("INSERT OR REPLACE INTO assets(path,kind,bytes,modified,sha256,width,height) "
                    "VALUES(?,?,?,?,?,?,?)",
                    (a["path"], a["kind"], a["bytes"], a["modified"], a["sha256"],
                     a.get("width"), a.get("height")))
    for p, k, h, b, m in sources:
        con.execute("INSERT OR REPLACE INTO sources(path,kind,sha256,bytes,modified) VALUES(?,?,?,?,?)",
                    (p, k, h, b, m))
    for t, k, x in runs:
        con.execute("INSERT INTO runs(time,kind,text) VALUES(?,?,?)", (t, k, x))
    for a, b, c, d, e, f in approvals:
        con.execute("INSERT OR REPLACE INTO approvals(id,kind,title,action,created_ms,status) "
                    "VALUES(?,?,?,?,?,?)", (a, b, c, d, e, f))

    con.commit()
    con.close()

    print(f"mode      : {'project' if PROJECT_MODE else 'template'}")
    print(f"root      : {ROOT}")
    for key in ("documents", "headings", "chunks", "facts", "assets", "sources", "runs", "approvals"):
        print(f"{key:<10}: {index['counts'][key]}")
    print(f"json      : {JSON_PATH} ({JSON_PATH.stat().st_size / 1024:.0f} KB)")
    print(f"database  : {DB_PATH} ({DB_PATH.stat().st_size / 1024:.0f} KB)")


def main():
    global ROOT, DATA, DB_PATH, JSON_PATH, PROJECT_MODE

    parser = argparse.ArgumentParser(description="Build a template or project knowledge database")
    parser.add_argument("--root", help="Folder to index (default: this repository)")
    parser.add_argument("--out", help="Database file to write (default: <root>/data/knowledge.db)")
    parser.add_argument("--json-out", help="JSON dump to write (default: beside the database)")
    parser.add_argument("--project", action="store_true",
                        help="Project mode: add assets, sources, runs and approvals")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()

    if args.root:
        ROOT = Path(args.root).resolve()
    DATA = ROOT / "data"

    if args.out:
        DB_PATH = Path(args.out).resolve()
    else:
        DB_PATH = DATA / "knowledge.db"

    if args.json_out:
        JSON_PATH = Path(args.json_out).resolve()
    elif args.out:
        JSON_PATH = DB_PATH.with_suffix(".json")
    else:
        JSON_PATH = DATA / "index.json"

    PROJECT_MODE = args.project
    build()


if __name__ == "__main__":
    main()
