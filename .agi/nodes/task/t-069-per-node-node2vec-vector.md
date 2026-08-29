---
acceptance_criteria:
  - R1.1 (every node has exactly one associated vector after embed)
  - R1.2 (vector dimensionality configurable; documented default)
  - R1.3 (two runs over same graph + config + seed → identical vectors)
  - R1.4 (zero-node graph → completes successfully
  - empty vector set)
blocked_by:
  - task:t-001
  - task:t-003
cavekit_req: embeddings/R1
effort: M
id: "task:t-069"
mint_id: b93de7dd278345b4b388b08160de29bb
origin: build-site
parents:
  - hyp:embeddings-r1
status: pending
tags:
  - M
  - tier--1
tier: -1
title: "T-069: Per-node Node2Vec vector generation"
type: task
---

**Description:** Implement `embed_graph(graph, config) -> dict[node_id, vector]` using `gensim`-style Node2Vec or a stdlib reimplementation. Default dim=64; configurable via `context/config/embeddings.toml`. Random walks seeded.

**Files:** `agi-tree/src/embeddings/node2vec.py`, `agi-tree/src/graph_core/templates/embeddings.toml`, `agi-tree/tests/embeddings/test_node2vec.py`

**Test Strategy:** Fixture graphs of size 0, 1, and 10. Assert vector counts match node counts. Two runs with seed=42 produce identical vectors.
