---
confidence: 0.5
id: "hyp:renderers-r1"
mint_id: d718afc84b094938a450834e095cf941
next_edges:
  - exp:renderers-r1
origin: build-site
parents:
  - idea:domain-renderers
subgraph: false
tags:
  - renderers
  - R1
testable_claim: Shared Internal Representation
title: "renderers/R1: Shared Internal Representation"
type: hypothesis
---

**Description:** All renderers operate over a uniform representation: a sequence of render tokens, where each token carries identity, label, type, depth, two-dimensional coordinates, and outgoing edges.

**Acceptance Criteria:**
- [ ] A render token exposes the fields `id`, `label`, `type`, `depth`, `x`, `y`, and `edges`
- [ ] Building the representation from a graph is deterministic: identical input graphs produce identical token sequences
- [ ] The same representation is accepted by every renderer in this kit without conversion shims
- [ ] The representation is documented as a contract so external consumers (notably embeddings) can rely on it

**Dependencies:** graph-core (R1, R2)
