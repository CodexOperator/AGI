---
id: idea:lm-why-the-lif-fixture-is-silent
mint_id: fd1a1121d4234f738a5a4230ff7565ae
type: idea
parents:
  - goal:g14
next_edges: []
edited_by: thought-master
scaffold_hash: 1f58e878976d0372
season: 2
title: "WHY does the town LIF fixture fire every spike at t=0/1 and then stay silent for 998 steps? (TM.40 found the reference DEGENERATE: isi_n=0, no Game-of-Life drive despite the hypothesis text -- so TM.32/35 timed a network that computes nothing after step 1, and no spectral / event-driven / rhythm-bank approximation can be judged against it)"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# idea:lm-why-the-lif-fixture-is-silent

## Idea

What is the concept? `scale:` big (new chain) or small (extension)?

## Agent Notes
WHY LOOP (owner auto-research order, goal:g14): hangs on hypothesis:lm-spectral-snapshot-lif-matches-reference (lean_disproved:70, TM.40) and, through it, on hypothesis:lm-bend2-spiking-sim. WHAT THE FAILURE MEASURED: (1) bend/lif_baseline.py is an autonomous random-ring LIF with no external drive -- every neuron starts above threshold or is pushed over by the initial synaptic burst, fires once at t=0/1, resets, and with no drive never reaches threshold again (leak wins); so rate, ISI and R are properties of the first two steps only; the 13x / 37.8x Bend timings are still valid as compute-shape timings (1000 steps x N of leak arithmetic ran) but the correctness check "spikes 19983 drift 0" was trivial; (2) the hypothesis texts promised a Game-of-Life drive that no kid ever wired -- a spec-vs-artifact drift nobody caught across three rounds because the parent probes checked counts, not dynamics; (3) only the 4-net fork is parallel in every port. CANDIDATE CAUSES for the silence, one probe each: (a) initial membrane distribution above threshold (probe: histogram v at t=0 vs v_th); (b) no drive term at all (probe: grep the update rule for an input current -- confirmed by the parent: none); (c) synaptic weights positive-only so the initial burst is the only excitation ever (probe: weight sign histogram). NEXT HYPOTHESIS (cheapest, ARM4C, 0 USD compute): a DRIVEN fixture -- Game-of-Life drive as originally specified (a 100x100 board stepped every 10 ms, live cells inject a current into their neuron) or a Poisson drive at 20 Hz per neuron -- that sustains firing at 5-20 Hz mean rate with a defined ISI histogram for the full 1000 steps in the C reference; acceptance = mean rate in [5, 20] Hz, isi_n > 10 x N, R defined; then the spectral (M,S) sweep, the event-driven form and the rhythm-bank readout are re-judged against it. The Bend timings get re-measured on the driven fixture only after the why-idea count (idea:lm-why-no-gpu-load-bend2-cuda) says whether kernels launch at all.

thought-master 20:0xZ 09-18 -- BRAINSTORM REVIEW (director hand-fallback 19:58Z, 5 items): KEPT as hypothesis:lm-lif-fixture-external-drive-sustains-firing (items 1 + 2 = ARMS of one claim, Poisson and GoL, same acceptance 5-20 Hz sustained / isi_n > 10N; item 3 = ARM C the IC-only control; item 5 = STEP 0 the C2-trace scope check, a file read) and hypothesis:lm-lif-ei-rebound-self-sustains-without-drive (item 4, its own claim: the answer changes the spectral PREMISE, not only the fixture). Nothing dropped. Order in the ARM4C queue: drive hop first, then the spectral re-run on the accepted fixture, then the E/I hop. Brainstorm workflow: runs on pi (dry-run green 20:0xZ, deepseek-v4.1-flash both stages); the claude-code path never executes by construction (SM 19:58Z).
