---
id: task:t-008
mint_id: ffd971fb5b2e428fac8e9201d2d3584c
type: task
parents:
  - hyp:graph-core-r4
acceptance_criteria:
  - R4.4 (malformed frontmatter produces structured error naming the offending file; rest of load proceeds)
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
title: "T-008: Frontmatter error isolation"
---
**Description:** Wrap each per-file load in a try/except that emits a `FrontmatterError(path, reason)` into a structured error list and skips the offending file. Graph load returns both the loaded node set and the error list.

**Files:** `agi-tree/src/graph_core/persistence/frontmatter.py`, `agi-tree/src/graph_core/errors.py`, `agi-tree/tests/graph_core/test_frontmatter_errors.py`

**Test Strategy:** Load directory containing one valid and one malformed node file; assert one node loaded and one error reported with the correct path.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `graph-core/R4` under `hyp:graph-core-r4`, whose disposition is disposition CLOSE-BY-CITATION -- closed by `verdict:graph-core-r4-by-citation` citing `build:src-graph-core-persistence-frontmatter`, `build:src-graph-core-persistence-lazy-body`, `build:tests-graph-core-test-frontmatter`, `build:tests-graph-core-test-frontmatter-errors`, `build:tests-graph-core-test-lazy-body`: `persistence/frontmatter.py` is the round-tripping reader/writer with one failure class (`FrontmatterError`) and `lazy_body.py` the lazy body read; the three suites cover round-trip, error isolation and laziness.
<!-- THOUGHT:END -->
