---
id: idea:lm-hybrid-oscillator-readout
mint_id: 683642bace844c8388723445e4fa45b9
type: idea
parents:
  - goal:g5.11
next_edges: []
edited_by: belam
scaffold_hash: 4bafd0efecfeec50
scale: big
season: 2
tags:
  - local-maxxing
  - treasury
  - hunch
thought_session: dissolve-legacy-2026-09-19
title: "\"Hybrid timeless/timeful architecture: the LLM keeps the what-token-comes-next matrix shape; a sparse spiking oscillator network reads KV-cache and head-activation bits through 10-200 subscribed read sites per neuron, with energy = frequency alignment and a small rhythm-neuron subnetwork as the metronome — the subscription set IS the weight\""
town: local-maxxing
---
# idea:lm-hybrid-oscillator-readout

## Source
Pane line in the thought-master pane, 2026-09-16 21:5xZ (owner-style, unverified as owner; ingested under the standing doc+idea GO), quoted in Provenance below. Prior art in this treasury: `hypothesis:c2-digital-kuramoto-flip-mode` (ORDER 3, digital Kuramoto byte-neurons with a seed-stable sync switch; lap pending), `idea:lm-hunch-energy-frequency-prediction` (energy ledger + frequency lock on the flip toy; predict-then-verify gate), `idea:lm-hunch-per-layer-draft-kv-share`, `idea:lm-hunch-cluster-parallel-speculation`.

## Lever (the sketch, kept in its own terms)
- Two halves. TIMELESS: an ordinary LLM does the "what token comes next" matrix computation. TIMEFUL: a spiking network of oscillator neurons that constantly reads the LLM's KV caches and head activations and uses them as on/off bit triggers (spike flip signals); bespoke spike-based attention heads via oscillatory projection.
- Energy = alignment. Each oscillator's frequency is both a measure of system energy and its predicted value. When frequencies align, propagation costs little; when they do not, aligning them costs energy, paid through selective subscription of downstream neurons.
- Sparse subscription is the weight. A neuron picks 10-200 "read sites" — specific neurons whose bits it reads for flip signals. The subscription set IS the weight adjustment; each source additionally carries one weight clamped between two non-zero values, one positive band and one negative band (never zero, never unbounded).
- Rhythm without hard-coded cadence. Neurons hold frequency bands not by a per-neuron clock but by subscribing to a small network of rhythm neurons that keep the metronome going — many steady tones others can lock onto. The quantisation of frequencies across the network is emergent from the energy mechanics, not forced.
- No strict layer hierarchy; not matrix-multiplication-organised. An oscillator steady-state system that shifts state as sentence meaning evolves.

## What it buys the town
- If the timeful half can run on the A1's CPUs or the local-town leftovers while the timeless half generates, it is a second, cheap signal about the LLM's state (energy/alignment) usable as a gate: the town already wants predict-then-verify gates (`idea:lm-hunch-energy-frequency-prediction`) and a bytes/decision row (C2). A state shift that tracks sentence meaning is a candidate kid-side "am I still on task" detector at near-zero cost.
- It names a concrete mechanism for the two open hunches (energy ledger; frequency lock): subscription-as-weight and rhythm neurons — testable in numpy.

## First falsifier
In a numpy toy (N = 256-4096 oscillator byte-neurons, 10-200 read sites each, a rhythm subnetwork of 8-32 neurons, clamped ± weights), frequencies do NOT quantise into bands within the run (histogram of steady-state frequencies stays flat/unimodal), OR a controlled change in the driving bits (a fixed substitution in the read-site inputs standing in for a KV/head change) produces no measurable steady-state shift beyond seed noise. Either kills the "emergent quantisation" and "state shifts with meaning" claims before any LLM is attached.

## Cheapest test on our iron
- Extend the C2 flip toy ($0, CPU numpy, this A1 at loadavg < 2, ≤ 20 min per run): add (a) subscription read sites (10-200, chosen once per seed, the set fixed = the weight), (b) a rhythm subnetwork with steady tones, (c) an energy ledger = alignment cost per propagation step. Measure: frequency histogram (quantisation), energy per step vs alignment, state-shift latency when the driving bits change. One kid, $1 OpenRouter for its own tokens.
- Only after that: read REAL bits — dump one layer's KV cache / head activations from the 9B on local-town (llama-server `--verbose` or a llama.cpp hook) for two contrasting sentences, feed the bit deltas as the driving input, see whether the steady state separates them. Still $0 compute.

## Numbers (none measured; the sketch's own constants)
read sites per neuron 10-200; weights clamped to two non-zero bands (positive, negative); rhythm subnetwork "small"; prior C2 pilot: K_c ~ 116/256 threshold, CV < 1% (from the C2 hypothesis title).

## Provenance
Verbatim pane line (2026-09-16 21:5xZ): "Idk yet how to incorporate spiking networks into an LLM, the best approach feels like a hybrid system that constantly reads kv-caches and head activations and uses those as on/off signal bit triggers, so it becomes a hybrid timeless/timeful architecture. LLM for literally "what token comes next" matrix computation shape with bespoke spike-based attention heads via oscillatory projection? Idk just something that uses the oscillators as both measures of system energy and its predicted value. But energy could be based on alignment, so if frequencies align it takes little energy to propagate. But if they don't align, it takes lots of energy to make them align via selective subscription of downstream neurons. That's the other idea I had, the spike neurons form relatively sparse connections of only 10-200 "read sites" where it "picks" specific neurons whose bits to read for spike flip signals. And the subscription set IS the weight adjustment, though each info source is also weighted between two clamped non-zero positive/negative values. The neurons try to maintain frequency bands but not through a set cadence hardcoded into every neuron, but rather through subscribing to a small network of rhythm neurons who help keep the metronome beat going for the rest, offering lots of steady tones that other neurons can hone in on. And the overall frequency outputs/inputs across all neurons are mostly quantized not due to forced hardcoding but due to the natural energy mechanics of the system. Neurons don't have to maintain strict layer hierarchy, it's not meant to be as organized as matrix multiplication. It's meant to be an oscillator steady-state system that shifts states as sentence meaning evolves." Minted by thought-master 2026-09-16 21:5xZ; no spend follows until a hypothesis names its cap; the natural next hypothesis is a C2 round 2 once ORDER 3's lap lands.

## Agent Notes
OWNER 2026-09-18 06:14Z (thought-master pane), verbatim: "Btw I was thinking for one ingest these and queue model downloads if it makes sense. https://arxiv.org/abs/2609.04010 https://arxiv.org/abs/2510.03215 But the kv cache comms protocol could be used to bridge multiple choice models like open jev with standard LLMs or diffusion augmented LLMs double augmented with our novel oscillator architecture via spike modeling. A magical stitching together of models and comms protocols maybe able to utilize the tiniest models. All seem to be qwen based which is nice. Or many at least." APPLY (thought-master): the double augmentation = the receiver LLM KV (after a C2C fusion) read by the spiking oscillator readout through its subscribed read sites -- that is this idea composed with hypothesis:lm-c2c-kv-bridge-released-fusers; it gets its own hypothesis only after (1) the C2C bridge reproduces on our box and (2) hypothesis:lm-bend2-spiking-sim / lm-pufferlib-oscillator-policy give a working readout -- chain no longer than the evidence.
