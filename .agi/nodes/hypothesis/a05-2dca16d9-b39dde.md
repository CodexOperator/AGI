---
id: hypothesis:a05-2dca16d9-b39dde
mint_id: 95a24e6ac031474aaed83b8a9e115509
type: hypothesis
parents:
  - goal:g3
next_edges: []
confidence: 0.0
scaffold_hash: 7d42fe005d4a3824
title: A05 2dca16d9 b39dde
verdict: pending
---
# hypothesis:a05-2dca16d9-b39dde

## Hypothesis

**Claim:** `outcome_coverage` can be generalised to `goal_fulfilment_scoring(graph)`
that attributes each outcome node to the *specific goal node(s)* it fulfils (via
`parents:` traversal through mvp → build → idea/experiment chain), yielding a
per-goal metric in `[0.0, 1.0]` and a weighted aggregate that is strictly
harder to game than raw outcome_coverage.

### Structure

Walk each outcome node backward:
1. outcome → parent mvp (by `parents: [mvp:<id>]`)
2. mvp → parent hypothesis/experiment (by `parents: [hyp:<id>]` or `[exp:<id>]`)
3. continue up the parent chain until a `type: goal` node is reached

Count: for each goal G, `fulfilled_outcomes(G) / reachable_outcomes_from(G)`,
where `reachable_outcomes_from(G)` is the count of outcome nodes in G's subtree.

### Prove

- A working `goal_fulfilment_score(graph, goal_id)` returns correct score for
  3 test graphs: (a) one outcome traceable to G → 1.0, (b) 2/4 outcomes
  traceable → 0.5, (c) no outcomes traceable → 0.0.
- The aggregate `mean_goal_fulfilment(graph)` over all active goals is
  traceable: a human can verify each term by walking the node parents.
- The metric is monotonic in *goal reach, not hop count.* Appending deep
  chains under an outcome node that already resolves to a goal does not change
  any goal's score.

### Disprove

- Backward walk hits a node whose parent chain loops (cycle) without reaching
  a goal → undefined state that cannot be resolved without a cycle detector.
- An outcome node's parent chain terminates at a non-goal node with no further
  parents (orphan) → the score undercounts because half the tree is unreachable.
- `mean_goal_fulfilment` correlates strongly (>0.95 Pearson) with raw
  `outcome_coverage` on the real graph — meaning the extra resolution is
  illusory.


## Agent Notes
Filled in scaffolded hypothesis node for G3 L4 — true goal-fulfilment attribution scoring via backward parent-chain traversal from outcome through mvp/hypothesis/experiment to goal. Defines prove/disprove criteria including cycle-detection requirement and correlation check against raw outcome_coverage.
