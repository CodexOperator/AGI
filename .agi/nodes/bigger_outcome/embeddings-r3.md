---
id: bigger_outcome:embeddings-r3
mint_id: 3d0773adfa4d422fbf6325a66984c5e0
type: bigger_outcome
parents:
  - outcome:embeddings-r3
next_edges:
  - vision:embeddings
edited_by: season.py
judged_against: goal:g11
season: 1
subgraph: false
tags:
  - embeddings
  - R3
testable_claim: Coordinate Isomorphism with Renderers
thought_session: season
title: "embeddings/R3: Bigger Outcome"
---
**Bridges two previously separate layers into one isomorphic pipeline:**

1. **Embeddings layer** (`src/embeddings/`): `embed_graph()` → `project()` → produces `{node_id: (x, y)}` coordinates
2. **Renderers layer** (`src/renderers/`): `build_representation()` → produces `Representation` with x=0.0, y=0.0 tokens
3. **Integration (new):** `apply_umap_coords(repr, coords)` — bridges the two

**Why this matters:** The renderers (ASCII, Mermaid, git-tree, git-diff) now share a single source of truth for spatial layout. The UMAP projection that drives scatter-plot visualization IS the same projection used for ASCII depth layout. Visualization and similarity are now isomorphic by construction.

**Module purpose:** The embeddings module provides Node2Vec vectors and UMAP projections; the renderers module consumes those projections via a single function call; no duplicate coordinate computation.