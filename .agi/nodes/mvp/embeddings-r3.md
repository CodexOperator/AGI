---
id: mvp:embeddings-r3
mint_id: ea2eaba7355a4b1e8fa907c336f89086
type: mvp
parents:
  - verdict:embeddings-r3
next_edges:
  - outcome:embeddings-r3
edited_by: season.py
season: 1
subgraph: false
tags:
  - embeddings
  - R3
testable_claim: Coordinate Isomorphism with Renderers
thought_session: season
title: "embeddings/R3: MVP"
---
**MVP:** UMAP Coords → Representation Bridge

```python
from embeddings import (
    embed_graph, project,
    EmbeddingConfig, ProjectionConfig,
    apply_umap_coords,
)
from graph_core.loader import load_directory
from renderers import build_representation

# Step 1: Load graph
g, _ = load_directory("nodes", reconstruct_next_edges=True)

# Step 2: Embed graph nodes
vectors = embed_graph(g, EmbeddingConfig(dim=64, seed=42))

# Step 3: Project to 2D UMAP coordinates
coords = project(vectors, ProjectionConfig(dim=2, seed=42))

# Step 4: Build representation (tokens have x=0.0, y=0.0 by default)
repr_ = build_representation(g)

# Step 5: Apply UMAP coords — OVERWRITES token.x, token.y in-place
apply_umap_coords(repr_, coords)

# Now repr_.tokens have spatial x,y from UMAP, not just default zeros.
# The ASCII renderer and other renderers can use these coords for layout.
for t in repr_.tokens:
    print(f"{t.id}: x={t.x:.3f}, y={t.y:.3f}")
```

**Key files:**
- `src/embeddings/projection.py` — `apply_umap_coords()` function (new)
- `src/embeddings/__init__.py` — exports `apply_umap_coords`
- `src/renderers/representation.py` — R1 docstring updated to reference `apply_umap_coords`

**Isomorphic contract:** token.x, token.y == coords[node_id][0], coords[node_id][1]