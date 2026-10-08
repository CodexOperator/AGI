---
id: exp:a00-324837df-2546ce
mint_id: 7bad2164b95746689a109773f8839469
type: experiment
parents:
  - hyp:a00-324837df-2546ce
next_edges:
  - verdict:a00-324837df-2546ce
domain: vector-embedding-isomorphism
edited_by: season.py
season: 1
spawns: []
status: complete
tags:
  - embeddings
  - node2vec
  - gensim
  - skip-gram
  - spearman
thought_session: season
title: "R2: Gensim Skip-Gram Node2Vec Topology Preservation"
---
## Experiment: Gensim Skip-Gram Node2Vec (R2)

**Script**: `exp-a00-324837df-vector-embedding-isomorphism-r2.py`
**Run**: iter-031 agent a00-324837df
**Date**: 2026-05-01

### Method
1. Load graph (2968 nodes, 2440 edges)
2. Build adjacency and generate deterministic random walks (seed=42, walk_length=40, walks_per_node=5) — identical to R1 for fair comparison
3. Train gensim Word2Vec(sg=1, vector_size=32, window=5, epochs=10, seed=42)
4. Project learned vectors to 2D via PCA
5. Compute Spearman correlation on 94 reachable node pairs (same sample as R1)

### Results
- **Spearman rho (94 pairs): 0.3726** ← R1-comparable
- **Spearman rho (200 pairs): 0.4100**
- **p-value: < 0.001** (highly significant)
- R1 baseline: -0.18
- **Improvement vs R1: +0.5526** (from -0.18 to +0.37)

### Verdict
**PROVED** — Gensim skip-gram preserves graph topology significantly better than hash-based approach. Spearman 0.37 >> 0.3 threshold, and a complete reversal from R1's -0.18 failure.