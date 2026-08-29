---
confidence: 0.95
id: "mvp:a00-324837df-2546ce"
mint_id: 9766d3c1c2c44ecab1f46c5b4639c97e
next_edges:
  - outcome:a00-324837df-2546ce
parents:
  - verdict:a00-324837df-2546ce
status: open
tags:
  - embeddings
  - node2vec
  - gensim
  - MVP
title: "MVP: Gensim Skip-Gram Node2Vec Wrapper"
type: mvp
---

**Script**: `exp-a00-324837df-vector-embedding-isomorphism-r2.py`

**What it does**: Wraps gensim Word2Vec to replace the hash-based node2vec in `src/embeddings/node2vec.py`.

**Key changes**:
1. Install gensim dependency: `uv pip install gensim -p <venv>`
2. Replace `_walks_to_vector()` hash projection with gensim Word2Vec(sg=1)
3. Keep same random walk generation for deterministic walks
4. Preserve the `embed_graph()` function signature

**API** (same as existing):
```python
from embeddings import embed_graph, EmbeddingConfig
vectors = embed_graph(g)  # dict[node_id -> list[float]]
```

**Performance**: Gensim Word2Vec trains in ~seconds on 2968-node graph with 40-length walks.
**Result**: Spearman from -0.18 → +0.37 (complete reversal)
