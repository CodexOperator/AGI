---
id: idea:lm-kda-constant-state-kv-bytes
mint_id: 80c7345ea2de428cbe0b600f06243e9e
type: idea
parents:
  - goal:g5.5
next_edges: []
edited_by: belam
scaffold_hash: 7c8fabec3f2c0e02
season: 2
tags:
  - local-maxxing
  - treasury
thought_session: dissolve-legacy-2026-09-19
title: 3:1 KDA:MLA hybrid to hold per-token sequence-mixing bytes flat on bandwidth-bound decode
town: local-maxxing
---
# idea:lm-kda-constant-state-kv-bytes

## Source
doc:arxiv-2607-24653 — "Kimi K3: Open Frontier Intelligence" (https://arxiv.org/abs/2607.24653); digest `.agi/context/local-maxxing/papers/arxiv-2607-24653.md`; critic grounded=4/5 — All digest numbers trace to the PDF text (Table 1, §2.1.1, §2.2, §2.3, §3.2-3.4, §4.1.4, §5.4, §6.4, Table 5, §7) and the nano-kpu README; defects are three reader mechanisms (8-bit substrate, fixed-point argument, decode saving as demonstrated) leaking in as the source's, a [58]-cited N~=8, and a falsifier that cannot tell KV bytes from attention FLOPs on a 4-core CPU — tightened with a q8_0-KV control; BF16-only tile trick does not port to the Turing card.

## Lever
In 3 of every 4 attention layers a KDA-style fixed dk x dv recurrent state per head (log-decay bounded at g_min = -5, alpha > e^-5) replaces the KV cache, so those layers' per-decode-step bytes stop growing with context — K3 deploys this at 69 KDA + 24 MLA layers but never measures the decode saving, so the town must.

## What it buys the town
A kid-sized looped transformer trained on local-town whose decode bytes/token on the swarm box stay at (weights + constant state + 1/4 of the KV) at 8K-32K context instead of (weights + ctx x full KV), if and only if the falsifier shows KV bytes, not attention FLOPs, are what the town's 0.6B-4B decode loses at depth.

## First falsifier
On the swarm box, llama-bench Qwen3-0.6B Q8_0 tg at depths 256/2048/8192 with f16 KV and again with -ctk q8_0 -ctv q8_0: if tg at 8192 is within 10% of tg at 256, or if halving KV bytes moves tg at 8192 by under 10% while tg still drops, KV bytes are not the town's decode cost and the lever buys nothing at the contexts the town runs.

## Cheapest test on our iron
Swarm box (arm-cloud 4c, no GPU): `llama-bench -m qwen3-0.6b-q8_0.gguf -p 0 -n 64 -d 256,2048,8192` twice (default f16 KV, then `-ctk q8_0 -ctv q8_0 -fa 1`), ~20 min wall-clock, $0; only if the byte attribution survives, a ~20M-param 4-layer plain-vs-3:1 gated-delta+NoPE-softmax pair on local-town (gpu-8gS, chunkwise path in FP32 since Turing has no BF16), matched tokens, ~3-4 GPU-hours, $0.

## Numbers (quoted in the digest)
- total_params=2.8T (2.78T), activated=104B (104.2B), context=1M (abstract; Table 1)
- layers=93 vs K2 61; hidden=7,168; heads=96; routed_experts=896; active=16; shared=2; latent_moe_dim=3584; expert_hidden=3,072; vocab=160K (Table 1)
- attention_layers=69 KDA + 24 MLA, 3:1 per block plus one final MLA (Table 1; §2.1)
- kda_gmin=-5; alpha > e^-5 ~= 6.7e-3; 16-token tile log-decay in (-80,0); reciprocal < e^80 in BF16 range (§2.1.1)
- attnres_blocks=8 x 12 layers (9 with embedding); overhead O(Ld)->O(Nd) (§2.2)
- moe_sparsity=56; SiTU-GLU beta1=4, beta2=25, |f(x)| <= 100 (§2.3, Fig. 4)
- quantile_balancing comm cost=a few hundred histogram bins per expert (§2.3.3)
- scaling_efficiency_gain=~2.5x vs Kimi K2, OOD val loss vs FLOPs (abstract; §3.2 Fig. 7)
- schedule=cosine + 1% warmup, wd=0.1; ctx 8K->64K pretrain, 256K->1M cooldown (§3.3-3.4)
- vit=401M, 27 layers, patch 14; 2x2 pixel-shuffle = 4x fewer visual tokens (Table 1; §2.4)
- deployment: experts MXFP4, activations MXFP8, QAT over SFT+RL; draft unrolled 7 steps, LK loss, features from AttnRes blocks 1/4/final (§4.1.4)
- prefix cache: 512-token hash blocks inside 6144-token physical blocks; example hit B=2560=5x512 (§5.4.1)

## Provenance
Ingestion 2026-09-16 on the owner's GO ("idea is exactly the node type meant for deeper research"): reader → adversarial critic (corrected seed) → this node. Hypotheses hang from here.
What is the concept? `scale:` big (new chain) or small (extension)?
