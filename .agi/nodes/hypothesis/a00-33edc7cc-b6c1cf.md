---
id: hypothesis:a00-33edc7cc-b6c1cf
mint_id: 411fd7d3884644c3bb00ef88ab64fa85
type: hypothesis
parents:
  - goal:g3
next_edges: []
confidence: 0.0
scaffold_hash: aee6667a33947786
title: A00 33edc7cc b6c1cf
verdict: pending
---
# hypothesis:a00-33edc7cc-b6c1cf

## Hypothesis

**Claim:** The 596 unattributed nodes (`unattributed_nodes` from `goal_attribution()`, 61% of 974 active nodes in the agi corpus) include a disproportionate share of **hypotheses** — enough that the current `outcome_coverage = 0.229` is inflated by at least 0.05 versus a strict *attributed-only* ratio that counts only hypotheses and mvps reachable from an active scoring goal via `parents:` traversal.

This matters because unattributed nodes score by grace (the docstring in `goal_attribution` says "most of this corpus predates goal nodes") but the corpus has grown since — an unattributed hypothesis may simply be an orphan that no active goal owns, contributing denominator weight to a ratio it does not represent. G3 forbids motion that moves the score; unattributed hypotheses constitute exactly that — dead-weight denominator nodes that *keep* the score stationary by existing, while adding real goal-attributed hypotheses would lower it. The test determines whether the gap is material.

### Why this is distinct from sibling hypotheses

- **a03** claims 20% of mvps are orphaned from active goals — a numerator-only claim. This hypothesis targets the *denominator*: unattributed **hypotheses** inflating `outcome_coverage` by weighing down the denominator with nodes that cannot reach an active goal.
- **a04/a05/a06/a07** describe per-goal breakdowns of the aggregate. This hypothesis tests whether the aggregate ratio is structurally inflated by unattributed nodes at all — regardless of per-goal distribution — and by how much.
- **a00-9aeafcd1** measured per-goal variance but did not measure the unattributed-vs-attributed gap on the whole-graph ratio.

### What would prove it

Run the existing `goal_attribution()` instrumented to separate the scoring counts into two buckets:

1. **Attributed:** hypotheses/mvps where `goals_of(nid)` is non-empty AND at least one goal has status in `SCORING_GOAL_STATUSES`.
2. **Unattributed:** hypotheses/mvps where `goals_of(nid)` is empty — no transitive parent-chain path to any goal node.

Compute:
- `coverage_attributed = mvps_attributed / hyps_attributed`
- `coverage_full = (mvps_attributed + mvps_unattributed) / (hyps_attributed + hyps_unattributed)` (current ratio)
- `gap = coverage_full - coverage_attributed`

**Proof:** `gap >= 0.05` — meaning at least 5 percentage points of the current `outcome_coverage` come from unattributed denominator weight. A gap of 0.05 matters because `outcome_coverage = 0.229`; a 0.05 reduction would be a 22% relative drop.

Implementation: a short experiment script or extended `goal_attribution` call that returns the breakdown.

### What would disprove it

1. `gap < 0.02` — unattributed nodes contribute negligibly to the ratio's inflation. The aggregate is an accurate summary of goal-attributed progress.
2. `hyps_unattributed = 0 AND mvps_unattributed = 0` — all scoring hypotheses and mvps are already goal-attributed, meaning the 596 unattributed nodes are exclusively non-scoring types (build, idea, outcome, etc.).
3. `gap` reverses sign (`coverage_attributed > coverage_full`) — unattributed nodes have *fewer* mvps per hypothesis than attributed ones, making them a drag rather than an inflation.

### Edge cases

- A hypothesis whose `goals_of()` reaches a retired/complete goal is *not* unattributed — it IS attributed, just to a non-scoring goal. The `leaving` logic in `goal_attribution` already handles this (retired goals → node leaves scoring). This hypothesis tests only the `goals_of()` empty case, because the leaving/node-deprecated paths are already verified.
- A hypothesis unattributed because of a data problem (broken `parents:` link, missing node) is still unattributed. The gap measurement doesn't care *why* — it only measures what the metric does today versus what it would do with a strict attribution filter.
- The `max(..., 1)` denominator clamp in `outcome_coverage` applies. If `hyps_attributed = 0`, the result is 0/1 = 0.0, not NaN — and `gap = 0.229 - 0.0 = 0.229`, which would prove the claim dramatically.

## Agent Notes
Hypothesis: current outcome_coverage=0.229 is inflated by unattributed-hypothesis denominator weight. 596/974 active nodes (61%) are unattributed (no goal reachable via parent chain). Claim: filtering to only goal-attributed hyps/mvps drops coverage by >=0.05. Distinct from siblings: targets denominator (unattributed hyps), not numerator (orphan mvps like a03) or per-goal breakdown (a04-a07). No experiment run. Pending.
