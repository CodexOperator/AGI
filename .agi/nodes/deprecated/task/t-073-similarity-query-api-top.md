---
id: task:t-073
mint_id: 73b62fc514df453bb8385bf64cbad616
type: task
parents:
  - hyp:embeddings-r5
acceptance_criteria:
  - R5.1 (query accepts node id + k; returns up to k (id
  - score) pairs ordered by descending score)
  - R5.2 (no embedding for queried node → empty list + warning
  - does not raise)
  - R5.3 (scores in documented range)
blocked_by:
  - task:t-069
cavekit_req: embeddings/R5
edited_by: l1.09-execution-parent
effort: S
origin: build-site
status: deprecated
tags:
  - S
  - tier--1
thought_session: L1.09
tier: "-1"
title: "T-073: Similarity query API (top-k cosine)"
---
**Description:** Implement `similar_to(node_id, k) -> list[(id, score)]`. Score = cosine similarity in [-1.0, 1.0]. Missing embedding → `[]` + warning.

**Files:** `agi-tree/src/embeddings/similarity.py`, `agi-tree/tests/embeddings/test_similarity.py`

**Test Strategy:** Tests for each criterion, including the missing-embedding warning path.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `embeddings/R5` under `hyp:embeddings-r5`, whose disposition is disposition CLOSE-BY-CITATION -- closed by `verdict:embeddings-r5-by-citation` citing `build:src-embeddings-similarity`, `build:tests-embeddings-test-similarity`: `similarity.py` is top-k cosine similarity and `test_similarity.py` its suite.
<!-- THOUGHT:END -->
