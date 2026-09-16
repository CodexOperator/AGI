---
id: doc:deepseek-v4-1-flash
mint_id: 5d778b6aeaed46e3b15c02136b208626
type: doc
parents:
  - goal:g14
next_edges: []
edited_by: thought-master
link_ref: .agi/context/local-maxxing/papers/deepseek-v4-1-flash.md
scaffold_hash: 6151684256388732
season: 2
tags:
  - local-maxxing
  - treasury
  - ingestion
title: "\"DeepSeek-V4.1-Flash: Pushing the Limits of KV Cache Compression\""
town: local-maxxing
---
# doc:deepseek-v4-1-flash

**Source:** https://www.alphaxiv.org/abs/2609.deepseek-v4-1-flash
**Digest (link_ref):** `.agi/context/local-maxxing/papers/deepseek-v4-1-flash.md` — read + adversarially critiqued 2026-09-16 (workflow wf_92672d0f-312; critic grounded=4/5).
**Critic note:** Abs-page numbers hold (890 B/token, 1/4, 1/8, 552B, 16B/8B, 45T, 67.1->76.3, ~2.5x confirmed in author bytes); two 'confirmed' numbers trace to alphaxiv's generated overview; five figures are PDF-only and unverified this pass; the seed's lever is the town's bandwidth hypothesis wearing the paper's FP4 label, its gguf arithmetic checks out on the box, its iron claim (no int8 dot) is wrong (asimddp present), and the test is runnable as written.
**Seeds:** idea:lm-kv-bytes-ledger-q4-cache

## Relevance to local-maxxing
The paper's entire prize is KV bytes per token, and the town grades every lever as bytes-touched-per-token on a bandwidth-bound CPU; whether those are the same ledger at <=8K context on the swarm box is the unrun gating measurement (existing digest H3), and the appended seed sizes it: at depth 4,096 Qwen3-0.6B's f16 KV (~470 MB/token) is already ~40% of bytes touched next to ~0.64 GB of Q8_0 weights, so FP4-class KV (llama.cpp q4_0 cache) predicts ~1.4x tg with zero training. For the flip/SNN thread it sets a bound rather than a claim: the ladder f16 -> q8_0 -> q4_0 -> 1-bit sign-K is monotone in bytes, so the q4_0 point bounds what any bit-flip KV can buy on this iron, and the paper's own warning (SWA KV kept FP8 as quantization-sensitive) is the quality cliff to expect before 1 bit. For the looped transformer the best-fit bridges remain loop-count-as-effort (T9) and looping as unbounded cross-layer KV reuse (T2), both already seeded in the existing digest §6.
