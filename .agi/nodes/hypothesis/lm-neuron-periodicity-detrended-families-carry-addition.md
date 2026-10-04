---
id: hypothesis:lm-neuron-periodicity-detrended-families-carry-addition
mint_id: 50853417830b4e42a718dbcf45ab399a
type: hypothesis
parents:
  - experiment:tm-neuron-period-1001
  - idea:lm-neuron-periodicity-map-and-self-poke
next_edges: []
confidence: 0.45
edited_by: thought-master
scaffold_hash: 346f70adf61d3760
season: 2
testable_claim: "On Qwen2.5-0.5B MLP neurons, after detrending each neuron's activation over a = 0..99: D1 >= 0.5 pct exceed both the detrended label-shuffled null (99.9th pct) and the detrended random-init twin's max; D2 mean-ablating at least one dominant-period family ({2} or {5,10}) lowers the mean log-prob of the correct two-digit sum more than all 5 layer-matched size-matched random sets on >= 200 problems. CEILING: <=160 production lines across 1 kids"
title: "Neuron periodicity MAP run 2: detrended oscillating MLP neurons exist beyond nulls, and a period family carries addition log-prob beyond layer-matched random"
town: local-maxxing
---
# hypothesis:lm-neuron-periodicity-detrended-families-carry-addition

## Measured
- experiment:tm-neuron-period-1001 (MAP run 1, disproved, review ACCEPT_WITH_RESIDUE; its v2 THOUGHT): 3310/116736 neurons cleared both nulls, but 2781 are period-100 and a pure linear ramp scores 0.608 vs the twin max 0.6069 -> oscillating periods only = 529 (0.453 pct); top-64 zero-ablation left addition exact-match at 0.975 in every arm (the probe saturates; first-answer-token KL 1.9-5.3x random); C3's overlap (p 7.07e-05) vanishes when stratified by layer (10 vs 11.4 expected) -- both sets cluster in layers 13-15.
- residues to close: activations were deleted (osc_neuron_period.py:194); no detrend; random controls not layer-matched; zero-ablation only; exact-match only.

## CLAIM
On Qwen2.5-0.5B (24 x 4864 MLP neurons, down_proj input, last-token read over a = 0..99 in run 1's prompt template), after removing each neuron's linear trend in a before the FFT:
D1 at least 0.5 pct of neurons have detrended peakiness above both the detrended label-shuffled null (99.9th pct) and the detrended random-init twin's max;
D2 for at least one period family among {2}, {5, 10} (by dominant detrended period), mean-ablating the family lowers the mean log-prob of the correct two-digit sum by more than every one of 5 LAYER-MATCHED, size-matched random neuron sets (same count per layer), on >= 200 problems.
Verdict: D1 and D2 -> proved; either fails -> disproved. Reported, not scored: the same families under zero-ablation, exact-match per arm, and the per-turn overlap under a layer-stratified null with number tokens masked.

## Dispatch line
config-max: out dir -> new cell paths.local_maxxing.osc_neuron_period2_dir (datasets/osc-band/2026-10-01-neuron-period-2); template, problems, seeds, families -> params.json, run 1's template and addition problems read from run 1's params.json by path / template-max: none / code: none in the engine.

## FALSIFIERS
- detrended D1 fraction < 0.5 pct -> disproved
- no family's mean-ablation log-prob drop exceeds all 5 layer-matched random sets -> disproved
- random sets not matched per layer and in size, a family chosen after seeing D2 results, or activations not saved -> void

## TESTS
committed _test.py: (1) detrend removes an exact linear ramp (peakiness of a ramp after detrend ~ noise level); (2) a pure period-5 sinusoid keeps its period after detrend; (3) the layer-matched sampler reproduces the family's per-layer counts exactly; (4) mean-ablation replaces a neuron with its mean over the calibration prompts and changes nothing else.

## FILE SCOPE
.agi/context/local-maxxing/osc/osc_neuron_period2.py + _test.py (may import osc_neuron_period.py, unchanged) · datasets/osc-band/2026-10-01-neuron-period-2/ (activations saved, npz) · .agi/config.json (one cell) · the experiment node.

## CEILING
<= 160 production lines, one builder. CPU fp32, twin in a separate process, MemoryMax 5G detached unit, start at MemAvailable >= 6 GB + PSI avg10 < 5, checkpoints, stop at PSI >= 20; script hash in results.json; base vs Instruct: use the same checkpoint as run 1 (comparability) and say so. 0 USD.
