---
confidence: 1.0
id: "idea:domain-embeddings"
mint_id: aad5f8aac1df43f8858a453d2c321662
next_edges:
  - hyp:embeddings-r2
  - hyp:embeddings-r3
origin: build-site
scale: big
status: open
tags:
  - domain
  - seed
title: "Domain: embeddings"
type: idea
---

Vector embeddings of the graph that share their two-dimensional projection with the renderers' shared representation. The same coordinate values that drive a scatter rendering also drive similarity queries: visualization and embedding are isomorphic by construction. Node2Vec is the embedding model and UMAP is the projection method for v1. Other models and projections are documented as upgrade paths but not required.
