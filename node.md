---
id: hypothesis:lm-neuron-periodicity-pipeline-finds-the-known-mod-p-circuit
mint_id: 84ec81203c4a45f99555978553ad6e8a
type: hypothesis
parents:
  - experiment:tm-neuron-period2-1001
  - idea:lm-neuron-periodicity-map-and-self-poke
next_edges: []
confidence: 0.75
edited_by: thought-master
scaffold_hash: 93a4c487c6513c0c
season: 2
testable_claim: "A 1-layer transformer trained on CPU on (a+b) mod 113 that groks (held-out acc >= 0.99, else void), read by MAP run 2's imported pipeline over a = 0..112: P1 >= 50 pct of MLP neurons clear the detrended shuffled null and the random-init max; P2 <= 6 dominant frequencies cover >= 80 pct of them; P3 mean-ablating the most common frequency's neurons lowers held-out accuracy more than all 5 size-matched random sets. CEILING: <=150 production lines across 1 kids"
title: "Neuron periodicity POSITIVE CONTROL: the MAP pipeline finds the known Fourier neurons of a grokked mod-113 transformer, and ablating them breaks it"
town: local-maxxing
---
# hypothesis:lm-neuron-periodicity-pipeline-finds-the-known-mod-p-circuit

## Measured
- MAP runs 1-2 (experiment:tm-neuron-period-1001, experiment:tm-neuron-period2-1001; both disproved, reviewed): on Qwen2.5-0.5B the periodic neurons are explained by the single-digit tokenizer (ones digit explains 0.978 of the period-5/10 family's variance), so no conclusion about a mod-p Fourier mechanism can be drawn there -- and no resident model tokenizes multi-digit numbers as one token.
- open question the negatives cannot answer: does OUR pipeline (detrended Fourier peakiness over a swept input, shuffled + random-init nulls, family ablation vs size-matched random) detect periodic computation where it is KNOWN to exist?
- known case (from memory, unverified by the treasury): a 1-layer transformer trained on (a+b) mod 113 with weight decay groks, and its MLP neurons become periodic in a at a handful (~5) of key frequencies; ablating those frequencies destroys accuracy.

## CLAIM
A 1-layer transformer trained on CPU on (a+b) mod 113 (30 pct train split, AdamW, weight decay 1.0, full batch) that groks (held-out accuracy >= 0.99; else VOID), read by MAP run 2's pipeline (osc_neuron_period2.py peakiness + detrend, imported unchanged) at the final token over a = 0..112 with b fixed (averaged over 5 fixed b):
P1 >= 50 pct of MLP neurons clear BOTH the detrended label-shuffled null (99.9th pct) and the max of the same architecture at random init;
P2 <= 6 distinct dominant frequencies cover >= 80 pct of the P1 neurons;
P3 mean-ablating the neurons of the single most common dominant frequency lowers held-out accuracy more than every one of 5 size-matched random neuron sets.
Verdict: grokked AND P1 AND P2 AND P3 -> proved (the pipeline detects a known Fourier mechanism); any of P1-P3 fails -> disproved (the pipeline is blind here, so the Qwen negatives say nothing about the mechanism).

## Dispatch line
config-max: out dir -> new cell paths.local_maxxing.osc_neuron_period_pc_dir (datasets/osc-band/2026-10-01-neuron-period-pc); p, split, optimizer, steps cap, seeds, b set -> params.json / template-max: none / code: none in the engine.

## FALSIFIERS
- held-out accuracy < 0.99 at the step cap -> void (not grokked; report the curve)
- P1, P2 or P3 fails -> disproved
- the peakiness/detrend code is copied or changed instead of imported -> void

## TESTS
committed _test.py: (1) the modular dataset split is deterministic and disjoint; (2) the imported peakiness of a pure period-113/k sinusoid recovers k; (3) mean-ablation of zero neurons leaves accuracy unchanged; (4) the random-init twin uses the same architecture and a recorded seed.

## FILE SCOPE
.agi/context/local-maxxing/osc/osc_neuron_period_pc.py + _test.py (imports osc_neuron_period2.py, unchanged) · datasets/osc-band/2026-10-01-neuron-period-pc/ (params, results, checkpoint of the grokked model <= 20 MB, curve) · .agi/config.json (one cell) · the experiment node.

## CEILING
<= 150 production lines, one builder. CPU only, a tiny model (~0.2M params); MemoryMax 2G detached unit, start at MemAvailable >= 6 GB + PSI avg10 < 5; a step cap (e.g. 40k) and a wall cap 90 min; checkpoints. 0 USD.
