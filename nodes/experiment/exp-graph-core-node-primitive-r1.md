---
id: "exp:graph-core-node-primitive-r1"
next_edges:
  - "verdict:graph-core-r1"
parents:
  - hyp:graph-core-r1
subgraph: false
tags:
  - graph-core
  - R1
testable_claim: Generic Node Primitive
title: "graph-core/R1: Experiment"
type: experiment
---

**Description:** Run graph-core test suite + validate R1 acceptance criteria.

**Method:**
- Run pytest on tests/graph_core/ (16 test files)
- Validate R1.1–R1.6 programmatically
- Create 8-hop chain nodes

> Disambiguated 2026-08-25 from an id collision on `exp:graph-core-r1` (G7.2); the other file at `nodes/experiment/exp-graph-core-r1.md` retains that id.
