---
id: idea:lm-kv-bytes-ledger-q4-cache
mint_id: fa319016535e4378853a2934e47a560e
type: idea
parents:
  - goal:g14.6
next_edges: []
edited_by: thought-master
scaffold_hash: cd059c7373cb095e
season: 2
tags:
  - local-maxxing
  - treasury
title: "q4_0 KV on the swarm box: does halving KV bytes move Qwen3-0.6B tok/s at 4-8K context?"
town: local-maxxing
---
# idea:lm-kv-bytes-ledger-q4-cache

## Source
doc:deepseek-v4-1-flash — "DeepSeek-V4.1-Flash: Pushing the Limits of KV Cache Compression" (https://www.alphaxiv.org/abs/2609.deepseek-v4-1-flash); digest `.agi/context/local-maxxing/papers/deepseek-v4-1-flash.md`; critic grounded=4/5 — Abs-page numbers hold (890 B/token, 1/4, 1/8, 552B, 16B/8B, 45T, 67.1->76.3, ~2.5x confirmed in author bytes); two 'confirmed' numbers trace to alphaxiv's generated overview; five figures are PDF-only and unverified this pass; the seed's lever is the town's bandwidth hypothesis wearing the paper's FP4 label, its gguf arithmetic checks out on the box, its iron claim (no int8 dot) is wrong (asimddp present), and the test is runnable as written.

## Lever
The source demonstrates only that 4-bit main-KV storage is viable after QAT (global KV 890 B/token, ~1/4 of V4-Flash, abstract) and publishes no throughput number; on the swarm box llama.cpp -ctk/-ctv q4_0 cuts Qwen3-0.6B KV read per decode token at depth 4096 from ~470 MB (f16; 28 x 8 x 128 x 2 values/token per gguf header) to ~132 MB against a 0.64 GB Q8_0 weight read, so the town's own bandwidth ledger — not the paper — bounds the gain at <=1.44x tg at depth 4096 (1.24x at 2048, 1.75x at 8192) and ~1.0x at depth 0, with attention compute (~0.94 GFLOP/token at 4096 vs ~1.2 GFLOP weight matmul) as the reason it may come in lower.

## What it buys the town
If q4_0 tg is >= 1.2x f16 tg at depth 4096, every agent-length (4-8K) decode on the swarm box gets 1.2-1.7x for one flag with zero training, and H3 is answered positive — KV bytes bind on this iron, which licenses the cross-layer KV reuse (T2) and 1-bit-KV-floor threads as bandwidth plays; a null answers H3 negative and redirects effort to loop-count-as-effort (T9) and SWA bounded replay (T5).

## First falsifier
On the swarm box, /home/ubuntu/src/llama.cpp/build/bin/llama-bench -m ~/.cache/lm-models/Qwen3-0.6B-Q8_0.gguf -fa 1 -d 4096 -ctk f16,q8_0,q4_0 -ctv f16,q8_0,q4_0 -r 3: if q4_0 tg < 1.2x f16 tg at depth 4096, or depth-0 tg falls under q4_0, KV bytes are not the bottleneck at this context and the lever is dead (SDOT is present on this arm64, so a dequant-cost loss would be a measured fact, not the pre-judged one).

## Cheapest test on our iron
One llama-bench sweep on the swarm box (arm-cloud 4c, 23 GB, models and binary already on disk): 3 KV types x depths 0/2048/4096/8192 x 3 reps on Qwen3-0.6B-Q8_0, then one Qwen3.5-4B-Q4_K_M point at depth 4096 after checking the qwen35 header for which blocks carry full-attention KV; $0, no GPU, no training, wall-clock unmeasured but under an hour by prefill-token count.

## Numbers (quoted in the digest)
- global KV footprint=890 bytes/token (abstract; abs page, confirmed 2026-09-16)
- global KV vs V4-Flash=~1/4 / 4-fold; vs V1=437-fold (abs page summary, confirmed 2026-09-16)
- params vs V4-Pro-Base=~1/3 total, ~1/4 activated (abs page summary, confirmed 2026-09-16)
- backbone params=552B; active=16B decode / 8B prefill (abstract + existing digest §4.2.1)
- persistent KV vs V4-Flash=~1/8 (existing digest §3.1, paper §3.2.1)
- FP4 main KV vs FP8="nearly halves the storage footprint" (existing digest T4, paper §2.4.4)
- decode FLOPs growth over 256x context (4K->1M)=+1/4 (existing digest §3.2, paper Fig. 2)
- effort 25->100 avg Pass@1=67.1%->76.3% at ~2.5x tokens (existing digest T9, paper Table 2)
- Qwen3-0.6B f16 KV=112 KB/token, ~470 MB read/token at depth 4096 vs ~0.64 GB Q8_0 weights [ESTIMATE from public geometry, appended seed]
- predicted tg gain q4_0 KV at depth 4096=~1.4x if purely bandwidth-bound [ESTIMATE, appended seed]

## Provenance
Ingestion 2026-09-16 on the owner's GO ("idea is exactly the node type meant for deeper research"): reader → adversarial critic (corrected seed) → this node. Hypotheses hang from here.
What is the concept? `scale:` big (new chain) or small (extension)?
