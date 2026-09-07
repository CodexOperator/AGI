---
id: hyp:embeddings-r5
mint_id: 3282cea869104c2d95fce50e5a1b4e64
type: hypothesis
parents:
  - idea:domain-embeddings
confidence: 0.5
edited_by: season.py
origin: build-site
season: 1
status: deprecated
subgraph: false
tags:
  - embeddings
  - R5
testable_claim: Similarity Query API
thought_session: season
title: "embeddings/R5: Similarity Query API"
---
**Description:** A query returns the `k` most similar nodes to a given node id, ranked by similarity score.

**Acceptance Criteria:**
- [ ] The query accepts a node id and an integer `k` and returns up to `k` `(node_id, score)` pairs ordered by descending score
- [ ] When the requested node has no embedding, the query returns an empty list and emits a warning rather than raising
- [ ] Scores are real numbers in a documented range
- [ ] Two queries with the same arguments over the same embedding state produce identical results

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); disposition CLOSE-BY-CITATION -- closed by `verdict:embeddings-r5-by-citation` citing `build:src-embeddings-similarity`, `build:tests-embeddings-test-similarity`: `similarity.py` is top-k cosine similarity and `test_similarity.py` its suite.
<!-- THOUGHT:END -->