---
id: hypothesis:lm-band-pruned-k-cache-compounds-with-q4-kv
mint_id: 99eab27f9bc746b78a1a6f99d447af96
type: hypothesis
parents:
  - hypothesis:lm-band-pruned-heads-keep-next-token-agreement
  - hypothesis:lm-q4-kv-cache-tg-at-4k
next_edges: []
edited_by: thought-master
scaffold_hash: 48d790d8875b04cf
season: 2
testable_claim: "On Qwen2.5-0.5B-Instruct (HF bf16, rig) with the hop-2 per-head masks at the 95 pct energy setting: storing per head only its kept RoPE pairs of K, fake-quantised to 4-bit round-to-nearest in groups of 32 (the q4_0 layout of hypothesis:lm-q4-kv-cache-tg-at-4k), over the same 4096-token eval gives mean KL <= 0.03 against the full-precision full-K model, at K-cache bytes per token per layer <= 1/1.6 of plain 4-bit full-K (bytes computed exactly from kept-pair counts, group scales included); V untouched; falsifier: KL > 0.03 at the >= 1.6x byte ratio -- then band pruning and 4-bit K do not compound and the join is recorded as a measured trade-off curve (bytes vs KL) instead; throughput (tg at depth 4096 in llama.cpp) is explicitly OUT of scope here -- it needs a ggml patch and is its own hop; 0 USD compute, cap 1 USD pi"
title: "oscillator x KV join: RoPE pairs a head never uses are never stored -- band-pruned K on top of 4-bit K gives >= 1.6x fewer K-cache bytes than 4-bit alone at KL <= 0.03, compounding chain A with the measured q4 KV line"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-band-pruned-k-cache-compounds-with-q4-kv

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
