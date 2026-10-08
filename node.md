---
id: mvp:embeddings-r2
mint_id: 9fffa74147e04d6794845012390f544e
type: mvp
parents:
  - verdict:embeddings-r2
next_edges:
  - outcome:embeddings-r2
edited_by: season.py
season: 1
subgraph: false
tags:
  - embeddings
  - R2
testable_claim: UMAP Projection to 2D
thought_session: season
title: "embeddings/R2: MVP"
---
**MVP:** UMAP 2D/3D Projection from Embedding Vectors

```python
from embeddings import embed_graph, project, EmbeddingConfig, ProjectionConfig
from graph_core.graph import Graph

# Step 1: embed the graph
g = Graph()  # load from disk
vectors = embed_graph(g, EmbeddingConfig(dim=64, seed=42))

# Step 2: project to 2D
coords = project(vectors, ProjectionConfig(dim=2, seed=42))
# coords: {node_id: (x, y)} — x,y in [-1, 1]

# Step 3: project to 3D (optional)
coords3d = project(vectors, ProjectionConfig(dim=3, seed=42))
# coords3d: {node_id: (x, y, z)}
```

**Key files:**
- `src/embeddings/projection.py` — ProjectionConfig + project() function
- `src/embeddings/node2vec.py` — embed_graph() producing vectors
- `src/embeddings/similarity.py` — cosine + similar_to() for similarity queries

**Isomorphic contract:** The (x, y) produced here equals the x, y used by renderers' shared representation.