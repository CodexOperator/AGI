---
id: task:t-004
mint_id: c7e0c33254e447d9ae61f0d9a1137ac2
type: task
parents:
  - hyp:graph-core-r2
acceptance_criteria:
  - R2.1 (cycle insert returns structured error and leaves graph unchanged)
  - R2.4 (removing node removes all incident edges
  - no dangling refs)
blocked_by:
  - task:t-002
  - task:t-003
cavekit_req: graph-core/R2
edited_by: l1.09-execution-parent
effort: M
origin: build-site
status: deprecated
tags:
  - M
  - tier--1
thought_session: L1.09
tier: "-1"
title: "T-004: Graph DAG insertion with cycle rejection"
---
**Description:** Implement a `Graph` container that holds nodes by id and edges as a set, exposes `add_node`, `add_edge`, `remove_node`, and `remove_edge`. `add_edge` performs cycle detection via DFS from target back to source; on a cycle, raises `CycleError` and rolls back. `remove_node` filters out every incident edge.

**Files:** `agi-tree/src/graph_core/graph.py`, `agi-tree/tests/graph_core/test_graph_dag.py`

**Test Strategy:** Unit test attempts to insert an edge that closes a 3-cycle and asserts the graph state matches a snapshot taken before the call. Unit test removes a node with two incoming and three outgoing edges and asserts the edge set drops by exactly five.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `graph-core/R2` under `hyp:graph-core-r2`, whose disposition is disposition CLOSE-BY-CITATION -- closed by `verdict:graph-core-r2-by-citation` citing `build:src-graph-core-edge`, `build:src-graph-core-graph`, `build:tests-graph-core-test-graph-dag`, `build:tests-graph-core-test-edge`, `build:tests-graph-core-test-node-invariants`: `edge.py`/`graph.py` carry `add_edge`/`remove_edge` and `_cycle_path`; the DAG, edge and node-invariant suites exercise cycle rejection, idempotent insert and no dangling references -- the same evidence pattern `verdict:graph-core-r1` was closed on (16 real test files).
<!-- THOUGHT:END -->
