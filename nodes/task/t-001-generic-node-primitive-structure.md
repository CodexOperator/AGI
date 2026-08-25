---
acceptance_criteria:
  - R1.1 (id/type/payload_ref/parents/children/tags exposed; nothing else mandatory)
  - R1.2 (no-parent root and no-child leaf accepted)
  - R1.4 (tags is a set of strings independent of typed links)
blocked_by: []
cavekit_req: graph-core/R1
effort: M
id: "task:t-001"
mint_id: da86da1592964ca0b15a894814e47fcf
origin: build-site
parents:
  - hyp:graph-core-r1
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-001: Generic node primitive structure"
type: task
---

**Description:** Implement a `Node` dataclass/record with exactly the six fields. Type is a string (deferred semantic meaning to schema-registry). `parents`/`children` are sets of node-id strings. `tags` is a separate set[str]. Provide constructors that default to empty parents/children/tags, and accept a payload_ref of None. Expose only these fields publicly; do not auto-add fields like timestamps at this layer.

**Files:** `agi-tree/src/graph_core/node.py`, `agi-tree/tests/graph_core/test_node.py`

**Test Strategy:** Unit tests asserting (a) field set is exactly the six declared, (b) Node() with no parents is a root, (c) Node() with no children is a leaf, (d) tags being mutated does not affect parents/children.
