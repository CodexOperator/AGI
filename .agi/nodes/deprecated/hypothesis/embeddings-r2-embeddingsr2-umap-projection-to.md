---
id: hyp:embeddings-r2
mint_id: 595e78e465d5419d8af29a908703579f
type: hypothesis
parents:
  - idea:domain-embeddings
next_edges:
  - exp:embeddings-r2
confidence: 0.5
edited_by: l1.09-execution-parent
origin: build-site
status: deprecated
subgraph: false
tags:
  - embeddings
  - R2
testable_claim: UMAP Projection to 2D
thought_session: L1.09
title: "embeddings/R2: UMAP Projection to 2D"
---
**Description:** Per-node vectors are projected to two dimensions using UMAP. Three-dimensional projection is supported via configuration but is not required by default.

**Acceptance Criteria:**
- [ ] After projection, every embedded node has an `(x, y)` coordinate pair
- [ ] Projection dimensionality is configurable to either 2 or 3, with 2 as the default
- [ ] Two projection runs over the same vectors and configuration produce identical coordinates when the random seed is fixed
- [ ] When fewer than two nodes are embedded, projection completes with a documented degenerate result rather than raising

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); already closed by `verdict:embeddings-r2` before this pass; deprecated with its domain (`idea:domain-embeddings`).
<!-- THOUGHT:END -->
