---
acceptance_criteria:
  - R3.3 (edges from meta_node instances to ordinary nodes record which schema validated which node)
blocked_by:
  - task:t-022
  - task:t-003
cavekit_req: schema-registry/R3
effort: S
id: "task:t-023"
mint_id: ce2fc7037838499d83f70771b882f238
origin: build-site
parents:
  - hyp:schema-registry-r3
status: pending
tags:
  - S
  - tier--1
tier: -1
title: "T-023: Validating edges from meta-nodes to ordinary nodes"
type: task
---

**Description:** After validating a node against its schema, insert a `validated_by` edge from the meta-node to the ordinary node.

**Files:** `agi-tree/src/schema_registry/validation_edges.py`, `agi-tree/tests/schema_registry/test_validation_edges.py`

**Test Strategy:** Load fixture; for each ordinary node, assert exactly one validated_by edge from the corresponding meta-node.
