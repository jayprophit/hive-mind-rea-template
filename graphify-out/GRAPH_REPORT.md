# Graph Report - hive-mind-rea-template  (2026-11-24)

## Corpus Check
- 56 files · ~269,902 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 13 file(s) not represented in the graph (top: (none) 12, .db 1)

## Summary
- 698 nodes · 937 edges · 41 communities (36 shown, 5 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 28 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e17fa719`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- mcp
- research.py
- stack.yaml
- doctor.py
- services
- bootstrap.py
- build_index.py
- components
- coder/config.yaml
- decider/config.yaml
- designer/config.yaml
- finance/config.yaml
- hr/config.yaml
- marketer/config.yaml
- qa/config.yaml
- researcher/config.yaml
- reviewer/config.yaml
- supervisor/config.yaml
- windows/config.yaml
- writer/config.yaml
- query.py
- model
- model
- model
- model
- model
- model
- model
- model
- model
- model
- model
- repair-windows-admin.ps1
- providers
- datasources
- agent-preflight.ps1
- sync_second_brain.py
- steps

## God Nodes (most connected - your core abstractions)
1. `main()` - 19 edges
2. `Report` - 15 edges
3. `main()` - 15 edges
4. `build()` - 15 edges
5. `main()` - 11 edges
6. `main()` - 11 edges
7. `mcp` - 11 edges
8. `components` - 9 edges
9. `main()` - 8 edges
10. `check_layout()` - 8 edges

## Surprising Connections (you probably didn't know these)
- `account()` --references--> `Path`  [EXTRACTED]
  scripts/rea_evidence.py →   _Bridges community 1 → community 39_
- `fts_query()` --calls--> `re`  [EXTRACTED]
  scripts/query.py →   _Bridges community 20 → community 1_
- `check_layout()` --calls--> `json`  [EXTRACTED]
  scripts/doctor.py →   _Bridges community 3 → community 1_
- `check_mcp()` --calls--> `subprocess`  [EXTRACTED]
  scripts/doctor.py →   _Bridges community 3 → community 5_
- `check_resources()` --calls--> `shutil`  [EXTRACTED]
  scripts/doctor.py →   _Bridges community 3 → community 39_

## Import Cycles
- None detected.

## Communities (41 total, 5 thin omitted)

### Community 0 - "mcp"
Cohesion: 0.04
Nodes (48): command, enabled, environment, type, command, enabled, type, command (+40 more)

### Community 1 - "research.py"
Cohesion: 0.08
Nodes (33): as_sections(), as_table(), load(), main(), parse_markdown(), write_csv(), write_docx(), write_pptx() (+25 more)

### Community 2 - "stack.yaml"
Cohesion: 0.05
Nodes (38): enabled, note, description, enabled, note, demobase, graphify, mcp_servers (+30 more)

### Community 3 - "doctor.py"
Cohesion: 0.13
Nodes (21): check_core_binaries(), check_layout(), check_mcp(), check_ollama(), check_optional_binaries(), check_platform(), check_ports(), check_python() (+13 more)

### Community 4 - "services"
Cohesion: 0.06
Nodes (30): depends_on, environment, image, ports, environment, image, restart, volumes (+22 more)

### Community 5 - "bootstrap.py"
Cohesion: 0.18
Nodes (20): build_mcp_block(), config_root(), data_root(), find_bin(), head(), hermes_home(), home(), main() (+12 more)

### Community 6 - "build_index.py"
Cohesion: 0.18
Nodes (15): build(), find_headings(), first_title(), flatten_facts(), hard_wrap(), load_stack_facts(), main(), parse_activity() (+7 more)

### Community 7 - "components"
Cohesion: 0.10
Nodes (20): components, detect, env, id, install, label, models, required (+12 more)

### Community 8 - "coder/config.yaml"
Cohesion: 0.12
Nodes (15): auxiliary, group_router, model, provider, memory, memory_enabled, search, model (+7 more)

### Community 9 - "decider/config.yaml"
Cohesion: 0.12
Nodes (15): auxiliary, group_router, model, provider, memory, memory_enabled, search, model (+7 more)

### Community 10 - "designer/config.yaml"
Cohesion: 0.12
Nodes (15): auxiliary, group_router, model, provider, memory, memory_enabled, search, model (+7 more)

### Community 11 - "finance/config.yaml"
Cohesion: 0.12
Nodes (15): auxiliary, group_router, model, provider, memory, memory_enabled, search, model (+7 more)

### Community 12 - "hr/config.yaml"
Cohesion: 0.12
Nodes (15): auxiliary, group_router, model, provider, memory, memory_enabled, search, model (+7 more)

### Community 13 - "marketer/config.yaml"
Cohesion: 0.12
Nodes (15): auxiliary, group_router, model, provider, memory, memory_enabled, search, model (+7 more)

### Community 14 - "qa/config.yaml"
Cohesion: 0.12
Nodes (15): auxiliary, group_router, model, provider, memory, memory_enabled, search, model (+7 more)

### Community 15 - "researcher/config.yaml"
Cohesion: 0.12
Nodes (15): auxiliary, group_router, model, provider, memory, memory_enabled, search, model (+7 more)

### Community 16 - "reviewer/config.yaml"
Cohesion: 0.12
Nodes (15): auxiliary, group_router, model, provider, memory, memory_enabled, search, model (+7 more)

### Community 17 - "supervisor/config.yaml"
Cohesion: 0.12
Nodes (15): auxiliary, group_router, model, provider, memory, memory_enabled, search, model (+7 more)

### Community 18 - "windows/config.yaml"
Cohesion: 0.12
Nodes (15): auxiliary, group_router, model, provider, memory, memory_enabled, search, model (+7 more)

### Community 19 - "writer/config.yaml"
Cohesion: 0.12
Nodes (15): auxiliary, group_router, model, provider, memory, memory_enabled, search, model (+7 more)

### Community 20 - "query.py"
Cohesion: 0.20
Nodes (11): cmd_assets(), cmd_doc(), cmd_docs(), cmd_facts(), cmd_runs(), cmd_search(), cmd_sources(), cmd_stats() (+3 more)

### Community 21 - "model"
Cohesion: 0.17
Nodes (11): auxiliary, group_router, model, provider, memory, search, model, base_url (+3 more)

### Community 22 - "model"
Cohesion: 0.17
Nodes (11): auxiliary, group_router, model, provider, memory, search, model, base_url (+3 more)

### Community 23 - "model"
Cohesion: 0.17
Nodes (11): auxiliary, group_router, model, provider, memory, search, model, base_url (+3 more)

### Community 24 - "model"
Cohesion: 0.17
Nodes (11): auxiliary, group_router, model, provider, memory, search, model, base_url (+3 more)

### Community 25 - "model"
Cohesion: 0.17
Nodes (11): auxiliary, group_router, model, provider, memory, search, model, base_url (+3 more)

### Community 26 - "model"
Cohesion: 0.17
Nodes (11): auxiliary, group_router, model, provider, memory, search, model, base_url (+3 more)

### Community 27 - "model"
Cohesion: 0.17
Nodes (11): auxiliary, group_router, model, provider, memory, search, model, base_url (+3 more)

### Community 28 - "model"
Cohesion: 0.17
Nodes (11): auxiliary, group_router, model, provider, memory, search, model, base_url (+3 more)

### Community 29 - "model"
Cohesion: 0.17
Nodes (11): auxiliary, group_router, model, provider, memory, search, model, base_url (+3 more)

### Community 30 - "model"
Cohesion: 0.17
Nodes (11): auxiliary, group_router, model, provider, memory, search, model, base_url (+3 more)

### Community 31 - "model"
Cohesion: 0.17
Nodes (11): auxiliary, group_router, model, provider, memory, search, model, base_url (+3 more)

### Community 33 - "providers"
Cohesion: 0.22
Nodes (8): apiVersion, path, providers, disableDeletion, name, options, type, updateIntervalSeconds

### Community 34 - "datasources"
Cohesion: 0.29
Nodes (6): apiVersion, datasources, access, name, type, url

### Community 39 - "sync_second_brain.py"
Cohesion: 0.40
Nodes (5): main(), needs_copy(), sync_project_db(), sync_vault(), write_log()

### Community 40 - "steps"
Cohesion: 0.12
Nodes (16): jobs, verify, name, on, pull_request, push, workflow_dispatch, branches (+8 more)

## Knowledge Gaps
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `components` connect `components` to `stack.yaml`?**
  _High betweenness centrality (0.004) - this node is a cross-community bridge._
- **Are the 13 inferred relationships involving `main()` (e.g. with `check_core_binaries()` and `check_layout()`) actually correct?**
  _`main()` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Should `mcp` be split into smaller, more focused modules?**
  _Cohesion score 0.04081632653061224 - nodes in this community are weakly interconnected._
- **Why does `main()` connect `doctor.py` to `research.py`?**
  _High betweenness centrality (0.004) - this node is a cross-community bridge._
- **Should `research.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07597895967270601 - nodes in this community are weakly interconnected._
- **Should `stack.yaml` be split into smaller, more focused modules?**
  _Cohesion score 0.05128205128205128 - nodes in this community are weakly interconnected._
- **Should `doctor.py` be split into smaller, more focused modules?**
  _Cohesion score 0.12944523470839261 - nodes in this community are weakly interconnected._