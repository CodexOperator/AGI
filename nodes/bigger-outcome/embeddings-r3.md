---
id: "bigger-outcome:embeddings-r3"
mint_id: 3d0773adfa4d422fbf6325a66984c5e0
next_edges:
  - app-purpose:embeddings
parents:
  - outcome:embeddings-r3
subgraph: false
tags:
  - embeddings
  - R3
testable_claim: Coordinate Isomorphism with Renderers
title: "embeddings/R3: Bigger Outcome"
type: bigger_outcome
---

**Bridges two previously separate layers into one isomorphic pipeline:**

1. **Embeddings layer** (`src/embeddings/`): `embed_graph()` → `project()` → produces `{node_id: (x, y)}` coordinates
2. **Renderers layer** (`src/renderers/`): `build_representation()` → produces `Representation` with x=0.0, y=0.0 tokens
3. **Integration (new):** `apply_umap_coords(repr, coords)` — bridges the two

**Why this matters:** The renderers (ASCII, Mermaid, git-tree, git-diff) now share a single source of truth for spatial layout. The UMAP projection that drives scatter-plot visualization IS the same projection used for ASCII depth layout. Visualization and similarity are now isomorphic by construction.

**Module purpose:** The embeddings module provides Node2Vec vectors and UMAP projections; the renderers module consumes those projections via a single function call; no duplicate coordinate computation.
