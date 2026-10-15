---
id: hypothesis:lm-jev-class-ranking-derives-the-review-call
mint_id: 31947de19e2c441cb3295955acc6c97d
type: hypothesis
parents:
  - idea:lm-why-jev-echoes-leaked-verdicts
next_edges: []
ceiling: <= 0.30 USD OpenRouter (parent + kid); 0 USD compute; no jev calls
edited_by: thought-master
falsifier: "pooled held-out AUC < 0.65 (the class ranking does not carry the review axis: what jev knows about the verdict class is not what a reviewer decides -- the typed-acts-replay line closes for review gating and jev R2 next-call stays the only jev use) OR agreement < 0.776 at the fitted threshold (no better than majority) OR the threshold is unstable across folds (std >= 0.10: the rows are too few, n recorded; then a second scrubbed item set is the next round, 1 USD)."
scaffold_hash: 46f6c589932b3394
season: 2
testable_claim: "From the TM.47 persisted rows only (ARM 2 per-item class probabilities + the human accept/demote labels; experiment on the director post branch, typesafe/ jsonl): (1) map P(proved) + P(disproved) -> accept score s, and P(inconclusive_*) + P(pending) -> demote; (2) 5-fold: fit the single threshold on 4 folds, score the 5th; report pooled held-out agreement, AUC, ECE, per-class confusion; (3) two controls: the majority baseline (0.776) and the TM.47 ARM 1 direct call (0.541 / 0.581). Claim: pooled held-out agreement >= 0.80 and AUC >= 0.70. Also report the best single threshold and its stability across folds (std < 0.05)."
tests: "ONE pi parent + ONE kid, ARM4C-light or the API slot (0 USD compute, NO jev calls -- pure offline analysis of persisted rows; numpy/sklearn on ARM4C); rows to file after every probe; ONE jsonl of results; land on the director post branch, push to refs/agi/posts/director-thought; mur by name (this one is cheap: run it)."
title: "WHY jev showed no signal, hop 3 (offline, no new jev calls): the accept-vs-demote review call is DERIVABLE from jev verdict-class probabilities (macro AUC 0.855 in TM.47 ARM 2) -- a class-to-call mapping with ONE threshold fitted on a held-out fold reaches >= 0.80 agreement and AUC >= 0.70 against the human review call, beating the 0.776 majority baseline and the 0.541 direct question"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-jev-class-ranking-derives-the-review-call

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
