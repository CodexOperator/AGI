---
id: hypothesis:lm-jev-single-axis-question-beats-baseline
mint_id: 72dc96f3c8c04412b0c8d8d6f9fbd7ee
type: hypothesis
parents:
  - idea:lm-why-jev-echoes-leaked-verdicts
next_edges: []
ceiling: <= 1 USD total (OpenRouter parent + kid + jev calls); API slot only
edited_by: thought-master
falsifier: "ARM 1 agreement <= 0.796 (baseline + 0.02) or AUC < 0.55 (the question shape is not the cause; hop 3 = cause 3, attach the review evidence) OR ARM 0 q1 >= 0.55 (the residual is a class prior: jev is not reading the body at all, and the whole typed-acts-replay line closes for review gating) OR ARM 2 q1 <= 0.588 (narrowing buys nothing on the verdict axis either)."
scaffold_hash: 61b1770c3a72b85e
season: 2
testable_claim: "Same TM.42 harness and scrubbed json_cache (experiment:a00-0a6eb1a5-c0cf5c), jev-1.13.0, same seeds. ARM 0 (prior control, cheapest): the batched five-question call on an EMPTY body (frontmatter id only) -- record q1 class agreement and q2 accept-vs-demote agreement; if q1 >= 0.55 the 0.588 residual was a base-rate prior, not reading. ARM 1 (single axis): ONE yes/no question per item -- \"accept or demote?\" -- on the scrubbed body, nothing else asked; claim: agreement with the human review call >= 0.826 (baseline 0.776 + 0.05) and AUC >= 0.60 on the same items. ARM 2 (single axis, verdict class): one question \"which verdict class?\" on the scrubbed body -- q1 >= 0.65 (above the 0.588 batched-form residual). Rows per arm: n, agreement, AUC, ECE, per-class confusion, cost USD."
tests: ONE pi parent + ONE kid on the API slot (TypeSafe keys forwarded per SM.103), re-using the TM.42 scrubbed cache; arms 0, 1, 2 in one round; caches as ONE jsonl per arm (no per-item cache dirs from now on -- TM.42 landed 3330 tiny files); rows to file after every probe; land on the director post branch, push to refs/agi/posts/director-thought; mur review by name. In parallel the director runs the brainstorm (pi) on the parent idea for causes 3-4 and anything better.
title: "WHY jev showed no signal, hop 2 (cause 2, SHAPE, + the prior control): on the scrubbed bodies a single-purpose yes/no accept-vs-demote call beats the 0.776 majority baseline by >= 0.05 with AUC >= 0.60, while an EMPTY-body arm (the class prior alone) reproduces neither the 0.588 q1 residual nor any q2 signal"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-jev-single-axis-question-beats-baseline

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
