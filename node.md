---
id: bigger_outcome:embeddings-r2
mint_id: bc59d23570a94cdb8fb99c7e659b806a
type: bigger_outcome
parents:
  - outcome:embeddings-r2
next_edges:
  - vision:embeddings
edited_by: season.py
judged_against: goal:g11
season: 1
subgraph: false
tags:
  - embeddings
  - R2
thought_session: season
title: "embeddings/R2: Bigger Outcome"
---
**Broader outcome:** Per-node embeddings enable similarity queries, scatter rendering, and the vector-ASCII isomorphism (R3). Node2Vec generates vectors; UMAP projects to 2D. The same coordinate system underlies both the embeddings module and the renderers module.

**Properties achieved:**
- Per-Node Vector Generation (R1): embed_graph() returns one vector per node
- UMAP Projection to 2D (R2): project_to_2d() gives (x, y) coords
- Coordinate Isomorphism with Renderers (R3): UMAP (x,y) = RenderToken(x,y)
- Cache Invalidation on Graph Mutation (R4): embeddings invalidated on node add/remove
- Similarity Query API (R5): top_k_similar() returns k most similar nodes
- Scatter Rendering Plugin (R6): scatter renderer as renderer plugin
- Optional in Graph Embedding (R7): embeddings module is pluggable