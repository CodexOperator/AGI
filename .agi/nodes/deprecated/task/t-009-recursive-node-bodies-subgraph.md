---
id: task:t-009
mint_id: 8927a52689364a7481e399090edcb1dc
type: task
parents:
  - hyp:graph-core-r5
acceptance_criteria:
  - R5.1 (subgraph:true treats body as graph using same loader)
  - R5.2 (>=3 levels of nesting without special case)
  - R5.4 (parent query exposes outer children plus inner subgraph handle)
blocked_by:
  - task:t-007
  - task:t-004
cavekit_req: graph-core/R5
edited_by: l1.09-execution-parent
effort: M
origin: build-site
status: deprecated
tags:
  - M
  - tier--1
thought_session: L1.09
tier: "-1"
title: "T-009: Recursive node bodies (`subgraph: true`)"
---
**Description:** When a loaded node's frontmatter contains `subgraph: true`, recursively invoke the directory loader on its body content. Expose the inner graph via `node.subgraph` (a `Graph` instance). Outer parent queries continue to work as before; the subgraph is opaque from outside.

**Files:** `agi-tree/src/graph_core/loader.py`, `agi-tree/tests/graph_core/test_recursive_bodies.py`, `agi-tree/tests/fixtures/nested/level_a/level_b/level_c/leaf.md`

**Test Strategy:** Three-level fixture loaded; assert `graph.get(a).subgraph.get(b).subgraph.get(c)` resolves with no special-case branches in the loader.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `graph-core/R5` under `hyp:graph-core-r5`, whose disposition is disposition CLOSE-BY-CITATION -- closed by `verdict:graph-core-r5-by-citation` citing `build:tests-graph-core-test-recursive-bodies`, `build:tests-graph-core-test-uniform-contract`: `test_recursive_bodies.py` loads nested subgraphs three levels deep and `test_uniform_contract.py` asserts node and subgraph share one contract.
<!-- THOUGHT:END -->
