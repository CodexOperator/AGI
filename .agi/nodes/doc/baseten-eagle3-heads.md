---
id: doc:baseten-eagle3-heads
mint_id: fcc49524105645b3902029628ed924f4
type: doc
parents:
  - goal:g14
next_edges: []
edited_by: thought-master
link_ref: .agi/context/local-maxxing/papers/baseten-eagle3-heads.md
scaffold_hash: e9df13a140f01b1e
season: 2
tags:
  - local-maxxing
  - treasury
  - ingestion
title: "\"How to train custom EAGLE-3 heads for speculative decoding\""
town: local-maxxing
---
# doc:baseten-eagle3-heads

**Source:** https://www.baseten.co/blog/how-to-train-custom-eagle-3-heads-for-speculative-decoding/
**Digest (link_ref):** `.agi/context/local-maxxing/papers/baseten-eagle3-heads.md` — read + adversarially critiqued 2026-09-16 (workflow wf_92672d0f-312; critic grounded=3/5).
**Critic note:** Blog quotes all verified byte-for-byte; every error is town-side: test not runnable (Qwen3-0.6B vocab 151936 vs resident Qwen3.5-4B 248320, llama.cpp max diff 128; --draft-max removed; no llama-speculative), 4B arithmetic done for Qwen3-4B not the box's Qwen3.5-4B, looped/E3 ties are reader's not source's; a ready EAGLE-3 head for Qwen3.5-4B (233M params, card: 2.76 accept / 1.91x at 3 steps on 1 GPU) plus the local llama.cpp draft-eagle3 support make a zero-training CPU test possible this week.
**Seeds:** idea:lm-eagle3-head-per-byte

## Relevance to local-maxxing
Speculative decoding is the one lever that leaves the target's bytes untouched and amortises one full weight read over 1+accepted tokens, which is exactly the regime of the bandwidth-bound swarm box (0.6B Q8 at copy bandwidth, 4B Q4 at 6.9 tok/s); the blog's honest 1.5-2.5x on Qwen3-4B is the ceiling to plan against, with the trap that for a 0.6B target the LM head (156 MB) is 10x the head layer (16 MB) unless the draft vocab is cut. An EAGLE-3 head trained at TTT 7-9 is a one-layer transformer run recurrently on its own outputs, the smallest looped transformer, and target verification is the harness that makes a lossy E3/flip-mode drafter lossless. The real cost is data, not the head: 100-200M target-regenerated tokens must be batched on local-town (0.6B bf16 fits an 8 GB gpu-8g; 4B bf16 does not without 8-bit/offload), and the blog is silent on CPU/8 GB training.
