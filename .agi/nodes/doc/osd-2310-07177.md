---
id: doc:osd-2310-07177
mint_id: 4b1e103c570c4cfdb3d32908b52bd331
type: doc
parents:
  - goal:g5.29
next_edges: []
edited_by: thought-master
link_ref: .agi/context/local-maxxing/papers/osd-2310-07177.md
scaffold_hash: 6ef3cdd2b82dee68
season: 2
tags:
  - local-maxxing
  - treasury
  - ingestion
title: "\"Online Speculative Decoding\""
town: local-maxxing
---
# doc:osd-2310-07177

**Source:** https://arxiv.org/abs/2310.07177
**Digest (link_ref):** `.agi/context/local-maxxing/papers/osd-2310-07177.md` — read + adversarially critiqued 2026-09-16 (workflow wf_92672d0f-312; critic grounded=4/5).
**Critic note:** Digest is faithful to v2 (every paper number traces to bytes); the idea seed breaks on the iron — Qwen3-0.6B cannot draft for Qwen3.5-4B in llama.cpp (vocab 151,936 vs 248,320, tolerance 128), llama-speculative is not built, and v4 replaced the 3.06x headline with measured 1.42-2.17x; corrected to the same-vocab Qwen3.5-0.8B draft via llama-server -md.
**Seeds:** idea:lm-online-draft-distillation-cpu-split

## Relevance to local-maxxing
Speculative decoding is the direct lever for the swarm box's bandwidth-bound regime — each accepted draft token swaps a full target weight sweep for a draft sweep — and OSD makes the governing scalar α purchasable online at 1/12-1/19 of the target's FLOPs from logits the verify pass computes anyway. The owner's CPU angle is only half-supported: the paper's spare FLOPs are idle GPU tensor cores, its one nod to heterogeneity is 'executed concurrently on separate devices' (A.2), and on the A1 a draft backward pass competes for the same memory bus as decode, so the clean split is target decode on one box and the every-8-requests trainer on local-town fed by a logits byte-stream. For the looped transformer the shallow unroll is the natural draft and the deep unroll the target, with OSD's replay buffer of (error index, target logits) as the free supervision stream; the same buffer grades any cheap proposer (LUT cascade, oscillator ensemble) by one scalar α, and the town's narrow kid traffic is the 'relatively simple' query distribution the paper says a tiny draft learns in under 2K records.
