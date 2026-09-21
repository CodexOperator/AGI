---
id: task:t-075
mint_id: e4f9468a253f44859aa92eddc4237674
type: task
parents:
  - hyp:embeddings-r7
acceptance_criteria:
  - R7.1 (when enabled
  - each node carries embedding_vector payload field after embedding)
  - R7.2 (when disabled (default)
  - node files do not carry the field; embeddings live only in cache)
  - R7.3 (toggling option does not invalidate previously stored vectors)
blocked_by:
  - task:t-072
  - task:t-006
cavekit_req: embeddings/R7
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
title: "T-075: Optional in-graph embedding storage"
---
**Description:** Config flag `in_graph_storage: bool = false`. When true, after embed, write `embedding_vector` into each node's frontmatter via T-006 reader/writer. Toggle does not delete cache. Backfill is field-targeted (does not touch unrelated frontmatter keys).

**Files:** `agi-tree/src/embeddings/in_graph_storage.py`, `agi-tree/tests/embeddings/test_in_graph_storage.py`

**Test Strategy:** Default off → no field. Enable → field appears, other fields untouched. Toggle off → cache still valid. Toggle on with prior writes → no overwrite of unchanged values.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `embeddings/R7` under `hyp:embeddings-r7`, whose disposition is disposition GENUINELY-OPEN, not run: no `in_graph_storage.py` or equivalent; scoped by `goal:s32`.
<!-- THOUGHT:END -->