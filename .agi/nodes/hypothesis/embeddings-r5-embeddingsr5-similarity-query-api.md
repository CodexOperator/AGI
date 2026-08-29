---
confidence: 0.5
id: "hyp:embeddings-r5"
mint_id: 3282cea869104c2d95fce50e5a1b4e64
origin: build-site
parents:
  - idea:domain-embeddings
subgraph: false
tags:
  - embeddings
  - R5
testable_claim: Similarity Query API
title: "embeddings/R5: Similarity Query API"
type: hypothesis
---

**Description:** A query returns the `k` most similar nodes to a given node id, ranked by similarity score.

**Acceptance Criteria:**
- [ ] The query accepts a node id and an integer `k` and returns up to `k` `(node_id, score)` pairs ordered by descending score
- [ ] When the requested node has no embedding, the query returns an empty list and emits a warning rather than raising
- [ ] Scores are real numbers in a documented range
- [ ] Two queries with the same arguments over the same embedding state produce identical results
