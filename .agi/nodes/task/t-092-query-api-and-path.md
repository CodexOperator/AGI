---
acceptance_criteria:
  - R11.3 (find_paths)
  - R11.4 (find_ancestors)
  - R11.5 (find_descendants)
  - R11.6 (query filters)
  - R11.7 (lazy iterators)
blocked_by:
  - task:t-090
cavekit_req: graph-core/R11
effort: M
id: "task:t-092"
mint_id: 24c5112f2fb04a46b37dc388bcc3d63d
origin: build-site
parents:
  - hyp:graph-core-r11
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-092: Query API and path finding"
type: task
---

**Description:** Implement `find_paths(source_id, target_id)` returning all simple paths via DFS backtracking. Implement `find_ancestors(node_id)` and `find_descendants(node_id)` using BFS. Implement `query(type=None, tags=None, has_parent=None, has_child=None)` filtering nodes by criteria without loading bodies. All return lazy generators.

**Files:** `src/graph_core/query.py`, `tests/graph_core/test_query.py`
