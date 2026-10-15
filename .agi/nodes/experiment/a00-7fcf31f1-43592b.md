---
id: experiment:a00-7fcf31f1-43592b
mint_id: 0b48da3b66034bc8b571ed47657909f0
type: experiment
parents:
  - hypothesis:lm-oscillator-research-hunt
next_edges: []
confidence: 0.6
edited_by: a00-7fcf31f1
evidence_runs:
  - experiment:a00-7fcf31f1-43592b
loop: hypothesis:lm-oscillator-research-hunt@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 5543ccbbc0089916
season: 2
title: oscillatory-metronome-reader-hunt digest-landed
town: local-maxxing
verdict: inconclusive_lean_proved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-7fcf31f1-43592b

## Experiment

READER hunt (oscillatory key) — fetched 11 arxiv abs/API pages via curl (2026-09-16), wrote digest troves/2026-09-16-oscillatory/oscillatory.md.

Hunted: AKOrN 2410.13821, LinOSS 2410.03943, Energy-Based Transformers 2507.02092, Ramsauer Modern Hopfield 2008.02217, Krotov dense AM 1606.01164, SpikeGPT 2302.13939, Spike-driven v1 2307.01694 + v2 2404.03663, spiking CPG lamprey 2101.07001, phase-coded RAG 2511.11848, phase-codes-emerge 2310.07908, predictive-coding+InfoBottleneck hallucination 2601.15652.

End-answers: (1) three closest to the metronome = AKOrN (oscillator-as-state, binding-by-synchrony), phase-codes-emerge-in-RNN (emergent frequency quantisation), spiking-CPG + LinOSS (dedicated rhythm subnetwork, LinOSS proves nonnegative-diagonal stability). (2) smallest numpy test = rhythm-bank metronome toy: K=8 steering tones, N≈200–1000 oscillators each subscribing to 10–200 bits with clamped ±weights, Kuramoto push + alignment-cost energy; measure frequency-histogram quantisation, energy-vs-alignment, and re-lock latency after a driver-bit flip (falsifier for "steady state shifts with meaning"). Minutes, $0.

## Evidence

trove file: .agi/context/local-maxxing/troves/2026-09-16-oscillatory/oscillatory.md (11 sourced papers, every claim URL+date tagged MEASURED|ESTIMATE). Iron fit: all mechanisms numpy-on-A1, no GPU needed. All licences ESTIMATE (not fetched).

## Agent Notes
returned oscillatory metronome digest: 11 sourced papers, 3 closest mechanisms + numpy toy, mapped to owner sketch
