---
acceptance_criteria:
  - R11.1 (traverse_bfs)
  - R11.2 (traverse_dfs)
  - R11.8 (cycle detection utility)
blocked_by:
  - task:t-004
cavekit_req: graph-core/R11
effort: M
id: "task:t-090"
mint_id: d1e60b233c3f40e884c2d0cd5754f312
origin: build-site
parents:
  - hyp:graph-core-r11
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-090: BFS/DFS traversal primitives"
type: task
---

**Description:** Implement `traverse_bfs(start_id)` and `traverse_dfs(start_id)` as lazy generators yielding node ids in traversal order. Also expose a `detect_cycle(node_id)` utility that runs DFS from that node and reports any found cycle path. Use the existing Graph container from T-004.

**Files:** `src/graph_core/traversal.py`, `tests/graph_core/test_traversal.py`
