---
confidence: 0.5
id: "hyp:renderers-r4"
mint_id: 658337671af34e5fb20b53e5d4d2ff3e
origin: build-site
parents:
  - idea:domain-renderers
subgraph: false
tags:
  - renderers
  - R4
testable_claim: Git-Tree Renderer
title: "renderers/R4: Git-Tree Renderer"
type: hypothesis
---

**Description:** A renderer produces a view shaped like the output of a graph-style git log, where each chain corresponds to one branch shape.

**Acceptance Criteria:**
- [ ] Each chain in the input appears as one branch-shaped lane in the output
- [ ] Lane order is deterministic and rooted in the highest-scoring chain
- [ ] Merge points (where two chains share a node) render as a visible junction
- [ ] The output uses only printable ASCII characters
