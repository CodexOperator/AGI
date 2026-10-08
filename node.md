---
id: hyp:embeddings-r4
mint_id: 93c6b5bf11a846bd8de85eccda012042
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
  - R4
testable_claim: Cache Invalidation on Graph Change
thought_session: season
title: "embeddings/R4: Cache Invalidation on Graph Change"
---
**Description:** Embedding state is invalidated when the underlying graph changes. UMAP coordinates remain stable across rebuilds when the graph is unchanged and the seed is fixed.

**Acceptance Criteria:**
- [ ] Adding, removing, or modifying a node invalidates that node's vector and triggers recomputation on next embed
- [ ] When neither the graph nor the configuration change, two consecutive runs produce the same vectors and the same coordinates
- [ ] Cached embedding state lives inside the project context directory and is portable along with it
- [ ] A documented flag forces a full re-embed regardless of cache state

**Dependencies:** graph-core (R7 warm-load caching, R9 portability)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); disposition GENUINELY-OPEN, not run: no dedicated cache module under `src/embeddings/`; scoped by `goal:s32` (reuse `graph_core/cache.py`'s digest-and-invalidate pattern).
<!-- THOUGHT:END -->