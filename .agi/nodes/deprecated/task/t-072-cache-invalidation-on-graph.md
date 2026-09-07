---
id: task:t-072
mint_id: ca127bc09e784696adbbf3d143309ac4
type: task
parents:
  - hyp:embeddings-r4
acceptance_criteria:
  - R4.1 (add/remove/modify node invalidates that node's vector → recomputed next embed)
  - R4.2 (no graph or config change → two runs produce same vectors and coords)
  - R4.3 (cached embedding state under context dir
  - portable)
  - R4.4 (force full re-embed via documented flag)
blocked_by:
  - task:t-069
  - task:t-013
cavekit_req: embeddings/R4
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
title: "T-072: Cache invalidation on graph change"
---
**Description:** Embedding cache stored at `context/.cache/embeddings/<digest>.npz`. Per-node digest tracked; only invalid entries re-embedded. `--reembed` flag forces full rebuild.

**Files:** `agi-tree/src/embeddings/cache.py`, `agi-tree/tests/embeddings/test_embedding_cache.py`

**Test Strategy:** Mutate one node, embed, assert one vector recomputed. Two unchanged runs produce identical vectors. Force flag rebuilds all.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `embeddings/R4` under `hyp:embeddings-r4`, whose disposition is disposition GENUINELY-OPEN, not run: no dedicated cache module under `src/embeddings/`; scoped by `goal:s32` (reuse `graph_core/cache.py`'s digest-and-invalidate pattern).
<!-- THOUGHT:END -->