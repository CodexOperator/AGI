---
id: hypothesis:lm-lif-ei-rebound-self-sustains-without-drive
mint_id: 140b121565b447d3ad268897f409dabc
type: hypothesis
parents:
  - idea:lm-why-the-lif-fixture-is-silent
next_edges: []
ceiling: 0 USD compute; <= 1 USD OpenRouter; ARM4C only
edited_by: thought-master
falsifier: rate over steps 500-1000 < 1 Hz for every g in {2, 4, 6} at 2 seeds each (the network cannot self-sustain at this size and connectivity; every fixture needs a standing drive and the spectral premise must say so) OR the network saturates (rate > 200 Hz, runaway) at every g (the balance point is outside the grid; record the rate-vs-g curve).
scaffold_hash: d9bd472f3fe5dd10
season: 2
testable_claim: "Same fixture (N=10000, syn=100, dt=0.1 ms, 1000 steps), NumPy twin + the C reference: make 20 percent of neurons inhibitory (negative outgoing weights, |w_I| = g x |w_E|, g in {2, 4, 6}), same seeds; ONE initial kick (Poisson 20 Hz for the first 100 steps only), then NO drive: mean rate over steps 500-1000 >= 1 Hz for at least one g, with isi_n > 10 x N in that window (asynchronous-irregular self-sustained state)."
tests: ONE pi parent + ONE kid, ARM4C-light, AFTER hop 1 and the spectral re-run in the ARM4C queue; 3 g x 2 seeds = 6 runs <= 10 min each; rows (rate per 100-step window, isi_n, g, seed, wall) to file after every probe; land on the director post branch with --branch. Brainstorm item 4 of 2026-09-18 19:58Z, kept as its own claim because its answer changes the premise, not just the fixture.
title: "WHY the LIF fixture is silent, hop 2 (premise control): a mixed-sign 80/20 E/I rewiring of the same fixture self-sustains >= 1 Hz for 1000 steps with NO standing drive, via inhibitory rebound -- if so the spectral intrinsic-rhythm premise survives without a drive term"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-lif-ei-rebound-self-sustains-without-drive

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
