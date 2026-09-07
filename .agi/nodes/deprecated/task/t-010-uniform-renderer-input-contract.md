---
id: task:t-010
mint_id: a483c8f3c7b947cf9f174e6ca18d7810
type: task
parents:
  - hyp:graph-core-r5
acceptance_criteria:
  - R5.3 (renderers invoked uniformly on top-level and nested subgraphs using same input contract)
blocked_by:
  - task:t-009
cavekit_req: graph-core/R5
edited_by: season.py
effort: S
origin: build-site
season: 1
status: deprecated
tags:
  - S
  - tier--1
thought_session: season
tier: -1
title: "T-010: Uniform renderer input contract (recursive)"
---
**Description:** Document and enforce that any function accepting a `Graph` accepts both top-level and nested subgraph instances without type discrimination. Add an internal `RenderableGraph` typing alias so renderers (built later) inherit this contract.

**Files:** `agi-tree/src/graph_core/types.py`, `agi-tree/tests/graph_core/test_uniform_contract.py`

**Test Strategy:** Type test confirms `Graph` instances from outer and inner graphs share the same protocol; passing both into a stub callable returns equivalent shape.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `graph-core/R5` under `hyp:graph-core-r5`, whose disposition is disposition CLOSE-BY-CITATION -- closed by `verdict:graph-core-r5-by-citation` citing `build:tests-graph-core-test-recursive-bodies`, `build:tests-graph-core-test-uniform-contract`: `test_recursive_bodies.py` loads nested subgraphs three levels deep and `test_uniform_contract.py` asserts node and subgraph share one contract.
<!-- THOUGHT:END -->