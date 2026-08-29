---
confidence: 0.5
id: "hyp:environment-indexers-r8"
mint_id: 1861636abe0e4b6891a81d1d43d2f6b1
origin: build-site
parents:
  - idea:domain-environment-indexers
subgraph: false
tags:
  - environment-indexers
  - R8
testable_claim: Per-Path Result Caching
title: "environment-indexers/R8: Per-Path Result Caching"
type: hypothesis
---

**Description:** Indexer results are cached per-path so repeated invocations on the same unchanged source skip recomputation.

**Acceptance Criteria:**
- [ ] A second invocation on the same unchanged path returns in time indistinguishable from a no-op
- [ ] Modifying any source file under the target path invalidates the cache for at least that path's run
- [ ] Cache state is stored under the project context directory and is portable along with it
- [ ] Forcing a fresh re-run is available via a documented flag

**Dependencies:** graph-core (R7 warm-load caching, R9 portability)
