---
id: idea:domain-embeddings
mint_id: aad5f8aac1df43f8858a453d2c321662
type: idea
next_edges:
  - hyp:embeddings-r2
  - hyp:embeddings-r3
confidence: 1.0
edited_by: l1.09-execution-parent
origin: build-site
scale: big
status: deprecated
tags:
  - domain
  - seed
thought_session: L1.09
title: "Domain: embeddings"
---
Vector embeddings of the graph that share their two-dimensional projection with the renderers' shared representation. The same coordinate values that drive a scatter rendering also drive similarity queries: visualization and embedding are isomorphic by construction. Node2Vec is the embedding model and UMAP is the projection method for v1. Other models and projections are documented as upgrade paths but not required.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §B/§D/§E): the domain is partially built at `extensions/agi/src/embeddings/` (`idea:engine-embeddings` is the live counterpart); the three unbuilt pieces (R4 cache, R6 scatter renderer, R7 in-graph storage) are scoped by `goal:s32`, the one new goal this pass mints (§B).
<!-- THOUGHT:END -->
