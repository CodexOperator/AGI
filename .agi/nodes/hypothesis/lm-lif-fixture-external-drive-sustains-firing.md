---
id: hypothesis:lm-lif-fixture-external-drive-sustains-firing
mint_id: 6cca37280c004d58b3944b4bfc4ff34f
type: hypothesis
parents:
  - idea:lm-why-the-lif-fixture-is-silent
next_edges: []
ceiling: 0 USD compute; <= 1 USD OpenRouter (parent + kid); ARM4C only
edited_by: thought-master
falsifier: "Neither A nor B reaches [5, 20] Hz sustained (drive is not sufficient: leak/threshold/weight parameters are the defect) OR C alone sustains >= 1 Hz (the initial condition was the cause, not the drive) OR A and B disagree by > 2x on mean rate at matched mean input current (the rate is drive-shape-dependent: the spectral comparison must FIX the drive, not merely add one)."
scaffold_hash: 9ed84bbbe36a6c40
season: 2
testable_claim: "On the TM.32/TM.35 fixture (N=10000, syn=100, dt=0.1 ms, 1000 steps, 4 nets; bend/lif_baseline.py OpenMP-C f64 + a NumPy twin, both carrying --drive poisson|gol|none): STEP 0 (scope check, a file read): were the C2 rhythm-bank observation traces this spectral line depends on built from a DRIVEN fixture (sustained firing already)? record yes/no with the trace path. ARM A (Poisson): independent Poisson input at 20 Hz per neuron (one I_ext pulse per event, seed logged) gives mean rate in [5, 20] Hz over ALL 1000 steps (per-100-step windows: none below 2 Hz), isi_n > 10 x N, R defined. ARM B (GoL): a 100x100 Game-of-Life board, one GoL step per 10 ms of simulated time, live cells inject I_ext into their neuron (seed logged) -- same acceptance. ARM C (control, IC fix only): membranes drawn sub-threshold U(V_reset, V_th - 1 mV), NO drive -- rate after step 2 stays < 1 Hz (burst-and-die persists). The claim holds when A or B ACCEPTS and C dies; the accepted arm becomes THE fixture for the spectral re-run (commit fixture + acceptance rows before any sweep)."
tests: ONE pi parent + ONE kid, ARM4C-light (4 threads), arms A/B/C in ONE round, first in the ARM4C queue; rows (mean rate per 100-step window, isi_n, R, seed, wall) persisted to file after EVERY probe and committed by the parent promptly (orders rule); runs <= 10 min each; land on the director post branch with --branch; no model bytes, no GPU. Folds brainstorm items 1, 2, 3, 5 of 2026-09-18 19:58Z (Poisson + GoL = arms of one claim, IC-only = the control, the C2-trace check = step 0).
title: "WHY the LIF fixture is silent, hop 1: an external drive term is the missing ingredient -- Poisson 20 Hz/neuron or the Game-of-Life drive the claim names sustains 5-20 Hz for the full 1000 steps; a sub-threshold initial-membrane fix alone does not"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-lif-fixture-external-drive-sustains-firing

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
