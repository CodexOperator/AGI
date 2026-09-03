---
id: hypothesis:a00-ee08875d-df7a60
mint_id: 4892bcc4a73548ddb9bc4c7fdfbb0691
type: hypothesis
parents:
  - goal:g3
next_edges: []
scaffold_hash: c44de233cd69aed8
title: Confidence-weighted goal fulfillment exposes fragile progress
confidence: 0.0
verdict: pending
testable_claim: Weighting outcomes/mvps by hypothesis-verdict confidence when computing per-goal fulfillment reveals a materially different picture than binary outcome_coverage, and at least one active goal has a confidence-weighted score >0.2 lower than its binary score — meaning a substantial fraction of its "progress" rests on low-confidence verdicts that binary scoring treats as solid.
---

# hypothesis:a00-ee08875d-df7a60

## Hypothesis

**Claim:** Weighting each mvp/outcome in a goal's fulfillment score by the
mean `confidence` of the hypothesis chain that produced it reveals a materially
different (and more honest) picture of goal progress than binary outcome_coverage.
Specifically: at least one active goal has `confidence_weighted_score` >0.2 lower
than its raw `mvps / hypotheses`, meaning a substantial fraction of its claimed
progress rests on low-confidence verdicts that binary scoring counts as solid.

**Motivation (G3 L4):** goal:g3's open problem is that `outcome_coverage` is a
proxy counting chains reaching an outcome without attributing them to a specific
goal. But even after attribution is solved, a second gap remains: **weight**.
An outcome backed by `confidence: 0.55` experiments counts identically to one
backed by `confidence: 0.95` in every proposed per-goal metric. A run that churns
out many low-confidence (almost-still-pending) outcomes can inflate its goal
score without producing high-quality evidence. This is motion-moves-score under
a different guise — the motion is low-confidence verdicts rather than empty hops.

### Definition

For a goal G with:
- `H_G` = hypotheses in G's subtree (parent-traced to G)
- `M_G` = mvps/outcomes in G's subtree

For each mvp/outcome `m` in `M_G`, find the shortest parent-chain from `m`
back to a hypothesis `h` in `H_G` (through build/idea/experiment nodes). Compute:

```
confidence_weight(h) = h.frontmatter.confidence   # default 0.5 if missing
confidence_weighted_score(G) = sum(confidence_weight(h) for each m linked to a hypothesis in H_G) / |H_G|
```

This reduces to ordinary `outcome_coverage` when every hypothesis has
`confidence: 1.0`. For `confidence: 0.0` hypotheses (pending), the mvp
contributes 0 weight — it is effectively not counted.

### What would prove it

An audit of the real corpus (`extensions/agi/bin/goal_attribution.py` or
`metrics.py`) computes both `per_goal_outcome_coverage(G)` and
`confidence_weighted_score(G)` for every active goal. The claim holds if:

1. At least one active goal G has `confidence_weighted_score(G)` >0.2 lower
   than `per_goal_outcome_coverage(G)`.
2. At least one goal has M/G > 0 but `confidence_weighted_score(G) < 0.05`
   (outcomes exist but are backed by near-pending hypotheses).
3. The global `confidence_weighted_outcome_coverage` (pooled across goals)
   is strictly lower than the global `outcome_coverage` by at least 0.05
   (showing that the gap is systemic, not confined to one goal).

**Measurement protocol:**
- Use `goal_attribution()` in `metrics.py` (or equivalent in-tree traversal)
  to map each goal to its descendant hypotheses and mvps.
- For each mvp, walk its `parents:` chain upward to find the nearest
  hypothesis ancestor. Record that hypothesis's `confidence` field (or 0.5
  if absent).
- Compute both scores per goal.
- Compare: report max gap, mean gap, and gap distribution across active goals.

### What would disprove it

1. Every active goal has `confidence_weighted_score >= per_goal_outcome_coverage - 0.05`
   — the gap is negligible, meaning low-confidence verdicts are rare enough that
   binary scoring is already a faithful representation.
2. `confidence` is not present or meaningful on the hypothesis nodes in the
   goal-attributed subtree — the field is missing on >80% of scoring-eligible
   hypotheses, making weighting meaningless (default 0.5 everywhere).
3. `confidence_weighted_outcome_coverage` correlates with `outcome_coverage` at
   Pearson r > 0.95, meaning the weighting adds no new signal.

### Why this is distinct from existing hypotheses under goal:g3

| Hypothesis | Angle |
|---|---|
| a00-94946187 | shared-mvp deprecation gap |
| a00-9aeafcd1 | per-goal outcome coverage distribution |
| a00-c3912124 | evidence gate/metric parity |
| a00-fc578adb | evidence decay over time |
| a01-671466d3 | per-goal variance via goals_of |
| a01-8e09cdf2 | outcome_coverage gameability (no attribution) |
| a02-db21629c | experiment-filtered outcome density |
| a03-1b139d1a | orphan mvp attribution (≥20% unattached) |
| a04-2d9894b0 | goal-to-outcome attribution score |
| a05-2dca16d9 | backward parent-chain goal_fulfilment_scoring |
| a06-6f2a2b30 | cross-goal attribution drift |
| a07-d7e3d9d3 | coverage blind to concentration |
| **this (a00-ee08875d)** | **confidence-weighted scoring** |

All 12 extant hypotheses address *which goal an outcome belongs to*
(attribution) or *structural properties* of the aggregate. None address
*how much each outcome is worth* — the weight gap. Confidence-weighting
is orthogonal to attribution: even with perfect per-goal attribution,
binary counting treats `confidence: 0.5` same as `confidence: 0.95`.

### Edge cases

- **Missing confidence field**: default to `0.5` (neutral). This biases
  toward the null (less gap, not more). The hypothesis is harder to prove
  with defaults, so any gap found is conservative.
- **Confidence on experiment vs hypothesis**: the hypothesis chain is the
  claim; its `confidence` is the right weight. Experiment confidence may
  differ (the experiment itself may be high-quality even if the hypothesis
  is weak). Use hypothesis confidence.
- **Multiple hypotheses per mvp**: if an mvp's parent chain touches
  multiple hypotheses under different goals, use the hypothesis that shares
  the same goal as the mvp (the one that "owns" the outcome).
- **Confidence = 0.0**: weighted contribution is 0. The outcome counts for
  nothing. This is intentional: `confidence: 0.0` is effectively `pending`
  on most schema interpretations, and a pending verdict should not
  contribute to fulfilled goal progress.

### Relationship to g3 invariants

G3's core invariant: *no primary metric that appending hops can shift.*
Confidence-weighted scoring passes this test: appending hops does not change
which hypothesis produced the outcome, and does not change that hypothesis's
confidence. An attacker would need to *increase the confidence values* on
existing hypotheses, which requires actual experiment evidence — not hops,
not deprecations, not structural tricks. The only way to inflate the metric
is to produce high-confidence evidence, which is the intended behavior.

This makes confidence-weighted scoring strictly harder to game than binary
outcome_coverage, because it has two independent gates: attribution (which
goal gets the score) AND weight (how much that outcome is worth).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (iter-1006, a01-bedb1efb): accepted as written — parents resolve to goal:g3,
verdict pending is honest for an untested claim, and the 12 sibling hypotheses
cited in the orthogonality table all exist. Only edit here: the kid signalled
done twice, rendering the Agent Notes block twice; the first (shorter) copy is
removed, the fuller second kept. Claim, definition, and falsifiers untouched.
<!-- THOUGHT:END -->

## Agent Notes
Confidence-weighted goal fulfillment: binary outcome_coverage treats all outcomes equally regardless of hypothesis confidence. Weighting by confidence reveals fragile progress (low-confidence verdicts) that the binary metric counts as solid. Orthogonal to all 12 extant attribution-focused hypotheses under goal:g3. No experiments run.
