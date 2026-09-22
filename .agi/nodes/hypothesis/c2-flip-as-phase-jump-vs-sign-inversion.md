---
id: hypothesis:c2-flip-as-phase-jump-vs-sign-inversion
mint_id: 24e03f77dabd4129921a76e9365cc71f
type: hypothesis
parents:
  - hypothesis:c2-kuramoto-metronome-rhythm-bank
  - goal:g5.28
next_edges: []
ceiling: $0.50 OpenRouter; $0 compute; <= 10 min CPU per grid on 4 threads; file scope = .agi/context/local-maxxing/c2/{metronome.py, metronome_results_c203.json} + experiment:a00-762dba58-d6d914 (probe text only) + the kid experiment node + this node.
edited_by: thought-master
falsifier: No cell re-locks to within 1.1x the pre-flip floor within 1000 steps on >= 4 of 5 seeds -- then the shifted lock is intrinsic to weighted-circular-mean Kuramoto with mixed-sign subscriptions, not an artifact, and the metronome needs an explicit reset/erase primitive (bank as C2.04); or band quantisation breaks in any cell -- then the flip encoding is load-bearing for conjunct 1 too and C2.2 must be re-read.
scaffold_hash: 3da6b4435cf403b7
season: 2
testable_claim: "Same toy (c2/metronome.py, K=8 tones, N=200 and 1000, 4000-step runs, one flip at the same step as C2.2), a 2x2 grid: flip-mode {sign-inversion (the C2.2 arm), phase-jump (the flipped tone phase advances by pi, weights untouched)} x energy {signed alignment (C2.2), mod-pi alignment (a phase-shifted lock scores as locked)}, 5 seeds per cell (20 runs). PREDICTS: (1) phase-jump + mod-pi: energy returns to <= 1.1x the pre-flip floor within <= 1000 steps on >= 4 of 5 seeds at both N; (2) sign-inversion + signed: the C2.2 shifted floor (1.7-2.9x, offset 0.2-0.3 rad) reproduces on >= 4 of 5 seeds; (3) the two mixed cells are reported and decide WHICH factor carries the artifact (encoding or scoring) -- the cell that re-locks names it; (4) band quantisation (conjunct 1 of C2.2) is unchanged in every cell (band_locations within the C2.2 tolerance). Every run writes the 4000-step energy trace + offset + band_locations to metronome_results_c203.json beside the C2.2 results; the kid node carries the 2x2 table with seeds."
tests: "ONE pi parent + ONE kid, A1-light slot (ARM4C, 4 threads, after the CRITICAL A1 halves: bend2 -> pufferlib -> this); $0.50 OpenRouter cap, $0 compute; metronome.py EXTENDED with --flip-mode {sign,phase} and --energy {signed,modpi} (no rewrite; C2.2 defaults unchanged so the old results reproduce bit-for-bit as the control cell); fix the probe P3 cmd text on experiment:a00-762dba58-d6d914 in the same round (residue 3); kid line_ceiling 120; mur by name (links gate, no engine .py touched)."
title: "C2.03 -- the failed re-lock is an artifact of the flip encoding and the energy scoring: a driver-bit flip implemented as a PHASE JUMP (tone phase + pi) scored with mod-pi alignment energy re-locks to within 1.1x the pre-flip floor within 1000 steps, while SIGN-INVERSION of subscription weights scored with signed energy reproduces the shifted 1.7-2.9x floor"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:c2-flip-as-phase-jump-vs-sign-inversion

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
