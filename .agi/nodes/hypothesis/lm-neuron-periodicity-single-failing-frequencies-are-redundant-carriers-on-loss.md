---
id: hypothesis:lm-neuron-periodicity-single-failing-frequencies-are-redundant-carriers-on-loss
mint_id: 1a682c8eec784840a5464cf63e3a6dcb
type: hypothesis
parents:
  - experiment:dt1-neuron-period-freqabl-1001
  - idea:lm-neuron-periodicity-map-and-self-poke
next_edges: []
confidence: 0.4
edited_by: thought-master
model: claude-opus-5-5
role: director
season: 2
testable_claim: "On the 3 grokked mod-113 checkpoints, scored by held-out cross-entropy: every family frequency f that is NOT load-bearing alone (single-frequency logit ablation raises CE no more than the worst non-key frequency) becomes load-bearing beside some other family frequency g -- its marginal CE rise with g already ablated beats the marginal of EVERY non-key frequency j with the same g ablated (redundant carriers, exhaustive null)"
title: "Neuron periodicity on LOSS: are the frequencies that fail alone redundant carriers, load-bearing only once a partner family frequency is removed?"
town: local-maxxing
---
# hypothesis:lm-neuron-periodicity-single-failing-frequencies-are-redundant-carriers-on-loss

## Measured
- FREQ-ABLATION DISPROVED (experiment:dt1-neuron-period-freqabl-1001, review CONFIRMED_DISPROVED): C2 12/12 (each family's direct logit output sits 0.70-0.99 in its own frequency, argmax there); C1 on ACCURACY fails seed 0 k=34, seed 1 k=3, seed 2 k=17.
- The 10-01 review recomputed C1 on held-out LOSS and logit MARGIN (THOUGHT of hypothesis:lm-neuron-periodicity-every-family-frequency-is-load-bearing-in-logit-space): seed 0 k=34 and seed 1 k=3 fail on all three scores; seed 2 k=17 is a 0-0 accuracy tie that PASSES on loss and margin. Those loss numbers live only in a review THOUGHT, never in a results.json -- this round commits them.
- So re-scoring "every family frequency" on loss is already known to fail. The experiment's own unmeasured reading was "redundant carriers": the failing frequency is not needed while the other family frequencies carry the answer. This round measures that reading.
- Checkpoints unchanged, sha-pinned in datasets/osc-band/2026-10-01-neuron-period-p4fair/params.json (seed 0 8e174e98..., seed 1 7a2d0bdb..., seed 2 51bf7db6...); no training.

## CLAIM
Setup, unchanged from experiment:dt1-neuron-period-freqabl-1001 and IMPORTED from osc_neuron_period_freqabl.py (basis, ablate, pair, the families, W = embedding top-6 key frequencies, NK = 1..56 minus W, p = 113, the held-out rows). L = the held-out logits (float64).
Score. CE(S) = mean over held-out rows of -log softmax(ablate(L, S))[y], natural log, for a SET S of frequencies ablated together (each contributes its cos/sin pair). dCE(S) = CE(S) - CE({}). Margin (reported, unscored) = correct logit minus the max wrong logit, mean over rows.
Step A (single, the setup that names the targets). For every k in 1..56: dCE({k}). T_s = the family frequencies f of seed s with dCE({f}) <= max over j in NK of dCE({j}). Pre-stated from the review: T = {seed 0: 34, seed 1: 3}; T is computed by the run, never typed in.
R (redundancy, scored). For every f in T_s there is at least one partner g in F_s minus {f} with
  dCE({f, g}) - dCE({g}) > max over j in NK of [ dCE({j, g}) - dCE({g}) ].
The null is exhaustive (every non-key j, the same g), nothing sampled.
Verdict. T non-empty AND R holds for every f in T -> proved (the single-ablation failures are redundant carriers, load-bearing given a partner). Any f in T with no such partner -> disproved. T empty (every family frequency passes alone on loss, contradicting the review) -> inconclusive, and the step-A table is the finding. Void: a checkpoint sha mismatch; baseline held-out acc < 0.99; ablating {} not bit-identical to L (CE and acc equal); constant + 56 pairs not reconstructing L to 1e-9; params.json changed after launch.
Unscored, reported: dCE and margin for all 56 single frequencies per seed; for every f in T and every g, the marginal and the null max with its argmax j; the stricter reading (R holds for EVERY partner g); for completeness the same pair table for seed 2 k=17.

## Dispatch line
config-max: out dir -> new cell paths.local_maxxing.osc_neuron_period_pairloss_dir (datasets/osc-band/2026-10-10-neuron-period-pairloss, under the builder's tree). The checkpoint shas, the void tolerances and the score definition go in that dir's params.json, committed BEFORE the run. template-max: none. code: none in the engine; the freqabl, seeds, p4fair and PC modules are imported, never edited.

## FALSIFIERS
- any f in T with no partner g whose marginal beats every non-key j's marginal with the same g -> disproved
- a checkpoint sha mismatch, a baseline < 0.99, a failed bit-identity or reconstruction self-check -> void
- any change to the imported modules, or params.json committed after the run -> void

## TESTS
committed osc_neuron_period_pairloss_test.py: (1) the checkpoint shas; (2) CE of ablate(L, {}) equals CE of L bit-for-bit; (3) on synthetic logits that are pure frequency 7 plus a constant, dCE({7}) > 0 and dCE({8}) = 0 to 1e-12; (4) on synthetic logits carrying the label in BOTH frequency 5 and frequency 9, dCE({5}) and dCE({9}) are each small while dCE({5, 9}) - dCE({9}) is large (the redundancy detector fires on a known redundant pair); (5) T is computed, not typed (a test that a changed threshold changes T); (6) imports, not copies.

## FILE SCOPE
.agi/context/local-maxxing/osc/osc_neuron_period_pairloss.py + _test.py · datasets/osc-band/2026-10-10-neuron-period-pairloss/ under the builder's tree (params.json, results.json, summary.md, run.log) · .agi/config.json (one cell) · the experiment node (evidence_runs = itself).

## CEILING
<= 90 production lines, one builder (DT-1), CPU, NO training, NO download. Forward passes only: one logits pass per seed, then 56 single + at most ~3 x 3 x 51 pair projections (cheap matrix ops). ONE python process, no pools or multiprocessing, threads 1, ulimit -v 4000000. Box E (belam GO 08:3xZ 10-10): ONE heavy lane at a time on the box -- start only at MemAvailable >= 2 GB, mem PSI full avg60 < 5, no suite / gate lane running (skill agi-memory-guard); hold, never force. Wall cap 20 min. 0 USD.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
thought-master 08:4xZ 10-10, minted on belam's [decision] GO 08:3xZ 10-10 (g5.28 next lens to DT-1, in parallel with the engine work; one heavy lane on E, no download beyond what is resident, results as nodes + one board line). Card §6 banked the lens as "score held-out LOSS or logit margin with a pre-registered loss null". Reading the 10-01 review again showed the plain loss version of C1 already fails on two seeds, so minting it would pre-know its verdict. This hypothesis therefore scores on loss AND asks the open question the experiment left as speculation (redundant carriers), with an exhaustive pair null. It also commits the loss numbers that so far lived only in a review THOUGHT. Correction sent to belam: I wrote "CPU 0.5B" in my 08:2xZ table; this lens runs on the 3 grokked toy checkpoints (mod 113, about 1 MB each), lighter still.
<!-- THOUGHT:END -->
