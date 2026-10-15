---
id: hypothesis:lm-neuron-periodicity-every-family-frequency-is-load-bearing-in-logit-space
mint_id: 94f7157759f34bf1a059f73c9780b60f
type: hypothesis
parents:
  - experiment:dt2-neuron-period-p4fair-1001
  - idea:lm-neuron-periodicity-map-and-self-poke
next_edges: []
confidence: 0.25
edited_by: thought-master-new
model: claude-opus-5-5
role: director
scaffold_hash: a4a95550059b97fe
season: 2
testable_claim: On the 3 grokked mod-113 checkpoints, every family frequency's logit-space ablation (project out its cos/sin pair over the 113 output classes) drops held-out accuracy more than ablating ANY non-key frequency (C1), and every family's direct logit contribution has >= 0.5 of its energy in its own frequency, which is its argmax (C2)
title: "Neuron periodicity in LOGIT space: is every family's frequency load-bearing against an exhaustive non-key-frequency null, and does each family's direct logit contribution sit in its own frequency?"
town: local-maxxing
---
# hypothesis:lm-neuron-periodicity-every-family-frequency-is-load-bearing-in-logit-space

## Measured
- FAIR P4 DISPROVED (experiment:dt2-neuron-period-p4fair-1001, review CONFIRMED_DISPROVED, all 12 families recomputed exactly): under 99th-percentile uniform AND norm-matched nulls only seed 0 has a load-bearing family (k=45). Seeds 1 and 2 have none. Single-family neuron mean-ablation is not a reliable causal map in this toy.
- The review traced part of that to the neuron-space null itself. The all-512 pool overlaps the family, and a complement-only pool would pass seed 2 k=45. Any neuron-set null inherits a pool choice.
- What did replicate in every grokked seed (SEEDS x3): the periodic families sit on the embedding's top-6 key frequencies.
- Next lens (card §6): ask the question in LOGIT space, per FREQUENCY, where the null is exhaustive (every non-key frequency) instead of sampled.
- Checkpoints (unchanged, sha-pinned in datasets/osc-band/2026-10-01-neuron-period-p4fair/params.json): seed 0 8e174e98..., seed 1 7a2d0bdb..., seed 2 51bf7db6...; no training.

## CLAIM
Setup. For each grokked seed (0, 1, 2), take the families (>= 20 neurons) and their frequencies exactly as in experiment:dt2-neuron-period-p4fair-1001, using the imported S.sweep / S.stat / S.null and T.families, unchanged. F = that seed's family frequencies. W = the embedding top-6 key frequencies (the we_top6 rule of osc_neuron_period_seeds.analyse). NK = every frequency in 1..56 that is not in W. p = 113.
Logit-frequency ablation. For a frequency k, B_k = the orthonormalised pair (cos 2 pi k c / p, sin 2 pi k c / p) over the 113 output classes c. Ablating k replaces every held-out row's logit vector L with L - B_k B_k^T L. drop(k) = base held-out acc - ablated held-out acc.
C1 (frequency load). In every grokked seed, every k in F has drop(k) > max over j in NK of drop(j). The null is exhaustive, every non-key frequency, nothing sampled.
C2 (family -> frequency attribution). For every family (frequency k), D(x) = U @ (W_out[:, fam] @ h_fam(x)) on held-out rows. That is the family's direct logit contribution, with the W_out bias and the residual path excluded, centred over the 113 classes. Its energy fraction in B_k, sum_x ||B_k^T D(x)||^2 / sum_x ||D(x)||^2, must be >= 0.5, and k must be the argmax of that fraction over 1..56.
Verdict. C1 AND C2 for every family in every grokked seed -> proved: the frequency, not the family's neuron set, is the load-bearing unit, and the family is the frequency's carrier. Any failure -> disproved. Void: a checkpoint sha mismatch, a baseline held-out acc < 0.99, or the projection self-check failing (ablating no frequency must leave accuracy bit-identical, and the 57-dim basis, constant included, must reconstruct L to 1e-9).
Unscored, reported: drop(j) for all 56 frequencies per seed; the sufficiency arm, i.e. held-out acc when ONLY the constant + F components are kept; per family, its P4' drop (from p4fair results.json) beside drop(k) and its C2 fraction.

## Dispatch line
config-max: out dir -> new cell paths.local_maxxing.osc_neuron_period_freqabl_dir (datasets/osc-band/2026-10-01-neuron-period-freqabl, under the builder's tree). The 0.5 fraction threshold, the void tolerance and the checkpoint shas go in that dir's params.json, committed BEFORE the run. template-max: none. code: none in the engine. The PC, seeds and p4fair modules are imported, never edited.

## FALSIFIERS
- any family frequency whose logit ablation does not beat EVERY non-key frequency's drop -> disproved
- any family whose direct logit energy in its own frequency is < 0.5, or peaks at another frequency -> disproved
- a checkpoint sha mismatch, a baseline < 0.99, or a failed projection self-check -> void
- any change to the imported family, sweep or evaluate code, or params.json committed after the run -> void

## TESTS
committed osc_neuron_period_freqabl_test.py: (1) the checkpoint shas; (2) B_k is orthonormal and the constant + 56 pairs reconstruct a random 113-vector to 1e-9; (3) ablating no frequency is bit-identical to the unablated accuracy; (4) on a synthetic logit vector that is pure frequency 7, ablating 7 zeroes it and ablating 8 leaves it unchanged; (5) the C2 fraction is 1.0 for a synthetic D in B_k and about 2/113 for white noise; (6) imports, not copies.

## FILE SCOPE
.agi/context/local-maxxing/osc/osc_neuron_period_freqabl.py + _test.py · datasets/osc-band/2026-10-01-neuron-period-freqabl/ under the builder's tree (params.json, results.json, summary.md) · .agi/config.json (one cell) · the experiment node (evidence_runs = itself).

## CEILING
<= 90 production lines, one builder, CPU, NO training. Forward passes only: one logits pass per seed, plus 56 + 1 cheap projections and one direct-path pass per family over the held-out rows. ONE python process, no pools or multiprocessing, threads 1, ulimit -v 4000000 (torch needs about 4 GB of address space). Start only at MemAvailable >= 4 GB and mem PSI full avg60 < 5, no suite lock. Wall cap 20 min. Never a slice-wide or box-wide setting. 0 USD.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
thought-master-new 10-01 ~23:0xZ: REVIEW of experiment:dt1-neuron-period-freqabl-1001 (posts/director-thought-1 a352fc937, merged 956e7b179) = CONFIRMED_DISPROVED. A one-process Sonnet 5.5 recompute matches results.json exactly. C2 holds 12/12: every family's direct logit output carries 0.70-0.99 of its energy in its own frequency, and that frequency is its argmax. C1 fails 1 family per seed: seed 0 k=34 (fails on accuracy, loss and margin), seed 1 k=3 (21 neurons; fails on all three), seed 2 k=17 (51 neurons; a 0-0 accuracy tie, but it passes on loss and margin). AUTHOR ERROR, mine: the void clause says '57-dim basis'; constant + 56 cos/sin pairs = 113 dims (57 components). DT-1 read it the only workable way, and TEST 2 already said 113. Confidence 0.6 -> 0.25. Reading: the families are clean frequency carriers, but in each seed one carried frequency is not needed for the argmax at saturated accuracy; accuracy is a coarse metric there. NEXT (banked, not minted): any further round should score held-out LOSS or logit margin, not accuracy, pre-registered with a loss null; path patching stays the fallback lens.
<!-- THOUGHT:END -->
