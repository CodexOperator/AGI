---
acceptance_criteria:
  - R5.1 (subgraph:true treats body as graph using same loader)
  - R5.2 (>=3 levels of nesting without special case)
  - R5.4 (parent query exposes outer children plus inner subgraph handle)
blocked_by:
  - task:t-007
  - task:t-004
cavekit_req: graph-core/R5
effort: M
id: "task:t-009"
mint_id: 8927a52689364a7481e399090edcb1dc
origin: build-site
parents:
  - hyp:graph-core-r5
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-009: Recursive node bodies (`subgraph: true`)"
type: task
---

**Description:** When a loaded node's frontmatter contains `subgraph: true`, recursively invoke the directory loader on its body content. Expose the inner graph via `node.subgraph` (a `Graph` instance). Outer parent queries continue to work as before; the subgraph is opaque from outside.

**Files:** `agi-tree/src/graph_core/loader.py`, `agi-tree/tests/graph_core/test_recursive_bodies.py`, `agi-tree/tests/fixtures/nested/level_a/level_b/level_c/leaf.md`

**Test Strategy:** Three-level fixture loaded; assert `graph.get(a).subgraph.get(b).subgraph.get(c)` resolves with no special-case branches in the loader.
