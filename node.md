---
id: hyp:graph-core-r1
mint_id: 4959ba1d6e9f409ebd87fa3ee7dddb54
type: hypothesis
parents:
  - idea:domain-graph-core
next_edges:
  - exp:graph-core-r1
confidence: 0.5
edited_by: season.py
origin: build-site
season: 1
status: deprecated
subgraph: false
tags:
  - graph-core
  - R1
testable_claim: Generic Node Primitive
thought_session: season
title: "graph-core/R1: Generic Node Primitive"
---
**Description:** A node is a typed, identified record with an optional payload reference, parent and child links, and free-form tags. Node type does not constrain payload; payload meaning is delegated to the schema-registry.

**Acceptance Criteria:**
- [ ] A node exposes the fields `id`, `type`, `payload_ref`, `parents`, `children`, `tags` and nothing in graph-core requires additional mandatory fields
- [ ] A node with no parents is accepted as a valid root and a node with no children is accepted as a valid leaf
- [ ] `parents` and `children` are sets of node ids (no duplicates) and self-loops are rejected with a clear error
- [ ] `tags` is a set of strings and is independent of the typed parent/child links

**Dependencies:** none

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); already closed by `verdict:graph-core-r1` before this pass; deprecated with its domain (`idea:domain-graph-core`).
<!-- THOUGHT:END -->