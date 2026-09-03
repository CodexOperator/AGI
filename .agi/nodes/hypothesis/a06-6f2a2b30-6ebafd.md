---
id: hypothesis:a06-6f2a2b30-6ebafd
mint_id: 305c402eec5849e982fe1d085cc44df1
type: hypothesis
parents:
  - goal:g3
next_edges: []
confidence: 0.0
scaffold_hash: 090a03e07c3c7ae9
testable_claim: Whole-graph `outcome_coverage` (mvps / hypotheses, pooled across all goals) diverges from per-goal `outcome_coverage` when hypotheses and mvps concentrate under different goals. This means the primary metric can report rising `outcome_coverage` even though no single goal's chain closure rate improved — mvps spawned under one goal inflate the numerator for hypotheses languishing under another.
title: A06 6f2a2b30 6ebafd
verdict: pending
---
# hypothesis:a06-6f2a2b30-6ebafd

## Hypothesis

### Claim

Whole-graph `outcome_coverage` (mvps / hypotheses, pooled across all goals) diverges from per-goal `outcome_coverage` when hypotheses and mvps concentrate under different goals. This means the primary metric can report rising `outcome_coverage` even though no single goal's chain closure rate improved — mvps spawned under one goal inflate the numerator for hypotheses languishing under another.

This is the concrete form of L4: **the proxy is not merely imprecise, it is systematically confounded**. A hypothesis under goal:g3 that never reaches an mvp can still benefit from mvps produced under goal:g1 or goal:g2, because the ratio pools everything.

### Proved (what evidence looks like)

Compute per-goal `outcome_coverage` for every goal in a corpus. Show that:

1. **Variance** — per-goal coverage varies meaningfully across goals (e.g. goal:g1 has 0.5, goal:g3 has 0.0). This proves the whole-graph aggregate masks divergence.
2. **Directional divergence** — over a run, at least one goal's per-goal coverage moves *opposite* the whole-graph aggregate, or the aggregate rises while per-goal coverage falls across all goals (impossible with uniform distribution — would require a goal with zero hypotheses to suddenly gain mvps, which is exactly the kind of structural re-weight the aggregate cannot see).

Implementation sketch: `goal_attribution` already walks `parents` from every node; it can additionally bucket `scoring_mvp_count` and `scoring_hypothesis_count` **per goal** (including `unattributed` as a pseudo-goal). `outcome_coverage` then becomes a dict `{goal_id: float}`; the whole-graph ratio is a derived summary, not the primary.

### Disproved (what disproves it)

Per-goal `outcome_coverage` is within noise of whole-graph `outcome_coverage` for every goal in the corpus — variance is low (< 0.05 std across goals), and no individual goal diverges directionally from the aggregate over any measured run. Equivalently: the whole-graph ratio is a sufficient statistic; per-goal attribution adds no signal.

### Why this is directly under goal:g3

G3 says *added motion cannot move the score*. The current guards prevent:
- padding hops (`longest_chain_length` outlawed as primary)
- padding verdicts without evidence (`evidence_runs` must resolve)
- retiring/deprecating unconverted hypotheses (`deprecation_score_delta`)

**But none of these prevent cross-goal attribution drift.** Adding more mvps under *any* goal moves the numerator; nothing ties them to the hypotheses they claim to close. A run can raise `outcome_coverage` by closing easy goals while hard goals stay open — which is motion that moved the score, exactly what G3 forbids.

L4 names this. This hypothesis makes it testable.


## Agent Notes
Filled scaffold with hypothesis on L4: whole-graph outcome_coverage is confounded by cross-goal attribution drift. Per-goal coverage would unmask this. No experiment run; verdict pending.