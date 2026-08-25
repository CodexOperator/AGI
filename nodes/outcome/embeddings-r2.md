---
id: "outcome:embeddings-r2"
mint_id: a89d76ed6863454aa9a9bcf2ec3b4e32
next_edges:
  - bigger-outcome:embeddings-r2
parents:
  - mvp:embeddings-r2
subgraph: false
tags:
  - embeddings
  - R2
title: "embeddings/R2: Outcome"
type: outcome
---

**Input:** Node embeddings (float vectors), config dict, random seed

**Output:** 2D (x, y) coordinate pairs per node via UMAP projection

**Behavior:**
- embed_graph() → per-node vectors (Node2Vec / random walk)
- project_to_2d() → UMAP or fallback to hash-based deterministic projection
- Coordinates are deterministic given same seed + config
- Degenerate case (< 2 nodes): zero coordinates + UserWarning

**Edge cases:**
- numpy unavailable → hash-based projection (still deterministic)
- dim=3 → 3D coordinates
- empty graph → no-op, no exception
