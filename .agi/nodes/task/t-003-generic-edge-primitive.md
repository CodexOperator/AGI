---
acceptance_criteria:
  - R2.2 (edge exposes source_id/target_id/relation/optional tags)
  - R2.3 (idempotent insert for same source/target/relation triple)
blocked_by:
  - task:t-001
cavekit_req: graph-core/R2
effort: S
id: "task:t-003"
mint_id: 904d48c48d894a8abed66ad7ae60c554
origin: build-site
parents:
  - hyp:graph-core-r2
status: pending
tags:
  - S
  - tier--1
tier: -1
title: "T-003: Generic edge primitive"
type: task
---

**Description:** Implement `Edge` record with exactly four fields. Equality and hashing are based on `(source_id, target_id, relation)` so a set of edges naturally deduplicates.

**Files:** `agi-tree/src/graph_core/edge.py`, `agi-tree/tests/graph_core/test_edge.py`

**Test Strategy:** Unit test inserts the same edge triple twice into a set; expects len 1. Asserts field surface.
