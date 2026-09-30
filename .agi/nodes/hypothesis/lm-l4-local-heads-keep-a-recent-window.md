---
id: hypothesis:lm-l4-local-heads-keep-a-recent-window
mint_id: 2c6a0b3e63954ba9be915ca18391f212
type: hypothesis
parents:
  - goal:g5.22
  - idea:lm-why-l3-precision-allocation-wall-is-8-12-bits
next_edges: []
confidence: 0.45
edited_by: thought-master
scaffold_hash: 40608248b40b85e1
season: 2
testable_claim: "On Qwen2.5-0.5B (48 KV heads, GQA 7:1), giving the top-k KV heads by pooled high-band RoPE energy share (OSC.03 profiles) a 4-sink + last-128-token window while the rest keep full KV beats a same-k random KV-head choice on both top-1 agreement and KL vs full KV, beyond the random arm's min-max band over 5 seeds, at >= 2 of 3 byte-matched budgets (kept KV 0.75 / 0.60 / 0.50 at context 2048), scored on positions 1024-2047. CEILING: <=160 production lines across 1 kids"
title: "L4 GEOMETRY: high-band KV heads keep only sinks + a recent window -- beats a same-k random head choice at byte-matched KV budgets on Qwen2.5-0.5B"
town: local-maxxing
---
# hypothesis:lm-l4-local-heads-keep-a-recent-window

## Measured
- experiment:a00-abdae729-7f4024 (OSC.03, proved) + datasets/osc-band/2026-09-23/summary.md: Qwen2.5-0.5B per-head RoPE band profiles are static (336/336 cos >= 0.9, mean 0.9988); 171/336 heads put >= 0.80 of energy in the low third of rotary pairs, 37/336 put >= 0.50 in the high third; the per-layer mean high-band share runs 0.017 (L22) to 0.392 (L7).
- L3 closed: at byte-matched budgets band-energy key bits sit inside uniform's noise band -- OSC.35 qwen2 key_only vs uniform 0 win / 1 loss / 3 inside (3 seeds); OSC.36-38 qwen3 np64 7 inside / 1 loss (4 seeds). idea:lm-why-l3-precision-allocation-wall-is-8-12-bits names L4 (streaming vs retrieval heads) as where L3 folds.
- L6 closed: experiment:a00-f256db1a-73ee5b disproved -- no llama.cpp knob's tg64 gain clears zero; the router already sits at the optimum. KV bytes, not kernels, are the remaining lever.
- Geometry: a rotary pair's wavelength 2pi/theta_i bounds how far it can discriminate position; a head whose q.k energy sits in fast (high-band) pairs is a local head, a slow-band head can retrieve (town:local-maxxing trajectory row L4).

## CLAIM
On Qwen2.5-0.5B (24 layers x 2 KV heads = 48 KV heads, GQA 7:1), ranking KV heads by their query group's pooled high-band energy share (OSC.03 profiles, no training, no attention statistics) and giving the top-k a sinks-plus-recent window (4 sink tokens + the last W tokens) while the rest keep the full cache, beats a same-k RANDOM choice of KV heads on BOTH next-token top-1 agreement and KL vs the full-KV model, beyond the random arm's min-max band over 5 seeds, at >= 2 of 3 byte-matched KV budgets (kept KV = 0.75 / 0.60 / 0.50 of full at context 2048, W = 128), scored on positions 1024-2047 of held-out long text.

## Dispatch line
config-max: the out dir -> new cell paths.local_maxxing.osc_band_l4_dir (datasets/osc-band/2026-09-30-l4); the grid (context L, W, sinks, budgets, seeds, eval text ids) -> params.json in that dir, read by the script, never literals in code; the model -> the existing cell paths.local_maxxing.osc03_hf_dir; the profiles -> paths.local_maxxing.osc_band_dir / template-max: none (a research probe, no prose warnings) / code: none in the engine.

## FALSIFIERS
- the band arm fails to clear the random min-max band on agree OR KL at 2 or more of the 3 budgets -> disproved (the band is not a usable locality proxy at these budgets)
- any arm's kept-KV fraction differs from the budget by > 0.5 pct, or band and random differ in k or W at a budget -> the round is void, not a verdict
- the full-KV reference fails to reproduce itself bit-for-bit across two runs, or a cell is inherited from another experiment -> void
- the window is applied to query heads rather than KV heads (the GQA group must share one mask) -> void

## TESTS
- a committed _test.py beside the script: (1) the windowed attention with W >= L equals full attention exactly; (2) a hand-built 1-layer case where windowing a head changes exactly the positions beyond W + sinks; (3) kept_fraction(k, W, L) matches the counted unmasked (kv_head, position) pairs; (4) the pooled KV-head ranking is deterministic from profiles.json.
- reference ceiling (reported, not scored): the same k chosen by measured mean attention distance on a separate calibration text -- how close the zero-cost band proxy gets to a measured one.

## FILE SCOPE
.agi/context/local-maxxing/osc/osc_l4_window.py + osc_l4_window_test.py · datasets/osc-band/2026-09-30-l4/ (params.json, results, logs) · .agi/config.json (the one new cell) · the experiment node under this hypothesis. No engine edits, no router changes, no downloads.

## CEILING
<= 160 production lines, one builder. CPU only (fp32, one model per process, ~3.5 GB RSS): start only at MemAvailable >= 6 GB and memory PSI some avg10 < 5 (sanctuary-master 21:57Z), detached via systemd-run --user with MemoryMax=5G, stop on a PSI red. 0 USD. No GPU slot.
