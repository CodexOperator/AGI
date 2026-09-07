---
id: task:t-015
mint_id: f711cf41e93d41d89e13ced2be466e65
type: task
parents:
  - hyp:graph-core-r8
acceptance_criteria:
  - R8.1 (backend implements load/save/list/watch; graph-core depends only on contract)
  - R8.2 (swap to in-memory stub in tests changes no caller code)
  - R8.3 (default install requires no external service)
  - R8.4 (backend selectable via configuration)
blocked_by:
  - task:t-006
  - task:t-011
cavekit_req: graph-core/R8
edited_by: season.py
effort: M
origin: build-site
season: 1
status: deprecated
tags:
  - M
  - tier--1
thought_session: season
tier: -1
title: "T-015: Pluggable persistence backend contract"
---
**Description:** Define a `PersistenceBackend` Protocol with `load(path)`, `save(path, node)`, `list(path)`, `watch(path)`. Filesystem backend is the default implementation. Provide an `InMemoryBackend` for tests. Configuration via `context/config/graph-core.toml` selects which backend to use.

**Files:** `agi-tree/src/graph_core/persistence/backend.py`, `agi-tree/src/graph_core/persistence/filesystem.py`, `agi-tree/src/graph_core/persistence/in_memory.py`, `agi-tree/tests/graph_core/test_backend_swap.py`

**Test Strategy:** Run the same loader test suite once with the filesystem backend and once with the in-memory backend; assert outputs equal. Confirm filesystem backend has no `import requests` or socket usage.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `graph-core/R8` under `hyp:graph-core-r8`, whose disposition is disposition CLOSE-BY-CITATION -- closed by `verdict:graph-core-r8-by-citation` citing `build:src-graph-core-persistence-backend`, `build:src-graph-core-persistence-filesystem`, `build:src-graph-core-persistence-in-memory`, `build:src-graph-core-persistence-sqlite-backend`, `build:tests-graph-core-test-backend-swap`: `persistence/backend.py` is the protocol, with filesystem, in-memory and sqlite implementations, and `test_backend_swap.py` swaps them under one graph.
<!-- THOUGHT:END -->