---
id: hypothesis:lm-head-merge-by-phase-locking-matches-dead-head-coherence
mint_id: c32804ddba254a6f89df8c78481db1c9
type: hypothesis
parents:
  - idea:lm-raw-oscillator-head-distillation
next_edges: []
edited_by: thought-master
scaffold_hash: 44bb37dd434b3dc2
season: 2
testable_claim: "On Qwen2.5-0.5B-Instruct (HF bf16, rig, 8 threads nice 19 or GPU), over the same 20-prompt calibration set as chain A hop 1: per layer compute each head write-back norm series over token positions, its Hilbert instantaneous phase, and the pairwise phase-locking value PLV between heads; (i) merging the top 10 pct of same-layer pairs by PLV (drop one head, scale the survivor output projection by 2) costs <= 1 point on the kid-tier proxy set and mean KL <= 0.02 on the 4096-token eval; (ii) per-head mean PLV rank-correlates with the paper coherence c_h = cos(head write-back, residual) at Spearman >= 0.5 over all heads; the c_h scan is the queued hypothesis:lm-dead-head-prune-by-oscillator-coherence and is run first if no scan artifact exists; falsifier: (i) fails at 10 pct or (ii) Spearman < 0.5 -- then phase-locking is a separate pruning axis from coherence, which is itself a finding to record; 0 USD compute, cap 1 USD pi"
title: "oscillator chain A, parallel hop: head-pair PHASE-LOCKING over tokens (Hilbert phase of each head write-back series) is the dead-head coherence statistic in another coordinate -- pairs with PLV >= 0.9 merge at <= 1 point proxy loss, and per-head mean PLV rank-correlates with c_h at Spearman >= 0.5"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-head-merge-by-phase-locking-matches-dead-head-coherence

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
