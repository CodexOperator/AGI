---
acceptance_criteria:
  - R2.1 (cycle insert returns structured error and leaves graph unchanged)
  - R2.4 (removing node removes all incident edges
  - no dangling refs)
blocked_by:
  - task:t-002
  - task:t-003
cavekit_req: graph-core/R2
effort: M
id: "task:t-004"
mint_id: c7e0c33254e447d9ae61f0d9a1137ac2
origin: build-site
parents:
  - hyp:graph-core-r2
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-004: Graph DAG insertion with cycle rejection"
type: task
---

**Description:** Implement a `Graph` container that holds nodes by id and edges as a set, exposes `add_node`, `add_edge`, `remove_node`, and `remove_edge`. `add_edge` performs cycle detection via DFS from target back to source; on a cycle, raises `CycleError` and rolls back. `remove_node` filters out every incident edge.

**Files:** `agi-tree/src/graph_core/graph.py`, `agi-tree/tests/graph_core/test_graph_dag.py`

**Test Strategy:** Unit test attempts to insert an edge that closes a 3-cycle and asserts the graph state matches a snapshot taken before the call. Unit test removes a node with two incoming and three outgoing edges and asserts the edge set drops by exactly five.
