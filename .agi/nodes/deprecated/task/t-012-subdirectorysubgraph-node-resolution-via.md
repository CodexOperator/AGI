---
id: task:t-012
mint_id: e1b455750252422cbcb11d9cfb7235ce
type: task
parents:
  - hyp:graph-core-r6
acceptance_criteria:
  - R6.2 (subdirectory loaded as subgraph node whose type resolved through schema-registry)
  - R6.3 (files not matching any schema load as generic with warning listing them)
blocked_by:
  - task:t-011
  - task:t-019
  - task:t-020
cavekit_req: graph-core/R6
edited_by: l1.09-execution-parent
effort: M
origin: build-site
status: deprecated
tags:
  - M
  - tier--1
thought_session: L1.09
tier: "-1"
title: "T-012: Subdirectory→subgraph node resolution via schema-registry"
---
**Description:** When loader encounters a subdirectory, it asks the schema-registry to resolve the directory name into a node type. Falls back to generic node type when no match. Emits a single aggregated warning naming each unmatched file.

**Files:** `agi-tree/src/graph_core/loader.py`, `agi-tree/tests/graph_core/test_loader_schema_resolution.py`

**Test Strategy:** Loader test against fixture with one schema-matched directory and one unmatched; assert correct types and one aggregated warning.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `graph-core/R6` under `hyp:graph-core-r6`, whose disposition is disposition CLOSE-BY-CITATION -- closed by `verdict:graph-core-r6-by-citation` citing `build:src-graph-core-loader`, `build:tests-graph-core-test-loader`, `build:tests-graph-core-test-walk-determinism`: `loader.py` is the directory walk with schema-resolved subgraphs and `test_walk_determinism.py` pins the walk order.
<!-- THOUGHT:END -->
