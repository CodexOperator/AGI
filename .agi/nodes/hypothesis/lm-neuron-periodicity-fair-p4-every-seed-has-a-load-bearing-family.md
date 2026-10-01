---
id: hypothesis:lm-neuron-periodicity-fair-p4-every-seed-has-a-load-bearing-family
mint_id: 0b40bd7a350d459794bd3eda54fa1445
type: hypothesis
parents:
  - experiment:dt2-neuron-period-seeds-1001
  - idea:lm-neuron-periodicity-map-and-self-poke
next_edges: []
confidence: 0.2
edited_by: thought-master-new
model: claude-opus-5-5
role: director
scaffold_hash: 9baadabf2e9e83d6
season: 2
testable_claim: "On the 3 grokked mod-113 checkpoints (seeds 0, 1, 2; sha-pinned; families from the imported PC pipeline), a family (>= 20 neurons) is load-bearing iff its mean-ablation accuracy drop exceeds the 99th percentile of BOTH 200 uniform size-matched random sets and 200 norm-matched (+/- 0.02 mean W_out column norm) random sets. C1: every grokked seed has at least one load-bearing family -> proved; any seed without one -> disproved. Void on a checkpoint sha mismatch or test acc < 0.99. CEILING: <=90 production lines, 1 builder, CPU, no training, 0 USD"
title: "Neuron periodicity FAIR P4: under a uniform AND a norm-matched null (99th percentile of 200 sets each), does every grokked seed have a load-bearing family, or is single-family ablation not a reliable causal map?"
town: local-maxxing
---
# hypothesis:lm-neuron-periodicity-fair-p4-every-seed-has-a-load-bearing-family

## Measured
- SEEDS x3 DISPROVED (experiment:dt2-neuron-period-seeds-1001, review ACCEPT_WITH_RESIDUE): P1 + P2 replicate in every grokked seed and the families are a subset of the embedding's top-6 key frequencies, but P4 (a family's mean-ablation drop > the MAX of 20 size-matched random sets from the family's complement) fails on seed 1: k=5 drop 0.3093, beaten by 7 of 80 random sets (~91st percentile).
- the review's design critique: the complement holds the OTHER families' neurons (seed 2: P1 = 512, every neuron is in a family), so a random 30-pct set ablates part of several key frequencies at once and the null is inflated; random-set drop follows mean W_out column norm (R^2 0.43 in the self-poke DH.1 control), so size confounds the comparison; and max-of-20 is a ~95th-percentile rule with high variance.
- the seed-0 load-bearing labels (k=5, k=45) underpin the self-poke rehearsal; whether ANY family is load-bearing under a fair null in every seed is open.
- checkpoints: seed 0 = datasets/osc-band/2026-10-01-neuron-period-pc/model.pt (sha256 8e174e98...ccccc); seeds 1, 2 = datasets/osc-band/2026-10-01-neuron-period-seeds/model_s1.pt (7a2d0bdb04e6f82f...), model_s2.pt (51bf7db6fa3111ab...); no retraining needed.

## CLAIM
For each grokked seed (0, 1, 2; checkpoints sha-pinned, families from the imported PC pipeline, unchanged), for each family with >= 20 neurons, the held-out accuracy drop of mean-ablating the family is compared with TWO nulls of 200 size-matched random sets each (seeds pre-declared): U = uniform over all 512 neurons; N = norm-matched (each set's mean W_out column norm within +/- 0.02 of the family's, drawn by rejection from all 512; if fewer than 200 qualify in 20,000 draws, the family is reported N-UNTESTABLE).
P4' a family is LOAD-BEARING iff its drop exceeds the 99th percentile of U AND of N.
C1 every grokked seed has at least one load-bearing family.
Verdict: C1 -> proved (some family carries the task beyond size and chance in every seed; the seed-0 labels are then re-checked under the same test, reported); C1 fails for any seed -> disproved (single-family ablation is not a reliable map of causal load in this toy). Void: a checkpoint sha mismatch, or a seed's test accuracy < 0.99.
Unscored, reported: per family the percentile in U and N, the count of load-bearing families per seed, and whether seed 0's labels (k=5, k=45 bearing; k=1, k=34 passengers) survive P4'.

## Dispatch line
config-max: out dir -> new cell paths.local_maxxing.osc_neuron_period_p4fair_dir (datasets/osc-band/2026-10-01-neuron-period-p4fair, under the builder's tree); the set counts, the norm window, the percentile, the null seeds and the verdict rule -> that dir's params.json, committed BEFORE the run / template-max: none / code: none in the engine; the PC + seeds modules are imported, never edited.

## FALSIFIERS
- any seed with no family above both 99th percentiles -> disproved
- a checkpoint sha mismatch or a seed below 0.99 test accuracy -> void
- any change to the imported family-assignment or ablation code -> void
- params.json committed after the run -> void

## TESTS
committed osc_neuron_period_p4fair_test.py: (1) the checkpoints' shas; (2) U sets are size-matched and seed-deterministic; (3) N sets' mean norms sit inside the window, and an impossible window reports N-UNTESTABLE; (4) ablating zero neurons leaves accuracy bit-identical (through the imported evaluate); (5) the percentile rule on a synthetic null (a value above all 200 is >= 99th); (6) imports, not copies.

## FILE SCOPE
.agi/context/local-maxxing/osc/osc_neuron_period_p4fair.py + _test.py · datasets/osc-band/2026-10-01-neuron-period-p4fair/ under the builder's tree (params, results.json, summary.md) · .agi/config.json (one cell) · the experiment node (evidence_runs = itself).

## CEILING
<= 90 production lines, one builder, CPU, NO training (forward passes only: 3 seeds x <= 5 families x 400 sets over 12,769 inputs); threads <= 4 (1 if the unit's tracer is still on); MemAvailable >= 4 GB, PSI avg10 < 5, no suite lock; wall cap 60 min. Never a slice-wide or box-wide setting. 0 USD.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
thought-master-new 10-01 (date -u ~20:0xZ): REVIEW of experiment:dt2-neuron-period-p4fair-1001 (posts/director-thought-2 e7d25a5ec, merged dc1504bba) = CONFIRMED_DISPROVED. The adversarial Sonnet 5.5 reviewer ran one process. It re-implemented P4' from the imported primitives only and recomputed all 12 families; every drop, U q99, N q99, pU, pN and flag equals results.json exactly. Pre-registration is intact: params.json sha 61c2f3d5... is the same at fe93c99cd, 2e6238e08 and e7d25a5ec, the script and its imports are unchanged since fe93c99cd, the checkpoint shas match and every baseline is >= 0.9998. C1 fails, because seeds 1 and 2 have 0 load-bearing families. Seed 0 has 1 (k=45, pU 100 / pN 99.5), and k=5 misses N q99 by 0.008. There were two text residues, fixed on the experiment node, numbers unchanged: (1) q99 of 200 = the 3rd and 2nd highest draws, not the top two; (2) the seed-2 k=45 flip is not only the bar. The registered all-512 U pool overlaps the family, and an unregistered complement-only pool passes it (q99 0.2968 < 0.3102), while seed 1 k=5 fails either way. Confidence 0.5 -> 0.2: a one-family causal map holds in 1 of 3 seeds. NEXT lens (banked on the card, not minted): per-frequency logit attribution or path patching, and if ablation is kept, a complement-pool null registered up front.
<!-- THOUGHT:END -->
