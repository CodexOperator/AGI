---
id: hyp:renderers-r6
mint_id: 4a98378739b54068bd1d05e3023a7495
type: hypothesis
parents:
  - idea:domain-renderers
confidence: 0.5
edited_by: l1.09-execution-parent
origin: build-site
status: deprecated
subgraph: false
tags:
  - renderers
  - R6
testable_claim: Recursive Rendering
thought_session: L1.09
title: "renderers/R6: Recursive Rendering"
---
**Description:** When a node's body is itself a subgraph, renderers may render it as a nested view bounded in depth.

**Acceptance Criteria:**
- [ ] A node flagged as containing a subgraph is rendered with a visible nested view in renderers that support nesting
- [ ] The ASCII renderer renders nested subgraphs to a maximum depth of two levels
- [ ] Renderers that do not support nesting render only a single placeholder line per nested subgraph
- [ ] Nesting depth is configurable and respects a documented maximum

**Dependencies:** graph-core (R5 recursive node bodies)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); disposition GENUINELY-OPEN, not run: no nested-subgraph rendering with a depth bound in `ascii.py` or elsewhere; no existing goal obviously covers it, so this THOUGHT is the record.
<!-- THOUGHT:END -->
