# Template database vs project database

There are **two separate SQLite files** with the same core schema:

| File | Purpose |
|---|---|
| `data/knowledge.db` | The **template** — generic, publishable knowledge about the stack, machine, agents and docs. Safe to pull on any workstation. |
| `projects/polsia-free-v1/knowledge.db` | This project's **own copy**, with the same tables plus project-only evidence, source ledger, build log and approvals. |

The project file is a copy of the template design, not a second copy of the
template's content. It contains only `polsia free v1` data.

A working copy is also written into the project workspace at
`C:\Users\jpowe\Desktop\projects\polsia free v1\.hive\knowledge.db` so the agent
can read it locally without touching the repo.

## Rebuild the project database

```powershell
cd C:\Users\jpowe\hive-mind-rea-template
python scripts\build_index.py `
  --root "C:\Users\jpowe\Desktop\projects\polsia free v1" `
  --project `
  --out "C:\Users\jpowe\hive-mind-rea-template\projects\polsia-free-v1\knowledge.db"

Copy-Item projects\polsia-free-v1\knowledge.db `
  "C:\Users\jpowe\Desktop\projects\polsia free v1\.hive\knowledge.db" -Force
```

Run this after a build finishes so screenshots, `capture.json`, `docs-data.js`
and the build log are current.

## Same core schema

`documents`, `headings`, `chunks`, `links`, `facts`, `chunks_fts` exist in both.
The project file adds:

| Table | What it guarantees |
|---|---|
| `sources` | One row per file with `sha256`, bytes and modified time — nothing is silently missed or duplicated. `path` is unique. |
| `assets` | Screenshots, fonts and binaries with hash, size and image dimensions. Duplicate files are detectable by identical `sha256`. |
| `runs` | Every `build-activity.log` event (time, kind, text) — the full build history. |
| `approvals` | Every inbox question/approval with answered/waiting status. |

Very large evidence JSON files (14–16 MB in this project) are recorded in
`sources` as `evidence` by hash and size, **not** chunked into FTS. This keeps
the project DB small (~5.6 MB) while still proving the file was seen.

## Query either database

```powershell
python scripts\query.py --stats
python scripts\query.py --db projects\polsia-free-v1\knowledge.db --stats
python scripts\query.py --db projects\polsia-free-v1\knowledge.db --search "cookie banner"
python scripts\query.py --db projects\polsia-free-v1\knowledge.db --runs 10
python scripts\query.py --db projects\polsia-free-v1\knowledge.db --assets
python scripts\query.py --db projects\polsia-free-v1\knowledge.db --sources

# sqlite-utils is installed for ad-hoc SQL
python -m sqlite_utils projects\polsia-free-v1\knowledge.db tables
python -m sqlite_utils projects\polsia-free-v1\knowledge.db query \
  "select kind, count(*), sum(bytes) from assets group by kind"
```

Useful dedup check:

```sql
SELECT sha256, count(*) copies, group_concat(path)
FROM sources GROUP BY sha256 HAVING copies > 1;
```

## Tools installed for this workflow

| Tool | Why |
|---|---|
| `sqlite-utils` 4.2.1 | Query/inspect the two databases from the CLI |
| Python `Pillow` | Image dimensions recorded in `assets` |
| Python `PyYAML`, `pandas`, `matplotlib`, `python-docx`, `python-pptx`, `openpyxl` | Existing reporting stack — charts, Office output, stack parsing |
| Craft Anything MCP (38 tools) | Evidence, web capture, rebuild checks, approvals |

Optional, not installed (only if you want them): DB Browser for SQLite (GUI),
Datasette (browser UI for the DB), `ripgrep`/`jq` for shell searching. None are
needed for the build to work.

## Current limitation — authenticated pages

Craft Anything's `web_site_open` uses a **fresh browser profile with no logins**.
The original target `https://polsia.com/dashboard/untitled-l1v2k8` redirected to
`/login`, so the capture contains only public pages. Any part of the logged-in
dashboard cannot be reproduced from this evidence. Provide screenshots or saved
HTML from a logged-in session, place them under `capture/dashboard/`, rebuild
the project database, and run another refinement round.

A second known gap is functional, not visual: `app/src/studio.js` currently has
a **list of selectable agents**. The requested design is a **single team** whose
members work concurrently, share messages and hand off work like a real
company. That requirement is recorded in `data/build-facts.json` under
`requirements` and must be the subject of the next refinement round.
