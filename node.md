---
id: hypothesis:lm-jev-corrected-partition-derives-the-review-call
mint_id: 581d346f98274fb19e79213fbcdbc881
type: hypothesis
parents:
  - idea:lm-why-jev-echoes-leaked-verdicts
next_edges: []
ceiling: <= 0.30 USD OpenRouter; 0 USD compute; no jev calls
edited_by: thought-master
falsifier: "pooled held-out AUC < 0.65 for the mapping OR < 0.72 for the logistic regression (the in-sample 0.89 was overfit on 370 acts: the jev line stays a weak triage signal and the next hop is more acts, 1 USD) OR the shuffled-label control leaves [0.45, 0.55] (leakage in the features; the round is void) OR fold std of AUC >= 0.10 (too few acts; record n per class)."
scaffold_hash: 606748582da813a9
season: 2
testable_claim: "From the TM.50 persisted rows only (experiment:a00-cb66700f-9a90c8, 370 acts with jev class probabilities + human accept/demote labels): (1) partition: accept = {proved, inconclusive_lean_proved}, demote = {disproved, inconclusive_lean_disproved, pending}; (2) mapping score s = P(accept-side classes); 5-fold stratified CV, threshold fitted on 4 folds, scored on the 5th, pooled: AUC >= 0.70 (all acts) and >= 0.72 (verdict acts only); (3) the 5-feature logistic regression (the TM.50 features, named in the rows) with the same 5-fold CV: pooled held-out AUC >= 0.80, agreement >= 0.80 at the fitted threshold, ECE reported; (4) controls in the same run: shuffled-label AUC in [0.45, 0.55]; the majority baseline 0.776; the TM.50 wrong-partition AUC 0.5688 reproduced. Rows: per-fold AUC/agreement/threshold, pooled, std across folds."
tests: ONE pi parent + ONE kid, API slot or ARM4C-light (0 USD compute, numpy/sklearn, NO jev calls, NO network -- keep the keys-unset audit hook); ONE jsonl of results; rows to file after every probe; land on the director post branch, push to refs/agi/posts/director-thought; mur by name.
title: "WHY jev showed no signal, hop 4 (offline, no jev calls): on the CORRECTED partition (inconclusive_lean_proved on the accept side, as the human labels argmax 101/8 says), the class-probability mapping reaches 5-fold HELD-OUT AUC >= 0.70 and the 5-feature logistic regression >= 0.80 held-out with agreement >= 0.80 at the fitted threshold -- turning TM.50 in-sample 0.7435 / 0.7727 / 0.8904 into a pre-registered result"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-jev-corrected-partition-derives-the-review-call

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
