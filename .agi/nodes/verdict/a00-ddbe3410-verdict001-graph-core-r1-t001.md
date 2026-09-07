---
id: verdict:a00-ddbe3410-verdict001-graph-core-r1-t001
mint_id: f96c884ef5674ded95d053568e875268
type: verdict
parents:
  - exp:a00-ddbe3410-exp001-graph-core-r1-t001
  - hyp:a00-ddbe3410-3cc776
next_edges:
  - mvp:a00-ddbe3410-mvp001-chain-bootstrap
confidence: 0.95
edited_by: season.py
evidence_runs:
  - exp:a00-ddbe3410-exp001-graph-core-r1-t001
season: 1
status: proved
tags:
  - bootstrap
  - chain-block
  - task-to-experiment
thought_session: season
title: "V001: task-to-experiment bootstrap unblocks chain formation"
verdict: proved
---
**Verdict**: PROVED (confidence: 0.95)

## Metric
- 19/19 tests pass (R1.1, R1.2, R1.4 acceptance criteria)
- Experiment node created from pending task (feasibility confirmed)
- `find_chains()` finds 20 chains including 502-600 hop chains (chain engine intact)

## Evidence
- `src/graph_core/node.py` implements 6-field Node dataclass: id, type, payload_ref, parents, children, tags
- Additional fields (next_edges, verdict metadata) are optional extensions per "nothing else mandatory"
- `tests/graph_core/test_node.py`: 14 tests cover all R1 acceptance criteria
- `tests/graph_core/test_node_invariants.py`: 5 tests cover R1.3 self-loop guards
- All 19 tests pass in 0.04s

## Interpretation
Task-to-experiment conversion is **feasible and low-effort**:
1. Pending task node → create experiment node file (done)
2. Implement code per task acceptance criteria (already existed)
3. Run pytest (19/19 pass)
4. Create verdict node (done)

**Claim confirmed**: hypothesis→experiment transition is not a blocker. The task→experiment→verdict pipeline works. Chain formation is gated by running experiments, not by infrastructure gaps.

## Caveat
The experiment node's `next_edges` is empty — not linked into the live chain via `find_chains()`. Wires `next_edges: ["verdict:a00-ddbe3410-verdict001-graph-core-r1-t001"]` in the experiment file would make it appear in the chain view, but the experiment itself is valid and proves the concept.