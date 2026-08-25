---
acceptance_criteria:
  - R4.2 (load-then-save round-trips byte-equivalent modulo whitespace)
  - R4.3 (Markdown-with-YAML or pure JSON files accepted)
blocked_by:
  - task:t-001
cavekit_req: graph-core/R4
effort: M
id: "task:t-006"
mint_id: 5cc81a01a00c4a97bebb664d33e7ee45
origin: build-site
parents:
  - hyp:graph-core-r4
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-006: Node file frontmatter persistence (Markdown + JSON containers)"
type: task
---

**Description:** Implement a frontmatter reader/writer. For `.md` files, parse a `---` YAML block then body. For `.json` files, treat the file as `{frontmatter:..., body:...}`. Write paths preserve a normalized form (consistent line endings, sorted top-level keys). Round-trip test feeds a known fixture, loads, saves, then asserts file equivalence after whitespace normalization.

**Files:** `agi-tree/src/graph_core/persistence/frontmatter.py`, `agi-tree/tests/graph_core/test_frontmatter.py`, `agi-tree/tests/fixtures/nodes/sample.md`, `agi-tree/tests/fixtures/nodes/sample.json`

**Test Strategy:** Round-trip test on both md and json fixtures. Test that no body content is read when only frontmatter is requested.
