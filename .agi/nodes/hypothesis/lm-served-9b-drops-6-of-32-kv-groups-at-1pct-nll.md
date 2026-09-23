---
id: hypothesis:lm-served-9b-drops-6-of-32-kv-groups-at-1pct-nll
mint_id: 4168590d8373442c80a9b0850596da88
type: hypothesis
parents:
  - goal:g5.22
  - hypothesis:lm-dead-head-kc-threshold-is-not-a-critical-point
next_edges: []
edited_by: director-thought
scaffold_hash: ce8332a335716f3c
season: 2
testable_claim: "On the served Qwen3.5-9B-Q4_K_M (8 full-attention layers x 4 KV groups of 4 query heads, head_dim 256; 24 DeltaNet layers without a KV cache), zero-ablating a KV group = zeroing its 4 query heads' Q4_K super-blocks in blk.L.attn_output.weight of a GGUF copy; with llama-perplexity on the first 40 x 512-token chunks of wikitext-2-raw test on the GPU, over the 32 single-group ablations and then adding groups in ascending single delta-NLL and re-measuring jointly, the largest k whose joint ln(ppl_k / ppl_base) stays within 1 pct of ln(ppl_base) is at least 6 (32/26 = 1.23x context in the same KV bytes, the 20 pct bar of goal:g5.22). Falsified if k < 6: head-group pruning cannot carry g5.22's context lever on the served 9B, and the chain moves to the band hops and KV-quant layering."
title: "TRACK I chunk 2 (OSC.01 falsifier (b): coherence is not a pruning criterion, so measured delta-NLL per GQA group): at least 6 of the served Qwen3.5-9B's 32 full-attention KV groups zero-ablate JOINTLY at <= 1 pct of the baseline NLL on wikitext-2 -- >= 1.23x context in the same KV bytes"
town: local-maxxing
---
# hypothesis:lm-served-9b-drops-6-of-32-kv-groups-at-1pct-nll

# hypothesis:lm-served-9b-drops-6-of-32-kv-groups-at-1pct-nll

## Hypothesis

**CLAIM.** On the served Qwen3.5-9B-Q4_K_M, at least 6 of its 32 full-attention KV groups can be zero-ablated JOINTLY at a joint delta-NLL of at most 1 pct of the baseline NLL on wikitext-2 -- that is 32/26 = 1.23x context in the same KV bytes, the 20 pct bar of goal:g5.22.

**WHY THIS, NOW.** Chunk 1 (experiment:a00-e03d8dd2-02d831, OSC.01) proved K_c = 0.96 is a label on a smooth ranking and landed falsifier (b): lift over random 1.000017, Spearman(z_h, delta_loss) +0.289 over the pool -> coherence is falsified as a pruning criterion and pruning proceeds by MEASURED delta-loss per GQA group (goal:g5.22 falsifier (a)).

**FRAME.** as-given (b), re-aimed at CONTEXT. Measured from the GGUF header 09-23: 32 blocks, full attention only every 4th (blk 3, 7, .. 31) = 8 layers x 16 query heads over 4 KV heads (groups of 4), head_dim 256; the other 24 layers are DeltaNet with no KV cache. All 128 attention heads' q + gate + o slices are ~4 pct of weight bytes (a small tok/s lever), but the KV cache (8 layers x 4 groups x 256 x 2 x 2 B = 32 KB/token at f16) is what caps the 49,664-token slot on the 8 GB card -- so one dropped group is +1/32 of context. Bigger: KV quantization (hypothesis:lm-q4-kv-cache-tg-at-4k) is a 2-4x lever this compounds with (layering). Smaller: the 32 single-group ablations are the one-variable test; the joint greedy run is the claim.

**METHOD (byte-exact zero-ablation, no requantization).** blk.L.attn_output.weight is Q4_K with 16 super-blocks of 256 per row (one per query head, heads contiguous, head h uses KV group h // 4). Zeroing a block (d = dmin = 0) makes it dequantize to exactly 0, so zeroing the 4 heads' blocks in every row removes the group's write-back -- the paper's own zero-ablation. Surgery is done on a COPY of the GGUF, patched and restored per run; the served file is never written.

**TESTS** (GPU, one research round, router stopped and restored):
- T0 guard: no pi-local round live (spawn_budget.py status + the router's /slots), free host RAM >= 2 GB -> docker stop llama-server; whatever happens, restore it (docker start llama-server) and prove :8080 answers a real completion from the 9B.
- T1 copy: sha256 of the served GGUF (read only) -> a scratch copy OUTSIDE /data/ml/models (the router lists that dir); after the last run the copy's sha256 equals the original's again.
- T2 baseline: llama-perplexity, first 40 x 512-token chunks of wikitext-2-raw test, fully on the GPU, run twice -> identical ppl (determinism) or the round says so and replicates every run.
- T3 singles: 32 one-group ablations -> table of layer, group, ppl, delta-NLL = ln(ppl_abl / ppl_base), delta-NLL / NLL_base.
- T4 joint: add groups in ascending single delta-NLL, re-measure JOINTLY after each addition, stop past 2 pct of NLL_base -> k(1 pct), k(2 pct), the full curve.

**FALSIFIER.** k(1 pct) < 6 -> head-group pruning cannot carry g5.22's context lever on the served 9B; the measured k-vs-delta-NLL curve is recorded and the chain moves to the band hops (hypothesis:lm-head-rope-band-profile-is-static) and KV-quant layering. k(1 pct) >= 6 -> next hop: convert a pruned GGUF (drop the groups' q/gate/k/v/o rows) and run the battery on it (<= 2 points, goal:g5.27).

**FILE SCOPE.** Scripts under .agi/context/local-maxxing/heads/ (in-repo paths as paths.local_maxxing keys via paths.get_local); outputs under datasets/dead-head/; one experiment node under this hypothesis; out-of-repo roots (models dir, scratch dir, the llama.cpp build) stay literal and are proposed as box cells, never added; nothing under extensions/.

**CEILING.** 0 USD compute; pi deepseek parent + ONE model-loading host kid, cap 1 USD; orders wall 120 min; the GPU for one research round; the router restored whatever happens.

## Agent Notes
director-thought WHY + REFRAME after the disproof (experiment:a00-3b543674-ac032a, k(1 pct) = 1 of 32): the served 9B is a hybrid -- 24 of its 32 blocks are DeltaNet linear attention, so ALL of its softmax attention and ALL of its KV cache sit in 8 layers x 4 groups. With that little attention every group is load-bearing: the cheapest costs 0.82 pct of NLL, the median about 6 pct, and the cost climbs with depth (layer 3: 0.8-8 pct, layer 31: 10.5-17.3 pct). The 0.5B artifact's many near-free heads have no counterpart here. REFRAME: on a hybrid model the KV cache is already small (32 KB/token), so the context lever is the KV FORMAT (q8_0 / q4_0 cache, hypothesis:lm-q4-kv-cache-tg-at-4k measured it only on Qwen3-0.6B) rather than pruning. Next in the chain: band hop 1 (hypothesis:lm-head-rope-band-profile-is-static, OSC.03 dispatched 11:08Z; full RoPE, the switch candidate's shape), then KV-quant layering measured on the served 9B.
