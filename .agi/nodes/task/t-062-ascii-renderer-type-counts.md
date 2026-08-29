---
acceptance_criteria:
  - R2.3 (output includes per-type count and edge summary)
blocked_by:
  - task:t-061
cavekit_req: renderers/R2
effort: S
id: "task:t-062"
mint_id: 3c891e92203041eba8d572825688fde2
origin: build-site
parents:
  - hyp:renderers-r2
status: pending
tags:
  - S
  - tier--1
tier: -1
title: "T-062: ASCII renderer — type counts and edge summary"
type: task
---

**Description:** Append a footer block with `Types: {type: count}` and `Edges: {relation: count}` lines.

**Files:** `agi-tree/src/renderers/ascii.py`, `agi-tree/tests/renderers/test_ascii_summary.py`

**Test Strategy:** Fixture with known type and edge mix; assert footer counts match.
