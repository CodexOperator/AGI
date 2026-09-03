---
id: task:t-001
mint_id: da86da1592964ca0b15a894814e47fcf
type: task
parents:
  - hyp:graph-core-r1
acceptance_criteria:
  - R1.1 (id/type/payload_ref/parents/children/tags exposed; nothing else mandatory)
  - R1.2 (no-parent root and no-child leaf accepted)
  - R1.4 (tags is a set of strings independent of typed links)
blocked_by: []
cavekit_req: graph-core/R1
edited_by: l1.09-execution-parent
effort: M
origin: build-site
status: deprecated
tags:
  - M
  - tier--1
thought_session: L1.09
tier: "-1"
title: "T-001: Generic node primitive structure"
---
**Description:** Implement a `Node` dataclass/record with exactly the six fields. Type is a string (deferred semantic meaning to schema-registry). `parents`/`children` are sets of node-id strings. `tags` is a separate set[str]. Provide constructors that default to empty parents/children/tags, and accept a payload_ref of None. Expose only these fields publicly; do not auto-add fields like timestamps at this layer.

**Files:** `agi-tree/src/graph_core/node.py`, `agi-tree/tests/graph_core/test_node.py`

**Test Strategy:** Unit tests asserting (a) field set is exactly the six declared, (b) Node() with no parents is a root, (c) Node() with no children is a leaf, (d) tags being mutated does not affect parents/children.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `graph-core/R1` under `hyp:graph-core-r1`, whose disposition is already closed by `verdict:graph-core-r1` before this pass; deprecated with its domain (`idea:domain-graph-core`).
<!-- THOUGHT:END -->
