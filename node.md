---
id: hypothesis:a00-b315c6a4-b89059
mint_id: cdf857c7159b4709be9d35d2adc2f4a0
type: hypothesis
parents:
  - goal:g3
next_edges: []
confidence: 0.0
edited_by: season.py
scaffold_hash: a58f91021358ee56
season: 1
testable_claim: "For hypothesis nodes with a definitive verdict (proved or disproved) and a confidence field, there is no statistically significant correlation between confidence and verdict outcome: AUC < 0.65, or Mann-Whitney U p > 0.05, or mean proved confidence within 0.1 of mean disproved confidence."
thought_session: season
title: Confidence prediction bias — hypothesis confidence does not predict verdict outcome
verdict: pending
---
# hypothesis:a00-b315c6a4-b89059

## Hypothesis

**Claim:** The `confidence` field on hypothesis nodes is a record of author overconfidence, not a calibrated posterior probability. For hypotheses that have reached a definitive verdict (`proved` or `disproved`), there is no statistically significant correlation between the `confidence` value written at creation time and the eventual verdict outcome. High-confidence (≥0.8) hypotheses are as likely to be `disproved` as low-confidence (≤0.2) hypotheses are to be `proved`.

**Why this matters for G3 (L4):** a00-ee08875d proposes weighting per-goal outcome scores by hypothesis confidence — a `confidence: 0.55` outcome counts less than a `confidence: 0.95` one. But if the confidence field is uncorrelated with actual claim resolution, this weighting introduces noise, not signal. Worse: it creates a *new* gaming vector — an author can inflate the goal score by writing high-confidence hypotheses regardless of whether they ever reach `proved`. This is motion that moves the score, exactly what G3 forbids.

The hypothesis tests the foundational assumption that `confidence` carries resolution signal before it is used as a weight.

### Formal statement

Let `H` be the set of hypothesis nodes with `verdict ∈ {proved, disproved}` and a `confidence` field present in frontmatter. Partition `H` into `P = {h ∈ H | verdict = proved}` and `D = {h ∈ H | verdict = disproved}`. Let `C(h)` be the confidence value.

**Null hypothesis H₀:** `mean(C(P)) ≈ mean(C(D))` within 0.1, and the distributions are not distinguishable beyond chance (Mann-Whitney U, p > 0.05).

**Alternative H₁:** `mean(C(P)) - mean(C(D)) ≥ 0.2` with p < 0.01 (confidence directionally predicts verdict), or the distributions are separable with AUC > 0.65.

### What would prove it (H₀ holds — confidence is not predictive)

An audit of the real corpus (all `.agi/nodes/hypothesis/*.md`) finds:

1. **Mean difference < 0.1** — proved hyps have mean confidence within 0.1 of disproved hyps.
2. **Mann-Whitney U p > 0.05** — the two distributions are not distinguishable.
3. **AUC < 0.65** — confidence as a classifier for proved/disproved is near-random.
4. **High-confidence disproved rate observed** — at least one hypothesis with `confidence ≥ 0.8` was `disproved`, demonstrating that high confidence does not protect against decisive falsification.

**Measurement protocol:**
- Parse all hypothesis node files (`.md` with `type: hypothesis`).
- Extract `verdict`, `confidence` from frontmatter. Exclude hyps where `confidence` is absent or `verdict` is `pending`/`inconclusive_lean_*`.
- Compute per-group statistics: count, mean confidence, median, std.
- Two-sample Kolmogorov-Smirnov or Mann-Whitney U between proved and disproved groups.
- AUC via logistic regression on confidence as sole predictor of proved (1) vs disproved (0).
- Plot histograms for visual inspection of overlap.

**Synthetic proof:** Construct two toy corpora:
- **Test A (no signal):** 10 proved hyps with confidence sampled uniformly [0.0, 1.0], 10 disproved hyps also uniform [0.0, 1.0]. AUC ~0.5, p ~1.0. This is the null case where the hypothesis is true.
- **Test B (strong signal):** 10 proved hyps all confidence ≥ 0.7, 10 disproved hyps all ≤ 0.3. AUC > 0.9, p < 0.01. This demonstrates the measurement can detect signal when it exists.

### What would disprove it (H₁ holds — confidence IS predictive)

1. **AUC > 0.75** — confidence reliably separates proved from disproved (usable as a weight).
2. **Mean diff > 0.2 with p < 0.01** — proved hypotheses carry substantially higher confidence, and the difference is statistically significant.
3. **Zero high-confidence disproved hyps** — no hypothesis with `confidence ≥ 0.8` was ever `disproved`, meaning the field is effectively a forecast (never oversold).
4. **Missing confidence correlates perfectly with pending** — the field is never absent on resolved hyps, so a00-ee08875d's default-0.5-for-absent problem never arises (the default-bias is zero).

### Edge cases and caveats

- **Confidence at creation vs verdict time:** The `confidence` field may have been updated after the verdict. The hypothesis tests the *current* confidence against the *current* verdict — if authors retroactively adjust confidence after the outcome is known, the data would show correlation that is not predictive (look-ahead bias). To control for this, compare only hyps where `confidence` was written before the verdict iteration (requires grid.py version history). If this is infeasible, note the caveat and test against current state, acknowledging the look-ahead risk.
- **Confidence 0.0 on non-pending:** Some schemas treat `confidence: 0.0` as de facto pending. If a proved hyp has confidence 0.0, it may be a schema mismatch rather than a low-confidence claim. Flag these as anomalies.
- **Small corpus size:** If the resolved (proved + disproved) hypothesis count is < 30, statistical power is low. Report effect size with confidence intervals regardless of significance.
- **Hypotheses without confidence field:** a00-ee08875d defaults these to 0.5. This hypothesis tests whether the absence pattern itself is informative — e.g., do missing-confidence hyps resolve differently?

### Relationship to sibling hypotheses

| Hypothesis | Angle | Relation to this one |
|---|---|---|
| **a00-ee08875d** | Confidence-weighted scoring | **Direct target**: this hypothesis tests whether confidence is predictive enough to use as a weight. If not, a00-ee08875d's proposal adds noise. |
| a00-dc761315 | Verdict vs mvp lifecycle | Orthogonal — tests lifecycle stages, not confidence calibration. |
| a00-94946187 | Deprecation guard gap | Orthogonal — tests deprecation arithmetic, not weight calibration. |
| a00-c3912124 | Evidence gate parity | Orthogonal — tests gate-metric consistency, not weight calibration. |
| a00-fc578adb | Evidence decay | Orthogonal — tests structural connectivity over time, not confidence |
| All attribution (a02-a07) | Goal attribution | Orthogonal — attribution says *which* goal; this says *how much weight*. The two are independent: even perfect attribution is useless if the weight is noise. |

This hypothesis is the **pre-condition check** for a00-ee08875d: before building confidence-weighted scoring, test whether the weight field carries resolution signal.

### Why this matters for the invariants

G3 forbids metrics that added motion can shift. a00-ee08875d's confidence-weighted score passes that test *if* confidence is predictive — an attacker must produce higher-quality evidence to raise the score. But if confidence is uncorrelated with resolution, the weight is a dial the author turns for free, and the score is gameable by inscribing high confidence on weak claims. Testing the calibration of the field before using it is a G3 invariant check, not a distraction.


## Agent Notes
Confidence prediction bias hypothesis: tests whether hypothesis  field carries any signal about eventual verdict. Pre-condition check for a00-ee08875d's confidence-weighted scoring proposal. If confidence is uncorrelated with proved/disproved outcome, weighting by it adds noise and creates a gaming vector (inflating scores by writing high confidence on weak claims) — a G3 invariant violation.