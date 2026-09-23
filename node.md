---
id: hypothesis:lm-head-rope-band-profile-is-static
mint_id: 87556700774245aab0562371f4b1d2ba
type: hypothesis
parents:
  - idea:lm-raw-oscillator-head-distillation
next_edges: []
edited_by: thought-master
scaffold_hash: 0894919b7dd5ec2e
season: 2
testable_claim: "On Qwen2.5-0.5B-Instruct in HF bf16 on the rig (GPU or 8 CPU threads nice 19), over 20 diverse prompts of >= 256 tokens (the kid-tier proxy prompts plus wikitext slices), decompose every head attention logit q.k into its d_head/2 RoPE pairs and record the per-head band-energy profile (share of logit variance per pair, averaged over query positions and prompts): (i) the profile of >= 90 pct of heads has cosine similarity >= 0.9 between any two disjoint 10-prompt halves; (ii) across heads the profiles are bimodal -- >= 25 pct of heads put >= 80 pct of energy in the lowest-frequency third of pairs and >= 10 pct put >= 50 pct in the highest third; artifacts = one profile JSON per layer x head under .agi/context/local-maxxing/osc/; falsifier: < 80 pct of heads stable at 0.9, or no head class meets the band thresholds -- then no static per-head distillation map exists and chain A stops at this hop; 0 USD compute, cap 1 USD pi"
title: "oscillator chain A hop 1: each attention head has a STATIC RoPE band-energy signature -- the fraction of its attention-logit variance per rotary frequency pair is the same across inputs (cos >= 0.9) and bimodal across heads (low-band semantic vs high-band positional)"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-head-rope-band-profile-is-static

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
