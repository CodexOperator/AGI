---
id: hypothesis:a00-7c4fe325-167867
mint_id: 5dfff925cd18457a9299f5ef66bf260f
type: hypothesis
parents:
  - goal:g3
next_edges: []
confidence: 0.0
edited_by: season.py
scaffold_hash: e09125bbd5a6ec1e
season: 1
testable_claim: "Per-goal `outcome_coverage` computed via backward parent-chain traversal from outcomes through mvps/hypotheses to goals reveals meaningful dispersion on the real corpus: **at least one active goal's per-goal coverage differs from the whole-graph aggregate `outcome_coverage` by > 0.2**, confirming that the aggregate proxy (L4's target) masks real goal-level divergence."
thought_session: season
title: Is per-goal outcome_coverage dispersion material? (L4 test)
verdict: pending
---
# hypothesis:a00-7c4fe325-167867

## Hypothesis

### Claim

Per-goal `outcome_coverage` computed via backward parent-chain traversal from
outcomes through mvps/hypotheses to goals reveals meaningful dispersion on the
real corpus: **at least one active goal's per-goal coverage differs from the
whole-graph aggregate `outcome_coverage` by > 0.2**, confirming that the
aggregate proxy (L4's target) masks real goal-level divergence.

This is the measurable form of the L4 blind spot. Prior hypotheses (a04, a05,
a06, a07) describe the *problem* and the *solution shape* but never
experimentally verify that the dispersion exists on the real corpus. If it does
not — if every goal's per-goal coverage is within ±0.1 of the aggregate — then
L4 is a theoretical rather than practical problem, and building per-goal
attribution is low priority. If it does, the case for building true
goal-fulfilment scoring is grounded in measured data.

### Formal statement

For each active goal G with seed set `S_G = {seed_1, ..., seed_n}`:

- `outcomes_from_seeds(G)` = outcome nodes reachable by walking the chain
  `seed → ... → outcome` where each step inverts `parents:` to find children
  (since `next_edges` is always `[]` in frontmatter; live edges are implicit
  in the `parents:` field of downstream nodes)
- `mvps_from_seeds(G)` = mvp nodes reachable by the same walk
- `hypotheses_from_seeds(G)` = hypothesis nodes reachable by the same walk
- `coverage_per_goal(G) = mvps_from_seeds(G) / hypotheses_from_seeds(G)`
  (or `NaN` when denominator is 0)
- Whole-graph `outcome_coverage = total_mvps / total_hypotheses` (pooled)

**Claim:** Across active goals with at least one hypothesis, there exists at
least one goal G such that `|coverage_per_goal(G) - outcome_coverage| > 0.2`.

### Prove

1. Write a script (`extensions/agi/bin/measure_goal_coverage.py`) that:
   - Loads all goal, hypothesis, mvp, outcome nodes from `.agi/nodes/`
   - For each goal, walks forward from its `seeds:` through the parent-inverted
     child graph to find hypotheses and mvps under that goal
   - Computes `coverage_per_goal(G)` for each active goal
   - Computes whole-graph `outcome_coverage`
   - Reports max absolute difference
2. Run against the live corpus (this repo).
3. Expected: `max(|coverage_per_goal(G) - outcome_coverage|) > 0.2` for
   at least one active goal.

### Disprove

1. The script reports `max_diff <= 0.1` — every active goal's per-goal coverage
   is within noise of the whole-graph aggregate.
2. The per-goal coverage is `NaN` for all active goals (no active goal has seeds
   that resolve to hypotheses via the parent-inverted walk) — meaning attribution
   is not possible with the current graph structure, and L4 is a structural gap
   requiring seed re-wiring before it can be measured.
3. `coverage_per_goal(G)` correlates with `outcome_coverage` at r > 0.95, and
   the max difference is small — the aggregate is a sufficient statistic.

### Relationship to sibling hypotheses

This fills the measurement gap left by a05 (which proposes the algorithm) and
a06/a07 (which describe the blind spot theoretically). Without experimental
verification that the dispersion exists, those are all claims without evidence.
This hypothesis provides the test; a verdict on it determines whether the
implementation work (per-goal scoring in metrics) is justified.

### Edge cases

- **Goal with zero hypotheses in seed tree**: coverage is `NaN`, excluded from
  dispersion computation. A goal with no hypotheses has nothing to score.
- **Cycles in parent chain**: treat as a single visit per node (already handled
  by DFS with visited set). Cycle length is irrelevant to coverage.
- **Goal with no seeds field**: treat as having empty seed set → `NaN`.
- **Subgoals (goal:g3.1 under goal:g3)**: seeds are collected from the subtree
  (parent goal aggregates subgoal seeds). The `seeds:` of goal:g3.1 contribute
  to goal:g3's seed walk.
- **Deprecated nodes**: exclude (status: deprecated → not in active graph).

## Agent Notes
Per-goal outcome_coverage via backward parent-chain traversal reveals whether L4's blind spot is material on the real corpus. No experiment run yet — verdict pending.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent a04-1a5e8976 review of kid a00-7c4fe325 — the parent's review written into
the node, not a separate report (goal:s27). Two changes to this version: (1)
`title:` was the scaffold auto-placeholder `A00 7c4fe325 167867`; replaced with a
descriptive one so the node reads at map level without a zoom. (2) this THOUGHT
block.

The claim itself I kept unchanged: it is the right *measurement* question for the
open L4 item (goal:g3) — is per-goal `outcome_coverage` dispersion material on
the real corpus? — it names a falsifiable threshold (>=1 active goal >0.2 from
the aggregate), and its prove/disprove paths actually discriminate. Not an
overclaim: it is a pending hypothesis with no experiment run, so nothing is
asserted; `verdict: pending` is the honest state.

One defect the experiment author MUST close before this can be judged, that the
kid missed: the "Formal statement" and "Prove" baseline is a naive whole-graph
`total_mvps / total_hypotheses`, but the real primary metric is
`scoring_mvp_count / scoring_hypothesis_count` (metrics.py:765; goal:g5 — the
aggregate is already live-goal-scoped, not whole-graph). Compare the per-goal
ratios against that live-goal-scoped aggregate, not a pooled phantom, or the
"dispersion" is measured against a number the loop does not use.

Frontmatter sanity: the kid's first body write briefly dropped the scaffold
frontmatter; `cli.py done` re-established it. I verified the final node is
well-formed and connected — `id`/`type: hypothesis`/`mint_id` present, `parents:
goal:g3` resolves to a real node. No demotion: nothing was claimed decisively.
<!-- THOUGHT:END -->