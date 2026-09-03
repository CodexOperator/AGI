---
id: task:t-092
mint_id: 24c5112f2fb04a46b37dc388bcc3d63d
type: task
parents:
  - hyp:graph-core-r11
acceptance_criteria:
  - R11.3 (find_paths)
  - R11.4 (find_ancestors)
  - R11.5 (find_descendants)
  - R11.6 (query filters)
  - R11.7 (lazy iterators)
blocked_by:
  - task:t-090
cavekit_req: graph-core/R11
edited_by: l1.09-execution-parent
effort: M
origin: build-site
status: deprecated
tags:
  - M
  - tier--1
thought_session: L1.09
tier: "-1"
title: "T-092: Query API and path finding"
---
**Description:** Implement `find_paths(source_id, target_id)` returning all simple paths via DFS backtracking. Implement `find_ancestors(node_id)` and `find_descendants(node_id)` using BFS. Implement `query(type=None, tags=None, has_parent=None, has_child=None)` filtering nodes by criteria without loading bodies. All return lazy generators.

**Files:** `src/graph_core/query.py`, `tests/graph_core/test_query.py`

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `graph-core/R11` under `hyp:graph-core-r11`, whose disposition is disposition CLOSE-BY-SMALL-EXPERIMENT, not run: `graph.py` exposes none of BFS/DFS/find_paths/ancestors/descendants publicly, but `chain_engine/query_api.py` already carries a private `_bfs_descendants`; promoting it into `graph_core` with a thin test file is small -- no existing goal obviously covers it, so this THOUGHT is the record.
<!-- THOUGHT:END -->
