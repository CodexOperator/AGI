---
confidence: 0.5
id: "hyp:embeddings-r3"
mint_id: e356a8ee1cc4429e94cb9bff07268cb6
next_edges:
  - exp:embeddings-r3
origin: build-site
parents:
  - idea:domain-embeddings
subgraph: false
tags:
  - embeddings
  - R3
testable_claim: Coordinate Isomorphism with Renderers
title: "embeddings/R3: Coordinate Isomorphism with Renderers"
type: hypothesis
---

**Description:** The `(x, y)` coordinates produced by projection are exactly the `x` and `y` values used by the renderers' shared representation. There is one source of truth.

**Acceptance Criteria:**
- [ ] The renderer's shared representation derives `x` and `y` for each token from the embedding output for the same node id
- [ ] When embeddings are recomputed, the renderer's coordinates change accordingly without separate update steps
- [ ] No alternative coordinate source is permitted for nodes that have an embedding
- [ ] An integration check confirms that for every node, the renderer-side and embedding-side coordinates are equal

**Dependencies:** renderers (R1)
