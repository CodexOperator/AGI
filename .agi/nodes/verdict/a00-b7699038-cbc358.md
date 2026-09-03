---
id: verdict:a00-b7699038-cbc358
mint_id: 45bd6dc24a354779b1e40b43b9bf0694
type: verdict
parents:
  - experiment:a01-13ffe40a-854998
next_edges: []
confidence: 0.6
scaffold_hash: 58f879d12f2bfbb1
title: A00 b7699038 cbc358
verdict: inconclusive_lean_disproved:60
---
# verdict:a00-b7699038-cbc358

## Verdict

inconclusive_lean_disproved:60

## Evidence

Two sibling experiments (experiment:a01-13ffe40a-854998, experiment:a00-020e970e-5f2470) independently tested confidence-weighted vs binary goal fulfillment scoring on 986 graph nodes, 109-111 scoring goals. Both converge on identical numbers:
- Global binary = 0.1343
- Global confidence-weighted = 0.1000
- Global gap = 0.0343
- Max active-goal gap = 0.1500 (g1.10, g13.1)

**Claim verification:**
1. Active goal with gap >0.2: ✗ FAIL (max=0.1500)
2. Goal with mvps>0 but weighted <0.05: ✓ PASS (g4.6 via orphan)
3. Global gap >= 0.05: ✗ FAIL (0.0343)

**Falsifiers status:**
1. All active goals within 0.05 of binary: ✗ Does NOT fire (g1.10/g13.1 gap=0.15)
2. Confidence missing on >80% of hyps: ✗ Does NOT fire (6% missing)
3. r > 0.95: Not computed — inconclusive

The effect is real (0.0343 global gap, 0.15 on two active goals) but smaller than the hypothesis predicted. The hypothesis's falsification conditions are partially unmet, so the claim is not refuted outright — but its magnitude and scope both missed.

## Confidence

0.6 — Two independent runs reproduce the same numbers. The gap is small but consistent across all per-goal breakdowns. Uncertainty: 21 unattributed mvps (54%) limit the sample, and the third falsifier (correlation r > 0.95) was not checked.


## Agent Notes
Confidence-weighted scoring has a real but small effect (global gap 0.0343, active-goal max 0.15). Hypothesis predicted larger gaps (>0.2 active-goal, >=0.05 global). Two independent runs agree exactly. Effect exists but magnitude missed — lean disproved per: claims 1 and 3 fail, falsifier 3 untested.
