---
id: idea:lm-eagle3-head-per-byte
mint_id: 8362bfbd9a524bbbb750a56b0de41186
type: idea
parents:
  - goal:g14.6
next_edges: []
edited_by: thought-master
scaffold_hash: 47c98c84704e2888
season: 2
tags:
  - local-maxxing
  - treasury
title: "EAGLE-3 head on Qwen3.5-4B: 233 MB draft steps amortise a 2.74 GB target read"
town: local-maxxing
---
# idea:lm-eagle3-head-per-byte

## Source
doc:baseten-eagle3-heads — "How to train custom EAGLE-3 heads for speculative decoding" (https://www.baseten.co/blog/how-to-train-custom-eagle-3-heads-for-speculative-decoding/); digest `.agi/context/local-maxxing/papers/baseten-eagle3-heads.md`; critic grounded=3/5 — Blog quotes all verified byte-for-byte; every error is town-side: test not runnable (Qwen3-0.6B vocab 151936 vs resident Qwen3.5-4B 248320, llama.cpp max diff 128; --draft-max removed; no llama-speculative), 4B arithmetic done for Qwen3-4B not the box's Qwen3.5-4B, looped/E3 ties are reader's not source's; a ready EAGLE-3 head for Qwen3.5-4B (233M params, card: 2.76 accept / 1.91x at 3 steps on 1 GPU) plus the local llama.cpp draft-eagle3 support make a zero-training CPU test possible this week.

## Lever
An EAGLE-3 head for the resident target (yuyijiong/Qwen3.5-4B-Eagle3: 1 layer + 50k-vocab lm_head, 233M params, ~233 MB at Q8 = 8.5% of the 2.74 GB Qwen3.5-4B Q4_K_M) reads three target hidden states and drafts 3 tokens verified in one batched target pass, cutting bytes touched per emitted token by the accept length (card, 1 GPU, temp 0, 3 steps: 2.76 accepted / 1.91x; blog on Qwen3-4B: 1.5-2.5x, memory-bound single-batch).

## What it buys the town
If a 4-token verify batch on the 4-core box costs near one token's bandwidth, the 6.9 tok/s Qwen3.5-4B kid runs ~1.5-1.9x faster with byte-identical greedy output, no training and no new engine code (existing llama.cpp 093a2f8, --spec-type draft-eagle3); the blog's recipe (target-regenerated data, TTT 7-9, LR 1e-4) becomes the template for a town-trained head only if that number holds.

## First falsifier
llama-bench on the swarm box, Qwen3.5-4B Q4_K_M, 4 threads, a 4-5-token batch forward vs a single-token step: if the batch costs >= ~2.5x the step, verify is compute-bound here and no drafter at any acceptance reaches 1.5x — five minutes, $0, before any download.

## Cheapest test on our iron
Swarm box: download the 466 MB head + Qwen/Qwen3.5-4B config/tokenizer, convert_hf_to_gguf.py --target-model-dir, then llama-server -m Qwen3.5-4B-Q4_K_M.gguf -md <head>.gguf --spec-type draft-eagle3 --spec-draft-n-max 3 vs --spec-type none vs draft-simple with Qwen3.5-0.8B Q8_0 over 20 kid-transcript prompts at temperature 0, reporting tok/s, accept length, RSS and output byte-identity; ~2 h wall-clock, $0.

## Numbers (quoted in the digest)
- head_size=1 decoder layer, 1-5% of target params (blog, What is EAGLE-3?)
- production_latency_improvement=1.5-2.5x on Qwen3-4B (blog, intro/Evaluation/Conclusion)
- paper_claimed_speedup=4-6x, discounted as serving-framework (blog, What is EAGLE-3?)
- ttt_length=7-9 (blog, TTT-length)
- num_draft_tokens=3-4 at inference; 8 rarely helps (blog, Number of draft tokens)
- lr=1e-4 (~3-7B) / 5e-5 (~7-20B) / 2e-5 (20B+), AdamW (blog, LR table)
- temperature=1 vs 0 speedup loss=15-25% (blog, Sampling parameters)
- dataset_generic=200k-300k samples (<=~20B), ~500k (large); dataset_specialized=~100k; tokens_per_sample=1k-2k (blog, dataset table)
- training_accuracy_plateau=70-80%; loss drop in first 10-20% of steps (blog, Step 4)
- training_hours=NOT GIVEN; hardware=NOT GIVEN; acceptance_length=NOT GIVEN; head_param_count=NOT GIVEN (grep of HTML)
- town arithmetic: Qwen3-0.6B one layer=~15.7M params (2.6%), LM head=155.6M; Qwen3-4B one layer=~100.9M (2.5%), LM head=389M (HF config.json)
- town arithmetic: 0.6B Q8 draft step ~172 MB full-vocab (29% of ~600 MB target step) or ~49 MB with a 32k draft vocab

## Provenance
Ingestion 2026-09-16 on the owner's GO ("idea is exactly the node type meant for deeper research"): reader → adversarial critic (corrected seed) → this node. Hypotheses hang from here.
What is the concept? `scale:` big (new chain) or small (extension)?
