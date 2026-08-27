---
confidence: 0.95
id: "vision:vector-embedding-isomorphism"
mint_id: 02b2716cc98e42bb93792dd5f34092ff
parents:
  - bigger_outcome:a00-324837df-2546ce
status: open
tags:
  - embeddings
  - renderers
  - duality
  - capillary-dag
title: "App-Purpose: Graph↔Vector Duality for Capillary DAG"
type: vision
---

**Purpose**: Enables semantic zoom and cross-domain queries on the capillary DAG.

The graph↔vector duality means the same node occupies similar coordinates in both the graph traversal space and the learned embedding space. This duality enables:

1. **Semantic zoom**: Visualize the entire research graph as a scatter plot; zoom in to see local neighborhood structure
2. **Embedding-based queries**: "Find the 5 hypotheses most similar to this one" via cosine similarity in vector space
3. **Cross-domain navigation**: See which ideas from different domains cluster together based on structural similarity
4. **Coherence scoring**: Measure how coherent a chain is by how tightly its nodes cluster in embedding space

**Status**: R1 DISPROVED (hash-based), R2 PROVED (gensim skip-gram, Spearman=0.37).
**Next**: R3 (embedding k-NN vs BFS neighbors), R4 (UMAP vs PCA for projection).
