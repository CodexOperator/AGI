---
acceptance_criteria:
  - R6.2 (subdirectory loaded as subgraph node whose type resolved through schema-registry)
  - R6.3 (files not matching any schema load as generic with warning listing them)
blocked_by:
  - task:t-011
  - task:t-019
  - task:t-020
cavekit_req: graph-core/R6
effort: M
id: "task:t-012"
mint_id: e1b455750252422cbcb11d9cfb7235ce
origin: build-site
parents:
  - hyp:graph-core-r6
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-012: Subdirectory→subgraph node resolution via schema-registry"
type: task
---

**Description:** When loader encounters a subdirectory, it asks the schema-registry to resolve the directory name into a node type. Falls back to generic node type when no match. Emits a single aggregated warning naming each unmatched file.

**Files:** `agi-tree/src/graph_core/loader.py`, `agi-tree/tests/graph_core/test_loader_schema_resolution.py`

**Test Strategy:** Loader test against fixture with one schema-matched directory and one unmatched; assert correct types and one aggregated warning.
