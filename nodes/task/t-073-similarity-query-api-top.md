---
acceptance_criteria:
  - R5.1 (query accepts node id + k; returns up to k (id
  - score) pairs ordered by descending score)
  - R5.2 (no embedding for queried node → empty list + warning
  - does not raise)
  - R5.3 (scores in documented range)
blocked_by:
  - task:t-069
cavekit_req: embeddings/R5
effort: S
id: "task:t-073"
mint_id: 73b62fc514df453bb8385bf64cbad616
origin: build-site
parents:
  - hyp:embeddings-r5
status: pending
tags:
  - S
  - tier--1
tier: -1
title: "T-073: Similarity query API (top-k cosine)"
type: task
---

**Description:** Implement `similar_to(node_id, k) -> list[(id, score)]`. Score = cosine similarity in [-1.0, 1.0]. Missing embedding → `[]` + warning.

**Files:** `agi-tree/src/embeddings/similarity.py`, `agi-tree/tests/embeddings/test_similarity.py`

**Test Strategy:** Tests for each criterion, including the missing-embedding warning path.
