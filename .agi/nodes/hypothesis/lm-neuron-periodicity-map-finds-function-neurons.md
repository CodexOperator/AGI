---
id: hypothesis:lm-neuron-periodicity-map-finds-function-neurons
mint_id: 0cd409a168a349bea0861c36f99def31
type: hypothesis
parents:
  - idea:lm-neuron-periodicity-map-and-self-poke
  - goal:g5.28
next_edges: []
confidence: 0.5
edited_by: thought-master
scaffold_hash: 4eb098746f998cce
season: 2
testable_claim: "On Qwen2.5-0.5B MLP neurons (down_proj input): C1 >= 0.5 pct of neurons are periodic over a swept value a=0..99 beyond both a label-shuffled null (99.9th pct) and a random-init twin's max; C2 zero-ablating the top-64 value-periodic neurons cuts two-digit addition accuracy more than 64 random neurons, beyond the random min-max over 5 seeds; C3 (scored separately) the top-1 pct neurons by periodicity over token position in one 2048-token turn overlap the C1 set beyond chance (hypergeometric p < 0.01). CEILING: <=180 production lines across 1 kids"
title: "Neuron periodicity MAP (stage 1): value-periodic MLP neurons exist beyond nulls, carry addition, and the cheap per-turn periodicity finds them"
town: local-maxxing
---
# hypothesis:lm-neuron-periodicity-map-finds-function-neurons

## Measured
- idea:lm-neuron-periodicity-map-and-self-poke (owner 22:0xZ 09-30, verbatim in its grid v0 THOUGHT): rank neurons by the Fourier periodicity of their activations; stage 1 = the MAP, before any self-poke.
- prior art (from memory, unverified by the treasury): mod-p transformers compute with a few key Fourier frequencies; pretrained LLMs represent integers with periodic features (periods near 2, 5, 10) for addition.
- this town: OSC.03 (experiment:a00-abdae729-7f4024) -- attention heads carry static RoPE band fingerprints; experiment:tm-l4-window-0930 -- that band is a weak locality proxy (rank corr 0.32 with measured attention distance). No MLP-neuron spectral measurement exists in the graph.

## CLAIM
On Qwen2.5-0.5B (24 layers x 4864 MLP neurons, read at the down_proj input act(gate) * up):
C1 VALUE AXIS: sweeping a = 0..99 in a fixed prompt and reading each neuron at the prompt's last token, at least 0.5 pct of neurons have spectral peakiness (max non-DC power / total non-DC power over a) above BOTH the 99.9th percentile of a label-shuffled null (a permuted, 20 permutations) AND the maximum of a random-init twin.
C2 FUNCTION: zero-ablating the top-64 value-periodic neurons cuts two-digit addition exact-match more than 64 random neurons do, beyond the random arm's min-max over 5 seeds (baseline accuracy must be >= 0.5, else C2 is void).
C3 THE OWNER'S BRIDGE (scored separately): the top-1 pct neurons by peakiness over token POSITION in one ordinary 2048-token turn (shuffled-token control subtracted) overlap the C1 set more than chance, hypergeometric p < 0.01.
Verdict: C1 and C2 -> proved; either fails -> disproved; C3 reported as its own conjunct whatever the verdict.

## Dispatch line
config-max: the out dir -> new cell paths.local_maxxing.osc_neuron_period_dir (datasets/osc-band/2026-10-01-neuron-period); the sweep, prompt templates, k, seeds, permutations, turn text id -> params.json there / template-max: none / code: none in the engine.

## FALSIFIERS
- fewer than 0.5 pct of neurons clear both nulls on the value axis -> C1 false
- top-64 ablation inside the random min-max band -> C2 false
- the random-init twin or the shuffled null is skipped, or a cell is reused from another round -> void
- baseline addition accuracy < 0.5 -> C2 void (report, do not score)

## TESTS
committed _test.py: (1) peakiness of a pure sinusoid = 1 and of white noise ~ 2/N; (2) the hook reads exactly the down_proj input (shape 4864 per layer); (3) zero-ablation of a neuron changes the forward only through that neuron's down_proj column; (4) the label-shuffled null keeps the activation multiset.

## FILE SCOPE
.agi/context/local-maxxing/osc/osc_neuron_period.py + _test.py · datasets/osc-band/2026-10-01-neuron-period/ · .agi/config.json (one cell) · the experiment node under this hypothesis.

## CEILING
<= 180 production lines, one builder. CPU fp32, one model per process (the random-init twin in a SEPARATE process), MemAvailable >= 6 GB + memory PSI some avg10 < 5 at start, systemd-run --user MemoryMax=5G, per-step checkpoints, stop on PSI >= 20. 0 USD.
