---
id: hyp:renderers-r1
mint_id: d718afc84b094938a450834e095cf941
type: hypothesis
parents:
  - idea:domain-renderers
next_edges:
  - exp:renderers-r1
confidence: 0.5
edited_by: season.py
origin: build-site
season: 1
status: deprecated
subgraph: false
tags:
  - renderers
  - R1
testable_claim: Shared Internal Representation
thought_session: season
title: "renderers/R1: Shared Internal Representation"
---
**Description:** All renderers operate over a uniform representation: a sequence of render tokens, where each token carries identity, label, type, depth, two-dimensional coordinates, and outgoing edges.

**Acceptance Criteria:**
- [ ] A render token exposes the fields `id`, `label`, `type`, `depth`, `x`, `y`, and `edges`
- [ ] Building the representation from a graph is deterministic: identical input graphs produce identical token sequences
- [ ] The same representation is accepted by every renderer in this kit without conversion shims
- [ ] The representation is documented as a contract so external consumers (notably embeddings) can rely on it

**Dependencies:** graph-core (R1, R2)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); already closed by `verdict:renderers-r1` before this pass; deprecated with its domain (`idea:domain-renderers`).
<!-- THOUGHT:END -->