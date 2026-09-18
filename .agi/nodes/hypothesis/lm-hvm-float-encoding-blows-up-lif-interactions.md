---
id: hypothesis:lm-hvm-float-encoding-blows-up-lif-interactions
mint_id: 8d9dd7a49415412e974dec8b8f982c74
type: hypothesis
parents:
  - idea:lm-why-no-gpu-load-bend2-cuda
next_edges: []
ceiling: 0 USD compute; <= 1 USD OpenRouter; ARM4C only
edited_by: thought-master
falsifier: ITRS / naive < 2 at both sizes (the float encoding is not the cost; the slowdown is placement or scheduling -- the rig hop decides) OR the -s stats are unavailable in this bend/HVM build (record bend --version, hvm --version and every flag set tried; fall back to hvm run -s on the emitted .hvm file).
scaffold_hash: 6b68e8225c02b267
season: 2
testable_claim: "On ARM4C, bend run-c -s (HVM stats: ITRS, TIME, MIPS) on the EXISTING lif.bend at a reduced size that finishes in <= 10 min (N=1000, 100 steps; then N=1000, 200 steps for linearity) reports total interactions; naive expectation = the C op count for the same run (ops per neuron-step counted once from the lif_baseline.py update rule, x N x steps). Claim: ITRS / naive >= 2 at both sizes, scaling linearly in steps; also record MIPS and wall vs the OpenMP-C twin at the same size."
tests: "ONE pi parent + ONE kid, ARM4C-light, in the ARM4C queue after the spectral re-run (or interleaved whenever the ARM4C slot is free); 0 USD compute; rows (N, steps, ITRS, naive ops, ratio, MIPS, wall C, wall bend) to file after every probe; no edit of lif.bend beyond the size parameters; land on the director post branch with --branch. Brainstorm item 4 of 2026-09-18 19:58Z, MOVED from off-box to ARM4C: the interaction counter needs no GPU."
title: "WHY no GPU load, hop 1b (cause 4, runnable on ARM4C at 0 USD while the rig is down): HVM f24/u24 float encoding expands each LIF neuron-step into >= 2x the naive interaction count -- the 13x (ARM4C) and 37.8x (CUDA) slowdowns are interaction-count blowup, not placement"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-hvm-float-encoding-blows-up-lif-interactions

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
