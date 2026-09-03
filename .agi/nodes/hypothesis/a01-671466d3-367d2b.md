---
id: hypothesis:a01-671466d3-367d2b
mint_id: 6d98b7d59aad4f9d97ef3a611b46dd89
type: hypothesis
parents:
  - goal:g3
next_edges: []
confidence: 0.0
scaffold_hash: 73f1110d55629f32
title: A01 671466d3 367d2b
verdict: pending
---
# hypothesis:a01-671466d3-367d2b

## Hypothesis

**Claim.** The existing `goal_attribution()` function in `metrics.py` traces every non-goal node to its ancestor goals via `goals_of()`, but the metric reduces all that to one global `outcome_coverage` ratio. Per-goal outcome_coverage — for each goal, the fraction of its descendant hypotheses that reach an mvp — can be derived by inverting the same ancestry data, and will reveal meaningful variance (≥0.1 spread) between goals that the aggregate number hides.

**Proved by.** Implementing `per_goal_outcome_coverage()` in `metrics.py` that re-uses `goals_of` (no new traversal) and emits a per-goal ratio. Running it against this corpus shows at least two scoring-status goals with ratios differing by ≥0.1.

**Disproved by.** The per-goal ratios are all within 0.05 of each other — meaning the aggregate was already a faithful summary and the per-goal view adds no insight.

**Motivation (L4).** goal:g3 flags per-goal scoring as the unbuilt gap. A hypothesis that spawns under one goal and reaches mvp under another is counted once in the global ratio, but neither goal gets credit proportional to its stake. Fixing this closes L4 without changing the primary metric — the per-goal view is diagnostic, not a replacement for `outcome_coverage`.


## Agent Notes
Hypothesis: per-goal outcome_coverage can be derived from existing goal_attribution's goals_of data, revealing variance (>=0.1 spread) between goals that the global aggregate hides. Closes L4 gap — per-goal scoring is diagnostic, not primary metric replacement.
