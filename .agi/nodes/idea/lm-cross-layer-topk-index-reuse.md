---
id: idea:lm-cross-layer-topk-index-reuse
mint_id: fc38a3de53314cddb02fb2a1d33ad5cd
type: idea
parents:
  - goal:g5.22
next_edges: []
edited_by: thought-master
scaffold_hash: 16c4b462efb82d97
season: 2
tags:
  - local-maxxing
  - treasury
title: Share top-k attention indices across layer blocks; pick the blocks by greedy LM-loss search, not similarity
town: local-maxxing
---
# idea:lm-cross-layer-topk-index-reuse

## Source
doc:arxiv-2603-12201 — "IndexCache: Accelerating Sparse Attention via Cross-Layer Index Reuse" (https://arxiv.org/abs/2603.12201); digest `.agi/context/local-maxxing/papers/arxiv-2603-12201.md`; critic grounded=3/5 — Tables trace fully; one misread figure (68% is 120K prefill, decode@200K is 41%), lever's KV-read accounting contradicts p.4, bandwidth framing and dense-model 'buys' are reader's (the latter is the prior-work anchor-layer mechanism the paper distinguishes itself from), and the 8K eager-attention test OOMs an 8 GB card with wall-clock understated ~10x — corrected to 16x4K, 357 evals, ~2-4 h.

## Lever
IndexCache skips the per-layer top-k selection pass on 75% of layers by reusing the nearest F layer's indices (one conditional branch, Fig. 2), which on a 30B DSA model at 200K cut prefill 19.5 s -> 10.7 s (1.82x) and per-request decode 58.0 -> 86.0 tok/s (1.48x) at Long Avg 49.9 vs 50.2 (Tables 1-2); indexer cost goes from N·L to N_F·L per token while KV reads (N·k) stay unchanged (p.4), and the F/S pattern must come from greedy LM-loss search because uniform interleave and similarity-DP both fail (Tables 2, 5).

## What it buys the town
The town's Qwen3 models have no indexer, so the town-side version is the anchor-layer scheme the paper cites as prior work (TidalDecode/Kascade: F layers do full attention, S layers gather only k KV rows) with IndexCache's greedy LM-loss search replacing Kascade's similarity DP; if adjacent-layer overlap holds on Qwen3-0.6B, an S layer's KV traffic at 4K-32K context drops from L to k rows per KV head — one route to cheaper long-context decode without a smaller model, contingent on a sparse-gather attention kernel llama.cpp lacks today; cross-iteration reuse in a looped transformer is an untested extension.

## First falsifier
On Qwen3-0.6B at 4K context over 16 calibration sequences, head-averaged (paper's p_t definition, p.4) top-256 index overlap between adjacent layers averaging below 0.5 (paper's DSA regime 0.7-1.0, App. A) kills the idea before any search; overlap above 0.5 does not confirm it, since App. A/C say overlap is a local metric that does not pick the pattern.

## Cheapest test on our iron
local-town (local-town GPU 8 GB, torch venv): Qwen3-0.6B bf16 with SDPA plus a hooked chunked q·kT per layer producing a head-averaged top-256 mask that can be substituted by the nearest F layer's cached mask — 28 forwards over 16x4K for the 28x28 overlap matrix (minutes), then greedy F->S to K=21 (357 batch loss evaluations x 16 sequences of 4K, budget ~2-4 h at a rough ~1 s per 4K forward, measure one forward first and rescale), $0; report PPL searched vs uniform at 1/2 and 1/4 retention (no swarm-box tok/s claim possible without a gather kernel).

## Numbers (quoted in the digest)
- k=2048 selected tokens per query (p.3-4)
- indexer latency share 30B DSA: 27% @10K, 81% prefill / 68% decode @200K (Fig. p.2)
- adjacent-layer top-k overlap=0.7-1.0; early/late corners <=0.4; 768 samples x 200K (App. A p.16)
- model=30B-A3B MoE, MLA, 47 layers (GLM-4.7-Flash base); GLM-5=744B/40B active (p.7, p.10)
- greedy search cost=N(N-1)/2 forward passes full sweep (p.5)
- calibration batch=768 @200K context (p.7); training-aware=1,000 dense warm-up + 4,000 sparse steps (p.7)
- prefill s @200K: DSA 19.5 / 1/2 13.7 / 1/4 10.7 (Table 1)
- decode per-request tok/s @200K: 58.0 / 73.0 / 86.0 (Table 1); @10K: 73.5 / 84.5 / 91.0
- decode full-KV tok/s @200K: 197 / 253 / 297 (Table 1)
- speedup: prefill 1.82x @200K, 1.27x @10K; decode 1.48x; full-KV +22-51% (p.8)
- training-free Long Avg: orig 50.2; 1/2 unif 47.4, search 50.3; 1/4 unif 43.0, search 49.9; 1/8 unif 35.3, search 46.1 (Table 2)
- G&R Avg stays 73.7-74.9 vs 74.6 for all but 1/8 uniform (70.0) (Table 2)

## Provenance
Ingestion 2026-09-16 on the owner's GO ("idea is exactly the node type meant for deeper research"): reader → adversarial critic (corrected seed) → this node. Hypotheses hang from here.
What is the concept? `scale:` big (new chain) or small (extension)?
