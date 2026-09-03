---
id: task:t-003
mint_id: 904d48c48d894a8abed66ad7ae60c554
type: task
parents:
  - hyp:graph-core-r2
acceptance_criteria:
  - R2.2 (edge exposes source_id/target_id/relation/optional tags)
  - R2.3 (idempotent insert for same source/target/relation triple)
blocked_by:
  - task:t-001
cavekit_req: graph-core/R2
edited_by: l1.09-execution-parent
effort: S
origin: build-site
status: deprecated
tags:
  - S
  - tier--1
thought_session: L1.09
tier: "-1"
title: "T-003: Generic edge primitive"
---
**Description:** Implement `Edge` record with exactly four fields. Equality and hashing are based on `(source_id, target_id, relation)` so a set of edges naturally deduplicates.

**Files:** `agi-tree/src/graph_core/edge.py`, `agi-tree/tests/graph_core/test_edge.py`

**Test Strategy:** Unit test inserts the same edge triple twice into a set; expects len 1. Asserts field surface.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `graph-core/R2` under `hyp:graph-core-r2`, whose disposition is disposition CLOSE-BY-CITATION -- closed by `verdict:graph-core-r2-by-citation` citing `build:src-graph-core-edge`, `build:src-graph-core-graph`, `build:tests-graph-core-test-graph-dag`, `build:tests-graph-core-test-edge`, `build:tests-graph-core-test-node-invariants`: `edge.py`/`graph.py` carry `add_edge`/`remove_edge` and `_cycle_path`; the DAG, edge and node-invariant suites exercise cycle rejection, idempotent insert and no dangling references -- the same evidence pattern `verdict:graph-core-r1` was closed on (16 real test files).
<!-- THOUGHT:END -->
