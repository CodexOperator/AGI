---
id: idea:lm-searched-swa-pattern-zero-train
mint_id: 3fb121025ee2488cbb342eff5d9a3bed
type: idea
parents:
  - goal:g14.6
next_edges: []
edited_by: thought-master
scaffold_hash: f935e715497d1822
season: 2
tags:
  - local-maxxing
  - treasury
title: Greedy-search a per-layer sliding-window pattern on Qwen3-0.6B, no training, to cut KV bytes/token
town: local-maxxing
---
# idea:lm-searched-swa-pattern-zero-train

## Source
doc:glm-5-3-flash — "GLM-5.3-Flash: More Intelligence with Less Compute" (https://autoclaw.z.ai/blog/model/glm-5.3-flash/); digest `.agi/context/local-maxxing/papers/glm-5-3-flash.md`; critic grounded=4/5 — Digest numbers all trace to fetched bytes (blog, HF card, config.json, GLM-5 report Tables 2/4/5/6/10); one summary gloss is wrong (Table 6 32K drop is 2.87, not ~1.3) and the idea's 37%/3-6h/12-step figures are reader arithmetic on the wrong model — corrected to Qwen3-0.6B with a pruned search; critique appended to the digest.

## Lever
Convert a searched half of the layers to a 2K sliding window (GLM-5 report Table 4: searched 1:1 SWA pattern with a 4096 window keeps RULER@16K 88.92 vs 92.01 full while naive alternation collapses to 25.89, zero training) so windowed layers read a fixed 2K-entry KV ring buffer per decoded token instead of the whole context — a derived 0.625x of full KV bytes read at a 1:4 window:context ratio, to be measured, since the source reports accuracy only.

## What it buys the town
On the swarm box, where Qwen3-0.6B's f16 KV (114,688 B/token, ~940 MB at 8K) outgrows the ~0.6 GB Q8 weight read near 5K tokens, a runtime-only decode-bandwidth win for long-context kids, plus a per-layer 'windowable' map that can be scored against D1's per-layer mean-ablation ranking.

## First falsifier
On Qwen3-0.6B bf16 at 8K context with half the layers windowed at 2K, if no greedy/beam-2 searched pattern stays within 5 RULER-lite points of full attention at 8K while the alternating pattern collapses, the layer-selection lever does not exist at 0.6B and the idea dies.

## Cheapest test on our iron
local-town (gpu-8g): HF transformers SDPA with a per-layer window mask on Qwen3-0.6B bf16 at 8K, ~20 RULER-lite prompts per candidate, one layer per step seeded by D1's per-layer ranking (greedy or beam 2, ~200-400 candidate evals, single-digit GPU hours, $0); then measure tg tok/s at 8K on the swarm box with a real per-layer ring-buffer KV (llama.cpp per-layer SWA path or a patched cache), not a mask.

## Numbers (quoted in the digest)
- total_params=320B, active_params=18B (blog para 1; HF card)
- layers=45 vs GLM-4.5 92; active 18B vs 32B (blog, Architecture for Efficient Inference)
- attention_compute_reduction_vs_GLM-5.3=3.0x; KV_cache_reduction_vs_GLM-5.3=4.4x (blog, same section)
- pretrain_corpus=30T tokens (blog; HF card)
- serving_e2e_speedup=3x vs own initial baseline on same hardware (blog, Serving at Scale)
- IndexPool=4 keys->1; config index_kpool=4, index_topk=2048, index_n_heads=32, index_head_dim=128 (blog + config.json)
- layer_types=34 linear_attention + 11 deepseek_sparse_attention at indices 3,7,...,43; mlp=3 dense + 42 MoE (config.json)
- MoE: n_routed_experts=288, num_experts_per_tok=8, n_shared_experts=1, moe_intermediate_size=2048, hidden_size=4096, vocab=154880, max_position_embeddings=1048576 (config.json)
- mHC: hc_mult=4, hc_sinkhorn_iters=20 (config.json)
- weights FP8 e4m3, weight_block_size [128,128], 1,509 modules unquantized incl. hyper_connection/lm_head/embed_tokens (config.json quantization_config)
- Terminal Bench 2.1=84.3 vs GLM-5.2 81.0; DeepSWE v1.1=63.4 vs 46.2; NL2Repo=56.3 vs 48.9; Toolathlon Verified=78.4 vs 59.9; AutomationBench v1.0.6=48.8 vs 26.2; Agents' Last Exam=26.3 vs 20.4; HLE with Tools=55.3 vs 54.7; GDPval-AA v2=1773 vs 1504 (blog table)
- OfficeQA Pro=62.4; CharXiv Reasoning w/ Tools=89.4; Chartography w/ Tools=78.0; BabyVision=53.4; MVBench=77.8; MMVU=80.5 (blog table)

## Provenance
Ingestion 2026-09-16 on the owner's GO ("idea is exactly the node type meant for deeper research"): reader → adversarial critic (corrected seed) → this node. Hypotheses hang from here.
What is the concept? `scale:` big (new chain) or small (extension)?
