---
id: idea:domain-vector-embedding-isomorphism
mint_id: 3b8e843c721c41d2b3d5b7304bcf37c2
type: idea
next_edges:
  - hyp:vector-embedding-isomorphism-r1
  - hyp:a00-324837df-2546ce
domain: vector-embedding-isomorphism
edited_by: season.py
season: 1
tags:
  - embeddings
  - renderers
  - isomorphism
  - node2vec
  - umap
  - duality
thought_session: season
title: "Vector Embedding Isomorphism: Graph↔Render Duality"
---
# Domain: Vector Embedding Isomorphism

## Concept
Bridge idea:domain-embeddings (Node2Vec + UMAP) with idea:domain-renderers (ASCII token positions) via **shared underlying representation**.

The claim: Node2Vec embeddings projected to 2D (UMAP) produce coordinates that are **isomorphic** to render token (x, y) positions. Same node should occupy similar coordinates in both spaces.

## Motivation
- AGENTS.md Capillary DAG: "Graph↔vector duality via Node2Vec+UMAP — shared representation between surface and embedding layer"
- Enables semantic zoom: visualize graph via embedding space, render via token space
- Enables cross-domain queries: "render nodes closest to node X in embedding space"

## Child Hypotheses

1. **hyp:vector-embedding-isomorphism-r1**: Node2Vec 2D projection places semantically-similar nodes at nearby (x,y) coordinates matching ASCII render positions
2. **R2**: Embedding-based similarity search returns same neighbors as graph traversal
3. **R3**: UMAP projection preserves local neighborhood structure