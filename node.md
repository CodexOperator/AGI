---
id: hypothesis:lm-band-pruned-heads-keep-next-token-agreement
mint_id: ee9e250ab2854c9886d09404d2e05ae9
type: hypothesis
parents:
  - hypothesis:lm-head-rope-band-profile-is-static
next_edges: []
edited_by: thought-master
scaffold_hash: a3c032315d23907c
season: 2
testable_claim: "With the hop-1 profiles on Qwen2.5-0.5B-Instruct (HF bf16, rig), per head keep the smallest set of RoPE pairs carrying 95 pct of its logit energy and zero the remaining pairs in q and k (a per-head mask, no retraining); over a held-out 4096-token eval (prompts disjoint from hop 1): top-1 next-token agreement with the unmasked model >= 98 pct and mean per-token KL <= 0.02, at a mean dropped-pair fraction >= 40 pct; report the agreement-vs-dropped-fraction curve at 90/95/99 pct energy; falsifier: at >= 40 pct dropped, agreement < 98 pct or KL > 0.02 -- then report the largest fraction at which both hold (a smaller distillation, not a disproof of hop 1); 0 USD compute, cap 1 USD pi"
title: "oscillator chain A hop 2: keeping only the RoPE pairs that carry 95 pct of each head logit energy (zeroing the rest in q and k) drops >= 40 pct of pairs on average while next-token top-1 agreement stays >= 98 pct and mean KL <= 0.02 against the full model"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-band-pruned-heads-keep-next-token-agreement

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
