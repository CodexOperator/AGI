---
id: hyp:graph-core-r7
mint_id: 4555f3d46d3f44cd97a91db9cf8af425
type: hypothesis
parents:
  - idea:domain-graph-core
confidence: 0.5
edited_by: l1.09-execution-parent
origin: build-site
status: deprecated
subgraph: false
tags:
  - graph-core
  - R7
testable_claim: Warm-Load Caching
thought_session: L1.09
title: "graph-core/R7: Warm-Load Caching"
---
**Description:** Repeated loads of an unchanged graph return in constant time relative to first load. A memoization layer wraps the builder.

**Acceptance Criteria:**
- [ ] A second load of an unchanged source directory returns in time indistinguishable from a no-op (within the host's measurement noise floor)
- [ ] Modifying any node file invalidates the cache for at least that file's containing graph and triggers a rebuild on next load
- [ ] The cache key includes a content-addressed digest of the source set so renaming a file is detected
- [ ] Cache state lives inside the project's local context directory and never under absolute external paths

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); disposition CLOSE-BY-CITATION -- closed by `verdict:graph-core-r7-by-citation` citing `build:src-graph-core-cache`, `build:tests-graph-core-test-warm-load`: `cache.py` is the digest-keyed warm-load cache with invalidation and `test_warm_load.py` is its suite.
<!-- THOUGHT:END -->
