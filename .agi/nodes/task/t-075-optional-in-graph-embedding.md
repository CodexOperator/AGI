---
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
effort: M
id: "task:t-075"
mint_id: e4f9468a253f44859aa92eddc4237674
origin: build-site
parents:
  - hyp:embeddings-r7
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-075: Optional in-graph embedding storage"
type: task
---

**Description:** Config flag `in_graph_storage: bool = false`. When true, after embed, write `embedding_vector` into each node's frontmatter via T-006 reader/writer. Toggle does not delete cache. Backfill is field-targeted (does not touch unrelated frontmatter keys).

**Files:** `agi-tree/src/embeddings/in_graph_storage.py`, `agi-tree/tests/embeddings/test_in_graph_storage.py`

**Test Strategy:** Default off → no field. Enable → field appears, other fields untouched. Toggle off → cache still valid. Toggle on with prior writes → no overwrite of unchanged values.
