# Knowledge base

A portable, offline index of everything in this repository plus the build facts
for the laptop/desktop. Pull the repo, run one command, and any agent can search
it without network access.

## Files

| File | What it is | Commit it? |
|---|---|---|
| `data/build-facts.json` | Curated, verified machine/toolchain/MCP facts | Yes — edit by hand |
| `data/index.json` | Generated structured dump (documents, headings, links, facts) | Yes — diffable |
| `data/knowledge.db` | Generated SQLite + FTS5 database | Yes — ~0.9 MB |
| `scripts/build_index.py` | Rebuilds both generated files | Yes |
| `scripts/query.py` | CLI search/read | Yes |

The database is committed on purpose: the desktop should not need Python to
read the data. Anything that can open SQLite (DB Browser, DBeaver, Datasette,
Python, Node, Go) can read it.

## Rebuild after editing docs

```bash
python scripts/build_index.py
```

Safe to run repeatedly. It excludes `repos/`, `.git`, `node_modules`, Hermes
caches/logs/sessions and every `*.db`, so only publishable text is indexed.

## Query

```bash
python scripts/query.py --stats
python scripts/query.py --search "bios ram"
python scripts/query.py --search "mcp hermes" --limit 5
python scripts/query.py --facts machine
python scripts/query.py --facts mcp
python scripts/query.py --facts toolchain
python scripts/query.py --docs
python scripts/query.py --doc docs/TROUBLESHOOTING.md
```

From another language, open `data/knowledge.db` directly:

```sql
-- full-text search with context
SELECT path, heading, snippet(chunks_fts, 0, '«', '»', '…', 14)
FROM chunks_fts
WHERE chunks_fts MATCH '"mcp" AND "hermes"'
ORDER BY bm25(chunks_fts)
LIMIT 10;

-- every verified fact about the machine
SELECT key, value FROM facts WHERE category = 'machine';

-- pending work
SELECT key, value FROM facts WHERE category = 'pending';

-- documents and headings
SELECT d.path, h.level, h.text, h.line
FROM headings h JOIN documents d ON d.id = h.doc_id
WHERE d.path LIKE 'docs/%'
ORDER BY d.path, h.line;
```

## Schema

```
documents(id, path, kind, title, modified, sha256, words)
headings(id, doc_id, level, text, line)
chunks(id, doc_id, heading, line_start, text)
links(id, doc_id, target)
facts(id, category, key, value)
chunks_fts(text, heading, path UNINDEXED, doc_id UNINDEXED)  -- FTS5, porter
```

`facts.category` is one of: `machine`, `windows_tuning`, `toolchain`, `agents`,
`mcp`, `projects`, `lessons`, `pending`, `component`, `stack`.

## Describing a new machine

The facts are not laptop-specific by design. On a new desktop:

1. Copy `data/build-facts.json` and update `machine`, `toolchain`, `projects`.
2. Run `python scripts/build_index.py`.
3. Commit. The old values stay in git history if you need to compare.

Do not put secrets, tokens, session transcripts or `repos/` contents in this
folder. The index is meant to be public-safe.
