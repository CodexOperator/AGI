---
confidence: 0.5
id: "hyp:graph-core-r7"
mint_id: 4555f3d46d3f44cd97a91db9cf8af425
origin: build-site
parents:
  - idea:domain-graph-core
subgraph: false
tags:
  - graph-core
  - R7
testable_claim: Warm-Load Caching
title: "graph-core/R7: Warm-Load Caching"
type: hypothesis
---

**Description:** Repeated loads of an unchanged graph return in constant time relative to first load. A memoization layer wraps the builder.

**Acceptance Criteria:**
- [ ] A second load of an unchanged source directory returns in time indistinguishable from a no-op (within the host's measurement noise floor)
- [ ] Modifying any node file invalidates the cache for at least that file's containing graph and triggers a rebuild on next load
- [ ] The cache key includes a content-addressed digest of the source set so renaming a file is detected
- [ ] Cache state lives inside the project's local context directory and never under absolute external paths
