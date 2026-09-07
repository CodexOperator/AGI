---
id: hypothesis:a00-c8b56cd1-d985fa
mint_id: 4b1fc820f9c74475a81b19d6cc10e08f
type: hypothesis
parents:
  - goal:g3
next_edges: []
confidence: 0.0
edited_by: season.py
scaffold_hash: a5b29514730b65f3
season: 1
testable_claim: Fraction of scoring mvps whose nearest hypothesis ancestor has verdict "disproved" is >= 0.1 on the real corpus, confirming that binary outcome_coverage credits disproven claims as goal-fulfilment.
thought_session: season
title: "Verdict polarity asymmetry: disproved mvp counts as goal-fulfilment"
verdict: pending
---
# hypothesis:a00-c8b56cd1-d985fa

## Hypothesis

**Claim:** Binary `outcome_coverage` counts mvps identically regardless of the
hypothesis verdict that produced them — a `disproved` hypothesis with an mvp
contributes the same numerator weight as a `proved` one. This is fundamentally
wrong for goal-fulfilment scoring: disproving a hypothesis means the claimed
path does NOT achieve the goal. Counting that mvp as "coverage" inflates the
metric by crediting dead-end work as progress toward the goal.

### Why this is distinct from sibling hypotheses

| Hypothesis | Angle |
|---|---|
| a00-dc761315 | lifecycle decoupling: verdict_exists vs mvp_exists (any verdict vs pending) |
| a00-ee08875d | confidence-weighting: scales mvp contribution by hypothesis confidence |
| a00-b315c6a4 | confidence does not predict verdict (correlation, not asymmetry) |
| a01-35f3a362 | evidence gate checks existence not type |
| **this** | **verdict polarity: disproved ≠ proved in goal-fulfilment** |

All existing hypotheses address *whether* evidence exists, *how strong* it is,
or *which goal* gets credit. None address that a disproved claim is
functionally *anti-progress* for the goal it belongs to — counting it as
coverage is structurally wrong, not just imprecise.

`disproved` is a valid scientific outcome (the hypothesis was testable and
tested), but it should not inflate goal-progress scoring. The metric should
either exclude `disproved`-backed mvps, or require a separate "exploration"
tracker orthogonal to goal-fulfilment.

### Testable claim

For every scoring mvp in the corpus, walk its `parents:` chain upward to find
the nearest hypothesis ancestor. Let `D` = number of scoring mvps whose
nearest hypothesis ancestor has `verdict: disproved`. Let `T` = total scoring
mvps. The claim holds if `|D| / |T| >= 0.1` — at least 10% of the "coverage"
numerator comes from disproven claims.

This is a conservative threshold. Even 5% would be material given that
outcome_coverage is the primary metric and goal:g3 forbids motion that moves
score — counting disproven work as coverage IS motion that moves score, but
under the opposite sign: it moves score WITHOUT making goal progress.

### What would prove it

1. **Real corpus measurement:** Run `goal_attribution()` from `metrics.py` to
   enumerate all scoring mvps. For each, walk `parents:` chain upward. Record
   verdict of nearest hypothesis ancestor. Compute `fraction_disproven_mvps` =
   `count(verdict == disproved) / total_scoring_mvps`. Report >= 0.1.

2. **Synthetic corner case:** Construct a corpus where goal G has 5 hypotheses
   (H1–H5), all `disproved` with full evidence chains, each with one child mvp.
   `outcome_coverage` = 5/5 = 1.0. True fulfilled progress = 0/5 = 0.0. The
   divergence is 1.0 — the metric is maximally misleading.

3. **Mixed corpus:** A corpus where `proved` hyps have mvps AND `disproved`
   hyps have mvps. Demonstrate that `outcome_coverage` is strictly higher than
   `proved_only_outcome_coverage` (mvps from proved hyps / total hyps) by
   > 0.05.

### What would disprove it

1. `|D| / |T| < 0.05` on the real corpus — disproved-backed mvps are so rare
   that the polarity asymmetry is practically irrelevant.

2. No hypothesis in the corpus has both `verdict: disproved` AND a reachable
   mvp descendant — the condition never fires because the lifecycle stages
   don't overlap (if `disproved` is assigned, the chain stops before an mvp).

3. `proved_only_outcome_coverage` correlates with `outcome_coverage` at
   Pearson r > 0.99 — removing disproved-backed mvps is a rounding error.

4. The `parents:` chain from an mvp to its hypothesis is too broken to
   attribute reliably (>30% missing edges), making the measurement
   high-noise regardless of polarity.

### Edge cases

- **Hypothesis with no verdict (pending):** Counted as `disproved`-backed in
  the strict sense? No — `pending` means unsettled, so the mvp's unproven
  status is already captured by `confidence: 0.0` defaults. The polarity
  hypothesis only counts explicit `verdict: disproved`. Pending hyps with
  mvps are a separate problem (covered by a00-dc761315).

- **Mvp with multiple hypothesis ancestors:** Use the nearest hypothesis (the
  shortest parent-chain walk). If multiple hypotheses at equal distance, use
  the one with the most restrictive verdict (disproved > proved > pending).

- **Disproved hypothesis with no mvp:** Does NOT affect the metric. The claim
  is about mvps counted as progress when they shouldn't be, not about
  disappeard work being invisible.

### Why this matters for G3

G3 says: *no primary metric that appending hops can shift*. Verdict polarity
asymmetry is a flaw orthogonal to hopping — it shifts the metric without
adding hops AND without adding goal progress, by simply creating mvps for
disproven claims. This is a distinct failure mode:

- Hop-padding shifts `longest_chain_length` (already demoted to descriptive)
- Confidence-padding shifts `confidence_weighted_score` (a00-ee08875d)  
- **Disproved-backed mvps shift `outcome_coverage` itself** — the existing
  primary, right now, today, with zero new infrastructure

Closing this gap is a precondition for L4 (true goal-fulfilment scoring)
because any per-goal metric built on the same mvp-numerator will inherit
the same polarity blindness.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review a07-4e294c0c (2026-09-03): accepted the hypothesis as written —
no body change — but ran the corpus audit the node's "What would prove it" step
1 describes, so the next experiment kid does not burn a turn rediscovering it:
this corpus has **zero** `verdict: disproved` hypotheses (4 nodes corpus-wide
carry `verdict: disproved`; exactly one is a `verdict`-type node, and it has no
live mvp descendant). Walked all 39 non-deprecated mvps to their nearest
hypothesis and nearest verdict ancestor: **0** are disproved-backed either way.
So on the real corpus the testable claim is vacuously falsified today
(0/39 = 0 < 0.05) — falsifier #2 is the current state, and #1 would fire
immediately if the audit is run. The design-level claim (the mvp numerator is
polarity-blind, which every L4 per-goal metric would inherit) stands on the
synthetic tests #2/#3, which remain the right place to spend the experiment.
Also noted for the record: the kid reported "1381/1381 tests pass, single edit
" — verified the working tree; the only change was this node. No engine code
touched, so the full-suite claim is a sanity check, not a change claim.
<!-- THOUGHT:END -->



## Agent Notes
Filed hypothesis on verdict polarity asymmetry: disproved-backed mvps inflate outcome_coverage by counting dead-end work as goal-fulfilment. Untested (pending).