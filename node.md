---
id: hyp:embeddings-r3
mint_id: e356a8ee1cc4429e94cb9bff07268cb6
type: hypothesis
parents:
  - idea:domain-embeddings
next_edges:
  - exp:embeddings-r3
confidence: 0.5
edited_by: season.py
origin: build-site
season: 1
status: deprecated
subgraph: false
tags:
  - embeddings
  - R3
testable_claim: Coordinate Isomorphism with Renderers
thought_session: season
title: "embeddings/R3: Coordinate Isomorphism with Renderers"
---
**Description:** The `(x, y)` coordinates produced by projection are exactly the `x` and `y` values used by the renderers' shared representation. There is one source of truth.

**Acceptance Criteria:**
- [ ] The renderer's shared representation derives `x` and `y` for each token from the embedding output for the same node id
- [ ] When embeddings are recomputed, the renderer's coordinates change accordingly without separate update steps
- [ ] No alternative coordinate source is permitted for nodes that have an embedding
- [ ] An integration check confirms that for every node, the renderer-side and embedding-side coordinates are equal

**Dependencies:** renderers (R1)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); already closed by `verdict:embeddings-r3` before this pass; deprecated with its domain (`idea:domain-embeddings`).
<!-- THOUGHT:END -->