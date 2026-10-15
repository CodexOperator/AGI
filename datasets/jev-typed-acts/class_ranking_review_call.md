# TM.50 — does the ARM2 verdict-class ranking derive the review call?

Offline only. Input `single_axis_rows.jsonl`, arm2_verdict rows, 370 acts, mean of
3 repeats. accept score s = P(proved)+P(disproved); label = `labels.q2` (accept|demote).
StratifiedKFold(5, shuffle, seed 20260918); ONE threshold fitted per train fold
(the s value maximising train agreement), applied to the held-out fold only.

## Pooled held-out results

| metric | value | bar | pass |
|---|---|---|---|
| pooled agreement | 0.7757 | >= 0.80 | **NO** |
| pooled AUC (accept positive) | 0.5688 | >= 0.70 | **NO** |
| threshold std over folds | 0.0 | < 0.05 | yes |
| pooled ECE (10 bins) | 0.3445 | — | — |
| majority control | 0.7757 | — | equal |
| ARM1 direct call (TM.47) | 0.541 / 0.581 | — | beaten |

Confusion (rows = accept/demote, cols = predicted): `[[287,0],[83,0]]`.

Per-fold thresholds: `[0.0, 0.0, 0.0, 0.0, 0.0]` (mean 0.0, std 0.0). Every train
fold's best-agreement threshold is the minimum of the accept-score range, i.e.
"call everything accept". The fitted threshold never leaves the majority rule.

In-sample diagnostic: best possible threshold on all 370 acts also gives 0.7757
— no threshold beats majority anywhere in the range. AUC 0.5688; mean s is
0.5049 on accept vs 0.4208 on demote (correct direction, tiny gap). Split by
kind: experiment acts AUC 0.543 (accept rate 0.925), verdict acts AUC 0.456
(accept rate 0.600) — the score is inert on experiments and inverted on verdicts.

## Negative gate probe

Labels permuted, same pipeline: pooled AUC 0.4962 (collapses to chance), agreement
0.7757 (majority, since the threshold is degenerate). No leak.

## Bar-by-bar verdict

PROVE needs agreement >= 0.80 AND AUC >= 0.70 AND std < 0.05 — fails the first two.
DISPROVE fires: pooled AUC 0.5688 < 0.65 and pooled agreement 0.7757 < 0.776
(exactly the majority baseline, not above it). **DISPROVED.**

The class ranking is the wrong carrier for the review axis: the accept score
ranks the human accept/demote call at 0.569 pooled, no threshold improves on
"always accept", and within verdict nodes the ranking is slightly inverted.
Repo: `class_ranking_review_call.py`, `class_ranking_review_rows.jsonl`.
