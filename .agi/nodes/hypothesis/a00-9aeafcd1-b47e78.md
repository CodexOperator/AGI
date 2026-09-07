---
id: hypothesis:a00-9aeafcd1-b47e78
mint_id: 1c24fa3a176e4c24b00a9d47af8e17cd
type: hypothesis
parents:
  - goal:g3
next_edges: []
confidence: 0.0
edited_by: season.py
scaffold_hash: a450cbcb416a0724
season: 1
thought_session: season
title: A00 9aeafcd1 b47e78
verdict: pending
---
# hypothesis:a00-9aeafcd1-b47e78

## Hypothesis

Per-goal outcome coverage disaggregates the aggregate metric and exposes
patterns—coverage concentration, zero-coverage goals, over-coverage from
convergent chains—that the pooled `outcome_coverage` (mvps / hypotheses)
makes invisible and therefore gameable.

**Testable claim:** Computing `outcome_coverage` per-goal (for each goal,
mvps descending from that goal / hypotheses descending from that goal) will
show a distribution with wider variance and a lower per-goal *mean* than the
aggregate, meaning the pool is already masking the fact that most goals have
near-zero or zero coverage while a few bear all the weight.

**What would prove it:**
- The per-goal mean is lower than the aggregate `outcome_coverage`.
- At least one scoring-eligible goal has zero coverage (hypotheses with no
  mvp) — meaning its chains contribute denominator weight to the
  aggregate without any numerator, a form of dead-weight averaging.
- At least one goal has `coverage > 1.0` (mvps outnumber hypotheses),
  indicating convergent chains terminating at the same mvp — a case where
  the aggregate sees "more outcomes" per hypothesis than exist as distinct
  results.

**What would disprove it:**
- Every scoring-eligible goal has roughly the same per-goal coverage as
  the aggregate, with variance below 0.05 — meaning the pool is a faithful
  representation of each goal individually.
- No goal has `coverage > 1.0` (no convergent chain artifact).
- No scoring-eligible goal has zero coverage (every goal has at least some
  mvp-terminal chains).

**Initial evidence (measured 2026-09-03 on the agi corpus):**
- Aggregate `outcome_coverage`: 0.250 (39 mvps / 156 hyps ← all nodes).
- Pooled over scoring-status goals only: 0.353 (18 mvps / 51 hyps).
- Per-goal mean (scoring goals with data): 0.551, **higher** than pooled —
  but range is 0.000–3.000; stddev 0.739.
- **goal:g3** itself: 12 hyps, 0 mvps, cov=0.000 — a zero-coverage goal
  whose 12 hypotheses contribute 23.5% of the scoring-hypothesis denominator
  and 0% of the numerator.
- At least one goal shows cov > 1.0 (mvps > hyps), indicating convergent
  chains that inflate the numerator.

These bullet points are initial measurements, not a settled result. The
formal claim—that per-goal distribution is a strictly more informative
(and game-resistant) signal than the aggregate—is what this hypothesis
tests by applying `goal_attribution`-style traversal per goal and comparing
the distributions.


## Agent Notes
Per-goal outcome coverage disaggregates the aggregate metric to expose gaming patterns (zero-coverage goals, convergent chains, coverage concentration) that the pooled outcome_coverage masks. Initial measurements show goal:g3 itself at 0.000 coverage (12 hyps, 0 mvps) and at least one goal with cov > 1.0.