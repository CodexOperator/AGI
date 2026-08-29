---
acceptance_criteria:
  - R2.1 (output ≤ 200 lines
  - ≤ 200 columns)
  - R2.2 (oversize → compress or truncate with visible marker
  - no overflow)
  - R2.4 (two runs on same graph → byte-equal output)
blocked_by:
  - task:t-060
cavekit_req: renderers/R2
effort: L
id: "task:t-061"
mint_id: fdc08817119748c3aab46ad1aa515310
origin: build-site
parents:
  - hyp:renderers-r2
status: pending
tags:
  - L
  - tier--1
tier: -1
title: "T-061: ASCII renderer — bounded 200x200 with truncation marker"
type: task
---

**Description:** Implement `AsciiRenderer.render(rep) -> str`. Hierarchical layout (depth-driven indent). Bounded by 200 lines and 200 cols; on overflow, emit `... [truncated, N more nodes]` and `... [line cut at column 200]` markers. Byte-equal across runs (driven by deterministic representation).

**Files:** `agi-tree/src/renderers/ascii.py`, `agi-tree/tests/renderers/test_ascii.py`

**Test Strategy:** Run against a 1000-node fixture; assert max line length and total lines. Byte-equality test on two consecutive runs.
