---
id: hyp:a00-ddbe3410-3cc776
mint_id: f202f3472d954d3f9c7ee2931f19e5df
type: hypothesis
parents:
  - idea:domain-chain-bootstrap
next_edges:
  - exp:a00-ddbe3410-exp001-graph-core-r1-t001
acceptance_criteria: []
blocked_by: []
cavekit_req: bootstrap/chain-block
edited_by: season.py
effort: L
season: 1
status: open
tags:
  - bootstrap
  - chain-block
  - iteration-1
thought_session: season
title: "Hypothesis: task-to-experiment bootstrap is the chain-block bottleneck"
---
## Hypothesis

The capillary DAG has 60 hypotheses, 90 pending tasks, but **zero experiment nodes and zero verdict nodes**. This is not a content gap — it is an **execution gap**. The graph is blocked at the hypothesis→experiment transition.

**Claim:** Converting pending task nodes into experiment nodes (with actual code implementations + test runs) is both necessary and sufficient to unblock chain formation and enable verdict nodes to appear.

## What would prove it?

1. Create ≥1 experiment node from a pending task (e.g., t-001 from graph-core-r1).
2. Implement the task's described code in `src/` and tests in `tests/`.
3. Run `pytest` — experiment succeeds (test passes).
4. Create the corresponding verdict node.
5. Verify `find_chains()` reports ≥1 chain of length >2 (hypothesis→experiment→verdict).

## What would disprove it?

- Cannot create experiment node because task definition is incomplete/ambiguous (acceptance_criteria missing critical detail).
- Code implementation fails all test paths (acceptance_criteria not achievable).
- After experiment runs, `find_chains()` still reports 0 chains (chain engine itself is broken).

## Rationale

The context snapshot shows `longest_chain: 0 hops` and `chain_count: 0`. This is not a render issue — it reflects that no experiment→verdict edges exist. The 60 hypothesis nodes are well-formed; the 90 task nodes are fully specified. The missing layer is **execution infrastructure**: experiment runners, test execution, and verdict node creation. Bootstrap this layer first; all other chains follow.

## Experiment Plan

Pick `task:t-001` (graph-core-r1, "Generic node primitive structure") as the first bootstrap experiment:
- **Hypothesis:** `hyp:graph-core-r1`
- **Task:** t-001 (6-field Node dataclass)
- **File to create:** `nodes/experiment/a00-ddbe3410-exp001-graph-core-r1-t001.md`
- **Code:** `src/graph_core/node.py` + `tests/graph_core/test_node.py`
- **Run:** `python3 -m pytest tests/ -q`
- **Verdict:** `nodes/verdict/a00-ddbe3410-verdict001-graph-core-r1-t001.md`