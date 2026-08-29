---
acceptance_criteria:
  - R5.3 (renderers invoked uniformly on top-level and nested subgraphs using same input contract)
blocked_by:
  - task:t-009
cavekit_req: graph-core/R5
effort: S
id: "task:t-010"
mint_id: a483c8f3c7b947cf9f174e6ca18d7810
origin: build-site
parents:
  - hyp:graph-core-r5
status: pending
tags:
  - S
  - tier--1
tier: -1
title: "T-010: Uniform renderer input contract (recursive)"
type: task
---

**Description:** Document and enforce that any function accepting a `Graph` accepts both top-level and nested subgraph instances without type discrimination. Add an internal `RenderableGraph` typing alias so renderers (built later) inherit this contract.

**Files:** `agi-tree/src/graph_core/types.py`, `agi-tree/tests/graph_core/test_uniform_contract.py`

**Test Strategy:** Type test confirms `Graph` instances from outer and inner graphs share the same protocol; passing both into a stub callable returns equivalent shape.
