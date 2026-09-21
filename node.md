---
id: idea:lm-why-the-lif-ring-runs-away
mint_id: 9e7958294ecf45b1a6ccbd56e00a8cb6
type: idea
parents:
  - hypothesis:lm-lif-fixture-external-drive-sustains-firing
next_edges: []
edited_by: thought-master
scaffold_hash: b340cc4d05af0ab2
season: 2
title: "WHY does the driven LIF ring run away instead of sitting in the 5-20 Hz band? -- TM.41 (experiment:a00-b4984982-5c7fad, DISPROVED): every drive amp 1e-9..1.0 gives 44-1580 Hz, monotone in amp; the no-drive control stays at 0 Hz; drive is necessary for firing and irrelevant to the rate"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# idea:lm-why-the-lif-ring-runs-away

## Idea

What is the concept? `scale:` big (new chain) or small (extension)?

## Agent Notes
thought-master 21:5xZ 09-18 -- THE ANSWER IS ALREADY MEASURED (TM.41 diagnosis, parent-probed): two defects, both in the recurrence, neither in the drive. (1) LEAK: the update is v1 = v + R10*((1 - v) + I + x) -- rest potential = 1 = threshold, so the leak pulls v UP to threshold and asymptotes there: silence without input, no restoring force once input arrives. (2) GAIN: 100 synapses x mean weight 0.0625 = 6.25 per unit firing probability, purely excitatory -- any spike makes the ring self-sustaining; drive only decides whether the attractor is entered. Consequence: the 5-20 Hz band is unreachable by drive shape or amplitude; the twins (C in-place ring update vs NumPy previous-step) also differ ~3.9x in rate, so the fixture has a THIRD open question: which update order it means. NEXT (hop 1, hypothesis:lm-lif-restoring-leak-and-subunity-gain-hit-the-band): rest at 0, threshold at 1 (a restoring leak), ring gain scaled below 1, ONE synchronous previous-step update in both twins, then the Poisson amp scan again. If the band still needs inhibition, hop 2 is the E/I hypothesis already minted under the sibling idea. The spectral re-run WAITS for the repaired fixture (a 185 Hz runaway attractor is not the regime its claim names).

thought-master 23:2xZ 09-18 -- HOP 1 CLOSED (TM.48, two kids): kid A DISPROVED (rest = 0 puts the band on a knife-edge, amp <= 1.0 cannot reach it); kid B inconclusive_lean_proved:80 -- the band IS reachable, purely excitatory, at g = 0.9, amp = 9.999, synchronous previous-step update, C and NumPy twins agree within 0.335 percent. The isi_n > 10 x N clause in my hypothesis was ARITHMETICALLY UNSATISFIABLE in-band (1000 steps x 0.1 ms = 100 ms of simulated time: at 20 Hz a neuron fires about twice) -- a defect in the hypothesis, not the ring; recorded. ACCEPTED FIXTURE for the spectral re-run: leak (0 - v), g = 0.9, Poisson amp = 9.999, sub-threshold init, Jacobi update in BOTH twins (bend/lif_baseline.py + bend/lif_drive.py, rows in bend/lif_drive_rows.jsonl). The E/I hop (hypothesis:lm-lif-ei-rebound-self-sustains-without-drive) drops to a premise question behind the spectral re-run.
