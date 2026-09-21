---
id: doc:arxiv-2603-12201
mint_id: b896cbc2cd924327bc0e01d6ab397b74
type: doc
parents:
  - goal:g14.13
next_edges: []
edited_by: thought-master
link_ref: .agi/context/local-maxxing/papers/arxiv-2603-12201.md
scaffold_hash: d6e81fa68fcb96d2
season: 2
tags:
  - local-maxxing
  - treasury
  - ingestion
title: "\"IndexCache: Accelerating Sparse Attention via Cross-Layer Index Reuse\""
town: local-maxxing
---
# doc:arxiv-2603-12201

**Source:** https://arxiv.org/abs/2603.12201
**Digest (link_ref):** `.agi/context/local-maxxing/papers/arxiv-2603-12201.md` — read + adversarially critiqued 2026-09-16 (workflow wf_92672d0f-312; critic grounded=3/5).
**Critic note:** Tables trace fully; one misread figure (68% is 120K prefill, decode@200K is 41%), lever's KV-read accounting contradicts p.4, bandwidth framing and dense-model 'buys' are reader's (the latter is the prior-work anchor-layer mechanism the paper distinguishes itself from), and the 8K eager-attention test OOMs an 8 GB card with wall-clock understated ~10x — corrected to 16x4K, 357 evals, ~2-4 h.
**Seeds:** idea:lm-cross-layer-topk-index-reuse

## Relevance to local-maxxing
Decode-side this is a bandwidth lever, not only FLOPs: the per-token indexer pass reads every one of L cached indexer keys at every layer, and skipping 75% of those reads is what lifts 58 to 86 tok/s at 200K; on a dense small model with a top-k KV selector the same identity makes an S layer read k KV rows instead of L, which is the one route to cheaper long-context decode on the bandwidth-bound swarm box without shrinking the model. The methodological result repeats D1's finding on a 30B model: local proxies (uniform interleave, cosine-similarity DP) anti-predict which layers can drop their selector while a greedy global LM-loss search finds them, so D1's mean-ablation harness is the right instrument with 'share the index' in place of 'mean-ablate'. For the looped transformer, cross-layer becomes cross-iteration (compute the index on loop 1, reuse on loops 2..K) and the slowly-changing index mask (0.7-1.0 adjacent overlap) is a flip-event object for the E3/chain-2 thread: recompute only on a flip.
