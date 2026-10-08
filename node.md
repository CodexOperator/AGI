---
id: hyp:embeddings-r7
mint_id: b3bd5c7126914e5d9e49c0b1a491b844
type: hypothesis
parents:
  - idea:domain-embeddings
confidence: 0.5
edited_by: season.py
origin: build-site
season: 1
status: deprecated
subgraph: false
tags:
  - embeddings
  - R7
testable_claim: Optional In-Graph Embedding Storage
thought_session: season
title: "embeddings/R7: Optional In-Graph Embedding Storage"
---
**Description:** Per-node vectors may optionally be stored as a payload field on the node itself so the embedding is persisted alongside the graph.

**Acceptance Criteria:**
- [ ] When in-graph storage is enabled, each node carries a `embedding_vector` payload field after embedding
- [ ] When in-graph storage is disabled (default), node files do not carry the field and embeddings live only in the cache
- [ ] Toggling the option does not invalidate previously stored vectors
- [ ] When the option is enabled and a node lacks the field, the embedding step backfills it without rewriting unrelated fields

## Out of Scope

- Alternative embedding models such as transformer-based encoders (documented as a future upgrade path but not required in v1)
- Specific workflows that consume similarity scores (for example "always extend the chain whose tail is most similar to X") — see autoresearch-tree-skill
- Visualization of three-dimensional projections beyond toggling the projection target — out of scope for renderers in v1
- Cross-graph or cross-repo embeddings — saved for later

## Cross-References

- See also: cavekit-graph-core.md (R1 nodes, R7 caching, R9 portability)
- See also: cavekit-renderers.md (R1 shared representation, R7 plugin contract)
- See also: cavekit-autoresearch-tree-skill.md (may consume similarity for agent dispatch)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); disposition GENUINELY-OPEN, not run: no `in_graph_storage.py` or equivalent; scoped by `goal:s32`.
<!-- THOUGHT:END -->