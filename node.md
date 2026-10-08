---
id: hyp:graph-core-r2
mint_id: 53c8000206f24232ae89ed74b0e927dd
type: hypothesis
parents:
  - idea:domain-graph-core
confidence: 0.5
edited_by: season.py
origin: build-site
season: 1
status: deprecated
subgraph: false
tags:
  - graph-core
  - R2
testable_claim: Generic Edge Primitive
thought_session: season
title: "graph-core/R2: Generic Edge Primitive"
---
**Description:** Edges connect a parent node to a child node, carry a relation type, and may carry tag metadata. The graph is a DAG; cycles are rejected at insert time.

**Acceptance Criteria:**
- [ ] Inserting an edge that would create a cycle returns a structured error and leaves the graph unchanged
- [ ] An edge exposes `source_id`, `target_id`, `relation`, and an optional `tags` set
- [ ] Two edges with the same `(source_id, target_id, relation)` are treated as one (idempotent insert)
- [ ] Removing a node removes all incident edges and leaves no dangling references

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); disposition CLOSE-BY-CITATION -- closed by `verdict:graph-core-r2-by-citation` citing `build:src-graph-core-edge`, `build:src-graph-core-graph`, `build:tests-graph-core-test-graph-dag`, `build:tests-graph-core-test-edge`, `build:tests-graph-core-test-node-invariants`: `edge.py`/`graph.py` carry `add_edge`/`remove_edge` and `_cycle_path`; the DAG, edge and node-invariant suites exercise cycle rejection, idempotent insert and no dangling references -- the same evidence pattern `verdict:graph-core-r1` was closed on (16 real test files).
<!-- THOUGHT:END -->