---
id: doc:lm-round0-table
mint_id: 6a1307eb9aad467ea23b099a1e9ad1c0
type: doc
parents:
  - goal:g14.3
next_edges: []
edited_by: thought-master
scaffold_hash: 6688a19ac6f37f60
season: 2
title: "Round 0 of the local-maxxing charter: the model (there is no qwen3.8-50b; the line is Qwen3.8-27B / Ternary Bonsai 2 27B), the Camber XS instance (1x L4 24 GB, 1.50 USD/h, billing granularity unpublished), and the arithmetic: the XS does not pay for kid inference (~16x deepseek-v4-flash per output token even at 8 slots); our 8 GB GPU has more bandwidth than the L4 for the ternary 27B"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# doc:lm-round0-table — Round 0 of the charter (§1.5 (a)-(c)): model · Camber XS · the arithmetic

Written by thought-master 2026-09-18 05:5xZ from the three read digests in `troves/2026-09-18-round0/` (MEASURED = quoted there with URL + date; ESTIMATE = arithmetic shown here). The survey's panel/judge stages never ran (pi 600 s wall until SM.105) — (c) is judged by hand.

## (a) The model — "qwen3.8 50b" does not exist (MEASURED, HF API 2026-09-18)
- Official Qwen3.8 = **27B dense** (hybrid attention: 16 full-attn + 48 linear-attn layers, 4 kv heads × 256 dim, ctx 262,144), **Flash-Next** (small experimental arch), **2.4T-A95B** (4.89 TB MoE). No 32B/50B/72B. Community-only `win10/Qwen3.8-45B-A30B` is a merge, not a candidate.
- The candidate line is therefore **Qwen3.8-27B** and its ternary child **Ternary-Bonsai-2-27B** (PrismML card: base Qwen/Qwen3.8-27B, 27.36B params, 98.2% of FP16 intelligence over 14 thinking-mode benchmarks, ~47 tok/s on a laptop-class GPU).
- Weights bytes (MEASURED file sizes): bf16 **55.6 GB** · FP8 **30.9 GB** · AWQ-INT4 **21.0 GB** · GGUF Q4_K_M **17.4** / UD-IQ4_XS 14.3 / UD-IQ3_XXS 10.9 / UD-IQ2_XXS 7.27 / UD-IQ1_S 6.19 · **Bonsai PTQ1_0 5.947 GB (1.75 bpw)** · Bonsai PQ2_0 7.206 GB (2.13 bpw). EXL3 repo holds no weights.
- KV at 8k, f16 (ESTIMATE from config): only the 16 full-attn layers grow → 64 KiB/token → **0.54 GB at 8k**; linear-attn state is constant-size. That is why the 27B fits small VRAM at all.
- Licence: Qwen3.8-27B card (Apache-2.0 lineage as Qwen3.5-35B-A3B is MEASURED Apache-2.0; the 3.8 card's licence line was not quoted by the reader — VERIFY before any redistribution). Tokenizer: Qwen (vocab 248,320).

## (b) Camber Cloud XS (MEASURED, docs.cambercloud.com/nodes-pricing, page dated 2025-09-25; compute page 2026-02-18)
| size | GPU | cores | RAM | USD/h |
|---|---|---|---|---|
| GPU **XSMALL** | **1× NVIDIA L4, 24 GB** (owner's 24 GB VERIFIED) | 8 | 32 GB | **1.50** (1 credit = 1 USD) |
| GPU MEDIUM | 4× L4 (96 GB) | 48 | 192 GB | 6.00 |
| CPU XSMALL (for a billing probe) | — | 8 | 32 GB | 0.32 |
- Billing: "credits are used while the job is RUNNING"; **granularity NOT published**; a community report (GitHub issue #43) of "6+ hours billed for ~10 minutes" (core-scaling) — the single biggest risk to a 3 GPU-h/month budget. Job-level SDK/CLI exists (`create_job(..., with_gpu=True)`, `camber job ... --gpu --size`), so one-shot jobs, never an interactive box. Spin-up: "within minutes" (no hard number; ESTIMATE 1-3 min). Disk, egress price, quotas, CUDA stack: not published on the pages read. 100 free credits on signup (an account exists: `CAMBER_CLOUD_API_KEY` is g14's gate) → the first trial hour may cost 0 USD. A separate HPC queue offers a T4 16 GB — a different product, do not conflate.

## (c) The arithmetic — USD per 1M OUTPUT tokens on one XS vs OpenRouter the same day (ESTIMATE; prices MEASURED 2026-09-18 05:21Z)
Decode is memory-bandwidth-bound: tok/s ≈ bandwidth / weight bytes × efficiency (0.5-0.6). L4 = 300 GB/s (public spec). Our GPU2070S = 448 GB/s, 8 GB. Batched slots share one weight read per step, so aggregate ≈ single × slots until compute-bound. Spin-up amortised at 2 min per session; session = 1 h or 6 h.

| candidate on ONE XS (24 GB) | fits? | est tok/s single / ×8 slots | USD per 1M out, 1-h / 6-h session (×8 slots) | same, single stream |
|---|---|---|---|---|
| Bonsai PTQ1_0 5.95 GB | yes (+0.54 GB KV/8k slot) | 25-30 / 150-200 | **~2.9 / ~2.8** | ~17 |
| Qwen3.8-27B Q4_K_M 17.4 GB | yes (4 slots at 8k) | 10-12 / ~40 (×4) | ~10.7 / ~10.4 | ~38 |
| Qwen3.5-9B Q8 ~10 GB | yes (many slots) | ~30 / ~200 | ~2.2 / ~2.1 | ~14 |
| 27B FP8 30.9 GB | **no** (needs MEDIUM 6 USD/h, 4× L4) | — | ~5.5 (MEDIUM, ×8) | — |
| 2× XS tensor-parallel | not needed — nothing in the line needs > 24 GB below FP8 | — | — | — |

OpenRouter the same day (USD per 1M output; input in brackets): **deepseek-v4-flash 0.177 (0.089)** · deepseek-v4-flash-0731 0.12 (0.06) · deepseek-v4.1-flash 0.60 (0.15), ×2 on weekdays 01-04Z and 06-10Z · qwen3.8-27b **2.55** (0.214) · qwen3.5-9b 0.15 (0.10) · qwen3.5-35b-a3b 1.30. Kid session shape 20k in / 5k out × 40 calls: flash 0.106 USD · qwen3.8-27b 0.68 USD · Bonsai on one XS ×8 kids ≈ 0.45 USD per kid-session (ESTIMATE).

**Break-even aggregate tok/s for the XS:** vs deepseek-v4-flash = 1.50 / 0.177 per 1M = **2,350 tok/s** (impossible for a 27B on an L4); vs hosted qwen3.8-27b = **163 tok/s** (reachable only at ≥ 8 parallel slots).

## Verdict (thought-master, by hand)
1. **Renting the XS for kid inference does not pay**: ~16× deepseek-v4-flash per output token even at 8 slots; parity with the hosted 27B only when ≥ 8 kids decode in parallel all hour. The rounds the owner named ("optimize it, quantize it, parallelize it") already run at 0 USD on GPU2070S, whose bandwidth (448 GB/s) beats the L4's (300 GB/s) for the ternary 27B that fits it — `hypothesis:lm-bonsai2-27b-kid-tier` (TM.30, live) is the measurement that decides the line, not a rental.
2. **What the XS is for**: VRAM headroom only — models > 8 GB at kid-quality (Q4 27B, 9B at long context), 8+ parallel slots (8 GB holds ~3 slots at 8k beside the 5.95 GB), and **training** (the banked kid-persona QLoRA). Job-level only.
3. **Before any GPU hour**: one 5-minute CPU-XSMALL job (0.03 USD) to observe the actual billing granularity on the account, given the core-hour overbilling report; then the 100 free credits cover the first real hour.
4. **Quality proxy that decides**: the 20-prompt kid-tier checklist the town already runs (task-shaped; `hypothesis:lm-bonsai2-27b-kid-tier` conjunct 3), with the card's 98.2%-of-FP16 as the prior — not perplexity.
5. **The name to use**: "qwen3.8 27b / Bonsai 2 27B" — there is no 50B; the 35B-A3B (Qwen3.5, MoE, Apache-2.0) is the other real candidate if a bigger total is wanted at ~3B active (fits 8 GB at Q4 ≈ 20 GB? no — 35B-A3B Q4 is ~20 GB, XS-only).

## Acceptance against the charter
(a) exact model + bytes + licence-to-verify: done · (b) XS instance quoted: done, granularity + disk + egress open · (c) rows with fits / tok/s / USD per 1M incl. spin-up over 1-h and 6-h vs deepseek-v4-flash the same day: done as ESTIMATE; the proven row is GPU2070S's, from TM.30 · (d) the looped-transformer chain: `doc:recurrent-looped-transformer` + `hypothesis:lm-oscillator-research-hunt` exist; not this doc's scope.

## Agent Notes
CORRECTED 22:3xZ 09-20 by ABC.01 (MEASURED, hypothesis:lm-bonsai2-27b-abc-coding-test-on-the-8gb-box): verdict 2 assumed ~3 slots at 8k beside the 5.95 GB PTQ1_0 on the 8 GB rig; at the 64K ctx line the 27B takes 7,268 MiB (64/64 layers, ~890 MiB headroom) = ONE stream at 23.0 tok/s (18.9 at 16.8K). Slot count on the rig is a ctx-line choice to be measured, not the free headroom the estimate implied. Bonsai row quality is now measured too: 86.6 pct HumanEval pass@1 vs the 9B's 78.0 pct. Cost table columns revised (abliterated?, Camber = training only, reference bar deepseek-v4.1-flash): goal:g14.3 note 22:3xZ.

thought-master 09:2xZ 09-21 CORRECTION #2 (SWR.02-B, measured): the arithmetic's 'batched slots share one weight read per step, so aggregate ≈ single × slots' does NOT hold for the ternary 27B on the 2070 SUPER -- decode is COMPUTE-bound there (20.5-23.0 tok/s flat across 1/2/4/8 slots), not bandwidth-bound; the ×8-slot USD-per-1M rows in (c) are therefore too optimistic for this model on this GPU (single-stream rows stand). The L4 rows were never measured; the same caveat applies until one is.
