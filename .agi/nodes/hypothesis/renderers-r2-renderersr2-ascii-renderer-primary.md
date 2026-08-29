---
confidence: 0.5
id: "hyp:renderers-r2"
mint_id: a60a3d65d9654a8394e4ca0a915e86d3
origin: build-site
parents:
  - idea:domain-renderers
subgraph: false
tags:
  - renderers
  - R2
testable_claim: ASCII Renderer (Primary)
title: "renderers/R2: ASCII Renderer (Primary)"
type: hypothesis
---

**Description:** A primary renderer produces a compact text view bounded by 200 lines and 200 columns. The view is hierarchical and includes a summary of edges and a count of node types.

**Acceptance Criteria:**
- [ ] Rendering any graph produces output of at most 200 lines and at most 200 columns
- [ ] When the graph is too large for the bounds, the renderer compresses or truncates with a clearly visible marker rather than overflowing
- [ ] The output includes a per-type count and a summary of edges
- [ ] Two runs against the same graph produce byte-equal output
