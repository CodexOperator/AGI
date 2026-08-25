---
confidence: 0.5
id: "hyp:renderers-r6"
mint_id: 4a98378739b54068bd1d05e3023a7495
origin: build-site
parents:
  - idea:domain-renderers
subgraph: false
tags:
  - renderers
  - R6
testable_claim: Recursive Rendering
title: "renderers/R6: Recursive Rendering"
type: hypothesis
---

**Description:** When a node's body is itself a subgraph, renderers may render it as a nested view bounded in depth.

**Acceptance Criteria:**
- [ ] A node flagged as containing a subgraph is rendered with a visible nested view in renderers that support nesting
- [ ] The ASCII renderer renders nested subgraphs to a maximum depth of two levels
- [ ] Renderers that do not support nesting render only a single placeholder line per nested subgraph
- [ ] Nesting depth is configurable and respects a documented maximum

**Dependencies:** graph-core (R5 recursive node bodies)
