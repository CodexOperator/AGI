---
id: hypothesis:a02-db21629c-547d80
mint_id: a6ad86b0e87240e1af4522f863d60e96
type: hypothesis
parents:
  - goal:g3
next_edges: []
confidence: 1.0
scaffold_hash: 7573f8a5a69cbb1a
testable_claim: "Implement `goal_outcome_density(goal_id)`: scan all outcome-type nodes, filter to those reachable from `goal_id` via a path that includes ≥1 experiment node. The value is `(|{outcomes matching filter}| / |{all outcomes}|)`. This metric is strictly monotonic in real goal progress and flat under irrelevant motion."
title: A02 db21629c 547d80
verdict: pending
---
# hypothesis:a02-db21629c-547d80

## Hypothesis

**Goal-attributed outcome density** — a metric measuring the fraction of outcome nodes in the graph that are reachable from a specific goal node through an edge path containing at least one experiment node — is a reliable, non-gameable measure of genuine goal progress. Unlike `outcome_coverage` (which counts any chain reaching any outcome, L4's open complaint), this metric cannot be inflated by adding irrelevant hops.

### Testable claim

Implement `goal_outcome_density(goal_id)`: scan all outcome-type nodes, filter to those reachable from `goal_id` via a path that includes ≥1 experiment node. The value is `(|{outcomes matching filter}| / |{all outcomes}|)`. This metric is strictly monotonic in real goal progress and flat under irrelevant motion.

### What would prove it (pass condition)

A synthetic graph experiment shows:
1. Adding 1000 hop-count nodes (no experiment, no evidence) between `goal:g3` and any outcome leaves `goal_outcome_density("goal:g3")` unchanged.
2. Adding one experiment-backed outcome linked to `goal:g3` increases the metric.
3. The metric correlates with `evidence_fraction` but is strictly lower or equal (because it requires goal-named reachability, not just any evidence).
4. `outcome_coverage` can rise while `goal_outcome_density` stays flat (demonstrating the gameability gap L4 names).

### What would disprove it (fail condition)

1. `goal_outcome_density` can be increased by hops that contain no experiment node (a path that reaches an outcome via only idea→build→build chains, bypassing experiment nodes, and still passes the filter).
2. The metric is identical to `outcome_coverage` on all real graph states (meaning it adds no new signal — the filter is redundant).
3. Implementation cost outweighs signal gain: the edge scan is O(n²) or worse on the full corpus and the metric is not computable in interactive time.


## Agent Notes
Goal-attributed outcome density hypothesis. Directly addresses L4: outcome_coverage proxies any-outcome, not goal-specific attribution. Metric requires >=1 experiment node in reachability path to prevent hop-count gaming. Pass conditions defined: synthetic graph test with 1000 irrelevant hops vs single experiment-backed outcome.