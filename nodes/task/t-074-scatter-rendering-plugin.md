---
acceptance_criteria:
  - R6.1 (registered through same renderer plugin contract used by renderers kit)
  - R6.2 (places each node at coordinates derived from UMAP (x
  - y)
  - no re-projecting)
  - R6.3 (output respects ASCII bounds: ≤200 lines/cols; degrades visibly when bounds exceeded)
blocked_by:
  - task:t-067
  - task:t-070
cavekit_req: embeddings/R6
effort: M
id: "task:t-074"
mint_id: 8ddb14828ed74cd496eb7090c4fa9c62
origin: build-site
parents:
  - hyp:embeddings-r6
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-074: Scatter rendering plugin"
type: task
---

**Description:** Implement `ScatterRenderer` registering via T-067 plugin protocol. Maps (x, y) to a 200x200 char grid. Overlap shown as `#`. Out-of-bounds compressed with edge markers `<>^v`.

**Files:** `agi-tree/src/embeddings/scatter.py`, `agi-tree/tests/embeddings/test_scatter.py`

**Test Strategy:** Fixture grid with overlap; assert `#` at the expected cell. Assert bounds. Assert no re-projection (mock projection and confirm it's not called during render).
