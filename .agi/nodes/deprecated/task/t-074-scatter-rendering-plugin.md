---
id: task:t-074
mint_id: 8ddb14828ed74cd496eb7090c4fa9c62
type: task
parents:
  - hyp:embeddings-r6
acceptance_criteria:
  - R6.1 (registered through same renderer plugin contract used by renderers kit)
  - R6.2 (places each node at coordinates derived from UMAP (x
  - y)
  - no re-projecting)
  - {"R6.3 (output respects ASCII bounds": "\u2264200 lines/cols; degrades visibly when bounds exceeded)"}
blocked_by:
  - task:t-067
  - task:t-070
cavekit_req: embeddings/R6
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
title: "T-074: Scatter rendering plugin"
---
**Description:** Implement `ScatterRenderer` registering via T-067 plugin protocol. Maps (x, y) to a 200x200 char grid. Overlap shown as `#`. Out-of-bounds compressed with edge markers `<>^v`.

**Files:** `agi-tree/src/embeddings/scatter.py`, `agi-tree/tests/embeddings/test_scatter.py`

**Test Strategy:** Fixture grid with overlap; assert `#` at the expected cell. Assert bounds. Assert no re-projection (mock projection and confirm it's not called during render).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `embeddings/R6` under `hyp:embeddings-r6`, whose disposition is disposition GENUINELY-OPEN, not run: no `scatter.py`, and the renderer plugin contract it was blocked on (`hyp:renderers-r7`) does not exist; scoped by `goal:s32`.
<!-- THOUGHT:END -->