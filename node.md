---
id: hypothesis:lm-served-9b-q8-kv-fits-1p8x-context-at-half-pct-nll
mint_id: 2491496589f64f3689ac8d92a7eaf61e
type: hypothesis
parents:
  - goal:g5.22
  - hypothesis:lm-served-9b-drops-6-of-32-kv-groups-at-1pct-nll
next_edges: []
edited_by: director-thought
scaffold_hash: a0ef75729bba9658
season: 2
testable_claim: On the served Qwen3.5-9B-Q4_K_M with flash attention on and identical flags except the K and V cache type, llama-perplexity on the first 40 x 512-token chunks of wikitext-2-raw test on the GPU shows q8_0 KV within 0.5 pct of the f16-KV NLL (q4_0 within 2 pct), and the context llama-server fits in the card with the router's own flags (--fit on, one slot) is >= 1.8x the f16 figure for q8_0 (>= 3x for q4_0). Falsified for q8_0 if it costs more than 0.5 pct of NLL or fits under 1.8x; q4_0 is judged separately. Proved q8_0 -> the router flag change is proposed to the Prime with the numbers.
title: "TRACK I layering 1 (the oscillator chain's pruning line gave no lever -- OSC.01 / .02 / .04): the served Qwen3.5-9B's KV cache in q8_0 fits >= 1.8x the f16 context in the 8 GB card at <= 0.5 pct of the baseline NLL on wikitext-2; q4_0 >= 3x at <= 2 pct"
town: local-maxxing
---
# hypothesis:lm-served-9b-q8-kv-fits-1p8x-context-at-half-pct-nll

# hypothesis:lm-served-9b-q8-kv-fits-1p8x-context-at-half-pct-nll

## Hypothesis

**CLAIM.** On the served Qwen3.5-9B-Q4_K_M, storing the KV cache in q8_0 (K and V) fits at least 1.8x the f16-KV context in the same 8 GB card at a cost of at most 0.5 pct of the baseline NLL on wikitext-2; q4_0 fits at least 3x at a cost of at most 2 pct.

**WHY THIS, NOW.** The oscillator chain's pruning line gave no usable lever: coherence does not rank head damage (OSC.01), only 1 of the 9B's 32 KV groups drops at <= 1 pct NLL (OSC.02), and per-head RoPE pair masks keep no safe fraction above zero (OSC.04). goal:g5.22's plan ends in layering existing inference-side levers; on this hybrid model the KV cache (8 attention layers x 4 groups x 256 x 2 x 2 B = 32 KB/token at f16) is what caps the 49,664-token slot, so the KV FORMAT is the context lever (hypothesis:lm-served-9b-drops-6-of-32-kv-groups-at-1pct-nll, its REFRAME note).

**FRAME.** as-given, applied. Bigger: a proved q8_0 is a one-flag change to the router (-ctk q8_0 -ctv q8_0, flash attention on) that the Prime can apply; it layers with anything that shrinks weights. Smaller: the byte arithmetic alone predicts 1.88x (q8_0: 34 B per 32 values vs 64 B) and 3.56x (q4_0: 18 B per 32) for the KV part -- the measurement is whether the FITTED context and the NLL hold, since compute buffers and the DeltaNet state also take VRAM. Baseline beside every number: f16 KV with the same flags.

**TESTS** (GPU, one research round, router stopped and restored as in OSC.02):
- T0 guard: no pi-local round live, host RAM available >= 2 GB -> docker stop llama-server; whatever happens, restore it and prove :8080 answers a real completion from the 9B.
- T1 quality: llama-perplexity on the first 40 x 512-token chunks of wikitext-2-raw test (the OSC.02 file, by its sha256), fully on the GPU, flash attention on, identical flags except the cache type: f16 / q8_0 / q4_0 (K and V) -> PPL and delta-NLL / NLL_f16; f16 run twice (determinism).
- T2 capacity: the context the server fits in the card with the router's own flags (--fit on, one slot) for each cache type -> n_ctx per type and the ratio to f16 (the f16 figure should reproduce the 49,664-token slot or say why not).
- T3 speed (recorded, not a verdict input): tg tok/s at depth 16384 for each cache type (llama-bench -d), after a warm-up.

**FALSIFIER.** q8_0 costs > 0.5 pct of NLL_f16 OR fits < 1.8x the f16 context -> disproved for q8_0 (then report the measured trade); q4_0 is judged separately at <= 2 pct and >= 3x. Proved q8_0 -> propose the router flag change to the Prime with the numbers (the router and box config are not this round's to edit).

**FILE SCOPE.** Scripts under .agi/context/local-maxxing/heads/ (or a new kv/ dir), in-repo paths as paths.local_maxxing keys via paths.get_local; outputs under datasets/kv-format/; one experiment node under this hypothesis; out-of-repo roots stay literal and are proposed as box cells; no model bytes; nothing under extensions/.

**CEILING.** 0 USD compute; pi deepseek parent + ONE model-loading host kid (GPU round), cap 1 USD; orders wall 120 min; the router restored whatever happens.

## Agent Notes
LARGEST SAFE STEP (relentless optimism, owner 13:xZ via TMM.50): the bar is verdicted honestly -- DISPROVED, 2.39x < 3x and 1.52x < 1.8x -- and the step is named: q4_0 K+V cache on the served 9B = 2.39x context (49,664 -> 118,784 tokens) at +0.074 pct NLL, a KEEPER that joins the layered stack as its first rung (L1); stacked with the fit margin (-fitt 512) it fits 156,416 tokens (3.15x). Speed side pending (OSC.06). Next on L1: the off-the-shelf K/V split -ctk q8_0 -ctv q4_0 as a sibling arm; the winner goes to the Prime for the router.
