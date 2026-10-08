---
id: task:t-006
mint_id: 5cc81a01a00c4a97bebb664d33e7ee45
type: task
parents:
  - hyp:graph-core-r4
acceptance_criteria:
  - R4.2 (load-then-save round-trips byte-equivalent modulo whitespace)
  - R4.3 (Markdown-with-YAML or pure JSON files accepted)
blocked_by:
  - task:t-001
cavekit_req: graph-core/R4
edited_by: season.py
effort: M
origin: build-site
season: 1
status: deprecated
tags:
  - M
  - tier--1
thought_session: season
tier: -1
title: "T-006: Node file frontmatter persistence (Markdown + JSON containers)"
---
**Description:** Implement a frontmatter reader/writer. For `.md` files, parse a `---` YAML block then body. For `.json` files, treat the file as `{frontmatter:..., body:...}`. Write paths preserve a normalized form (consistent line endings, sorted top-level keys). Round-trip test feeds a known fixture, loads, saves, then asserts file equivalence after whitespace normalization.

**Files:** `agi-tree/src/graph_core/persistence/frontmatter.py`, `agi-tree/tests/graph_core/test_frontmatter.py`, `agi-tree/tests/fixtures/nodes/sample.md`, `agi-tree/tests/fixtures/nodes/sample.json`

**Test Strategy:** Round-trip test on both md and json fixtures. Test that no body content is read when only frontmatter is requested.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `graph-core/R4` under `hyp:graph-core-r4`, whose disposition is disposition CLOSE-BY-CITATION -- closed by `verdict:graph-core-r4-by-citation` citing `build:src-graph-core-persistence-frontmatter`, `build:src-graph-core-persistence-lazy-body`, `build:tests-graph-core-test-frontmatter`, `build:tests-graph-core-test-frontmatter-errors`, `build:tests-graph-core-test-lazy-body`: `persistence/frontmatter.py` is the round-tripping reader/writer with one failure class (`FrontmatterError`) and `lazy_body.py` the lazy body read; the three suites cover round-trip, error isolation and laziness.
<!-- THOUGHT:END -->