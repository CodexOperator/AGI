---
id: outcome:a00-324837df-2546ce
mint_id: 5541a39537bc4518b06bdeb78b75a0f5
type: outcome
parents:
  - mvp:a00-324837df-2546ce
next_edges:
  - bigger_outcome:a00-324837df-2546ce
confidence: 0.95
edited_by: ubuntu
judged_against: goal:g13
lens: unknown
season: 1
status: open
tags:
  - embeddings
  - node2vec
  - isomorphism
thought_session: season
title: "Outcome: Gensim Skip-Gram Embeddings"
---
**Input**: Graph with 2968 nodes, 2440 edges (autoresearch-tree capillary DAG)
**Output**: dict[node_id → list[float, dim=32]] learned skip-gram embeddings

**Behavior**:
- Generates 40-step random walks (seed=42, 5 walks/node) over the graph
- Trains gensim Word2Vec(sg=1, vector_size=32, window=5, epochs=10)
- Returns one 32-dim vector per node

**Edge cases**:
- Empty graph → empty dict
- Isolated node → vector learned from walks that reach it
- Very large graph → gensim is O(n) for training, handles 3000+ nodes

**Topology preservation** (verified):
- Spearman rho = 0.37 on 94 reachable pairs (vs hash-based -0.18)
- Nodes closer in graph → closer in embedding space
- Statistically significant (p < 0.001)

**Next**: PCA/UMAP projection → scatter renderer for semantic zoom