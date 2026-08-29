---
acceptance_criteria:
  - R4.1 (loading reads only frontmatter; body fetched on first body access)
blocked_by:
  - task:t-006
cavekit_req: graph-core/R4
effort: S
id: "task:t-007"
mint_id: d7ac4a216e6c4dc8a63a52db85a4e17b
origin: build-site
parents:
  - hyp:graph-core-r4
status: pending
tags:
  - S
  - tier--1
tier: -1
title: "T-007: Lazy body loading"
type: task
---

**Description:** Wrap node body in a `LazyBody` object. The graph load path reads only the frontmatter region of each file. `node.body` is a property that triggers the on-disk read on first access.

**Files:** `agi-tree/src/graph_core/persistence/lazy_body.py`, `agi-tree/tests/graph_core/test_lazy_body.py`

**Test Strategy:** Counter-based test wrapping the file reader; asserts no body reads occur during graph load and exactly one body read occurs after first `node.body` access.
