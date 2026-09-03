---
id: task:t-002
mint_id: 874c5f8d16df4a008c99b76fb402cc73
type: task
parents:
  - hyp:graph-core-r1
acceptance_criteria:
  - R1.3 (parents/children are sets — no duplicates; self-loops rejected with clear error)
blocked_by:
  - task:t-001
cavekit_req: graph-core/R1
edited_by: l1.09-execution-parent
effort: S
origin: build-site
status: deprecated
tags:
  - S
  - tier--1
thought_session: L1.09
tier: "-1"
title: "T-002: Node parent/child invariant guards (no duplicates, no self-loops)"
---
**Description:** Add validators that reject inserting a node id into its own parents/children set with a `SelfLoopError` carrying the offending id; ensure set semantics naturally drop duplicates. Surface a structured exception type.

**Files:** `agi-tree/src/graph_core/node.py`, `agi-tree/src/graph_core/errors.py`, `agi-tree/tests/graph_core/test_node_invariants.py`

**Test Strategy:** Unit test attempts to add `n.id` to `n.children`; expects `SelfLoopError` with the id in the message. Unit test inserts duplicate child and asserts size unchanged.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `graph-core/R1` under `hyp:graph-core-r1`, whose disposition is already closed by `verdict:graph-core-r1` before this pass; deprecated with its domain (`idea:domain-graph-core`).
<!-- THOUGHT:END -->
