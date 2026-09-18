---
id: hypothesis:lm-jev-surface-lexical-beats-jev
mint_id: 8bbbb70cbedb4ee78ac77afaa295ee63
type: hypothesis
parents:
  - idea:lm-why-jev-echoes-leaked-verdicts
  - goal:g14
next_edges: []
ceiling: <= 1 USD OpenRouter (parent+kid); 0 API calls; 0 compute; no downloads on ARM4C without an owner yes; runs <= 10 min
edited_by: brainstorm
falsifier: Held-out TF-IDF mean accuracy is at or below jev scrubbed q1 agreement (0.60) -- then the residual is not surface-lexical and jev reads something a bag of words cannot; OR the TF-IDF advantage vanishes when node kind is removed from the text (the gain is only the kind prior, which H3 already covers).
scaffold_hash: d9880a60c947b53f
season: 2
testable_claim: "On the TM.42 scrubbed bodies (scrub regex applied identically), train a TF-IDF word 1-2 gram + logistic regression with class_weight balanced, 5-fold stratified CV by act id, seed 20260918. Measured preliminary: 0.661 mean held-out accuracy (folds 0.689/0.635/0.676/0.662/0.644), above jev scrubbed q1 0.588 to 0.596 and above the body-blind kind-prior 0.615. Claim: the held-out TF-IDF accuracy exceeds jev scrubbed q1 agreement by >= 0.04, so whatever above-chance signal survives the scrub is readable from lexical surface alone (hedge words, length, evidence-marker vocabulary), not from jev semantic review. Report mean and per-fold accuracy, the top weighted n-grams per class, and the paired per-act win/loss against jev."
tests: ONE pi parent + ONE kid, ARM4C-light slot (scikit-learn 1.8 + NumPy, CPU, no network, no downloads); steps (1) rebuild scrubbed bodies with the acts_replay_scrub.scrub regex and labels from acts_replay_scrub.jsonl; (2) 5-fold stratified CV by act id with a pinned seed, record mean and per-fold accuracy, and a per-act win/loss against jev; (3) ablate node-kind tokens and re-run to test the falsifier second clause; rows to bench/<utc>.jsonl, kid persists rows after every probe, parent commits promptly, FILE SCOPE .agi/context/local-maxxing/typesafe/, anonymization rule (hosts/IPs/GPU models/locations/key ids never; aliases ARM4C GPU2070S CPU8G EDGE), kid line_ceiling 120
title: "WHY jev echoes, hop 6 (anything better, SURFACE): the residual signal is lexical surface, not semantics -- a word-level TF-IDF + logistic regression on the SAME scrubbed bodies scores 0.661 in 5-fold CV, beating jev scrubbed 0.588"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-jev-surface-lexical-beats-jev

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
