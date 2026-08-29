---
confidence: 0.5
id: "hyp:embeddings-r2"
mint_id: 595e78e465d5419d8af29a908703579f
next_edges:
  - exp:embeddings-r2
origin: build-site
parents:
  - idea:domain-embeddings
subgraph: false
tags:
  - embeddings
  - R2
testable_claim: UMAP Projection to 2D
title: "embeddings/R2: UMAP Projection to 2D"
type: hypothesis
---

**Description:** Per-node vectors are projected to two dimensions using UMAP. Three-dimensional projection is supported via configuration but is not required by default.

**Acceptance Criteria:**
- [ ] After projection, every embedded node has an `(x, y)` coordinate pair
- [ ] Projection dimensionality is configurable to either 2 or 3, with 2 as the default
- [ ] Two projection runs over the same vectors and configuration produce identical coordinates when the random seed is fixed
- [ ] When fewer than two nodes are embedded, projection completes with a documented degenerate result rather than raising
