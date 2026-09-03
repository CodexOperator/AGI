---
id: task:t-007
mint_id: d7ac4a216e6c4dc8a63a52db85a4e17b
type: task
parents:
  - hyp:graph-core-r4
acceptance_criteria:
  - R4.1 (loading reads only frontmatter; body fetched on first body access)
blocked_by:
  - task:t-006
cavekit_req: graph-core/R4
edited_by: l1.09-execution-parent
effort: S
origin: build-site
status: deprecated
tags:
  - S
  - tier--1
thought_session: L1.09
tier: "-1"
title: "T-007: Lazy body loading"
---
**Description:** Wrap node body in a `LazyBody` object. The graph load path reads only the frontmatter region of each file. `node.body` is a property that triggers the on-disk read on first access.

**Files:** `agi-tree/src/graph_core/persistence/lazy_body.py`, `agi-tree/tests/graph_core/test_lazy_body.py`

**Test Strategy:** Counter-based test wrapping the file reader; asserts no body reads occur during graph load and exactly one body read occurs after first `node.body` access.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `graph-core/R4` under `hyp:graph-core-r4`, whose disposition is disposition CLOSE-BY-CITATION -- closed by `verdict:graph-core-r4-by-citation` citing `build:src-graph-core-persistence-frontmatter`, `build:src-graph-core-persistence-lazy-body`, `build:tests-graph-core-test-frontmatter`, `build:tests-graph-core-test-frontmatter-errors`, `build:tests-graph-core-test-lazy-body`: `persistence/frontmatter.py` is the round-tripping reader/writer with one failure class (`FrontmatterError`) and `lazy_body.py` the lazy body read; the three suites cover round-trip, error isolation and laziness.
<!-- THOUGHT:END -->
