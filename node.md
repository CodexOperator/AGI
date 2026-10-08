---
id: hyp:a00-324837df-2546ce
mint_id: cbe5102fffee43f9a2947c26ff776f63
type: hypothesis
parents:
  - idea:domain-vector-embedding-isomorphism
next_edges:
  - exp:a00-324837df-2546ce
domain: vector-embedding-isomorphism
edited_by: season.py
season: 1
spawns: []
status: complete
tags:
  - embeddings
  - node2vec
  - gensim
  - isomorphism
  - skip-gram
thought_session: season
title: "R2: Gensim Skip-Gram Node2Vec Preserves Graph Topology"
---
## Hypothesis

**Claim**: A true gensim skip-gram Word2Vec implementation will preserve graph topology significantly better than the hash-based approach (R1 Spearman = -0.18).

**Why this matters**: R1 proved that the stdlib hash-based Node2Vec (which projects node IDs through SHA-256 bins) fails completely at topology preservation. A real neural skip-gram learns distributional node similarity from random walk sequences — fundamentally different from hash projection. If skip-gram works, the graph↔vector duality in the capillary DAG becomes real.

**Test**:
1. Generate same deterministic random walks as R1 (walk_length=40, walks_per_node=5, seed=42)
2. Train gensim Word2Vec(sg=1, vector_size=32, window=5, epochs=10)
3. Project learned vectors to 2D via PCA
4. Compute Spearman correlation on 94 reachable node pairs (same sample as R1)
5. Compare to R1 baseline of -0.18

**Would prove it**: Spearman > 0.3 on the same 94-pair benchmark (meaningful positive correlation, significantly above R1's -0.18)
**Would disprove it**: Spearman ≤ 0.3 (including negative — gensim also fails)

## Next Steps
- R3: If R2 passes, test whether embedding-based similarity search (k-nearest in vector space) returns the same neighbors as graph BFS traversal
- R4: Test whether UMAP (instead of PCA) for 2D projection improves preservation further