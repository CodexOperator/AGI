---
id: task:t-090
mint_id: d1e60b233c3f40e884c2d0cd5754f312
type: task
parents:
  - hyp:graph-core-r11
acceptance_criteria:
  - R11.1 (traverse_bfs)
  - R11.2 (traverse_dfs)
  - R11.8 (cycle detection utility)
blocked_by:
  - task:t-004
cavekit_req: graph-core/R11
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
title: "T-090: BFS/DFS traversal primitives"
---
**Description:** Implement `traverse_bfs(start_id)` and `traverse_dfs(start_id)` as lazy generators yielding node ids in traversal order. Also expose a `detect_cycle(node_id)` utility that runs DFS from that node and reports any found cycle path. Use the existing Graph container from T-004.

**Files:** `src/graph_core/traversal.py`, `tests/graph_core/test_traversal.py`

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `graph-core/R11` under `hyp:graph-core-r11`, whose disposition is disposition CLOSE-BY-SMALL-EXPERIMENT, not run: `graph.py` exposes none of BFS/DFS/find_paths/ancestors/descendants publicly, but `chain_engine/query_api.py` already carries a private `_bfs_descendants`; promoting it into `graph_core` with a thin test file is small -- no existing goal obviously covers it, so this THOUGHT is the record.
<!-- THOUGHT:END -->