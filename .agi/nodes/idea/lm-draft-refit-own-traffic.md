---
id: idea:lm-draft-refit-own-traffic
mint_id: 3f6ffb60848b449fac862b7048f5b8ab
type: idea
parents:
  - goal:g5.5
next_edges: []
edited_by: belam
scaffold_hash: 141aa815e47aeadb
season: 2
tags:
  - local-maxxing
  - treasury
thought_session: dissolve-legacy-2026-09-19
title: Refit a small draft on target-regenerated town prompts; measure accept rate with llama.cpp speculation
town: local-maxxing
---
# idea:lm-draft-refit-own-traffic

## Source
doc:baseten-live-draft — "Live draft model training for speculative decoding" (https://www.baseten.co/blog/live-draft-model-training-for-speculative-decoding/); digest `.agi/context/local-maxxing/papers/baseten-live-draft.md`; critic grounded=4/5 — Source half fully grounded (all quotes/numbers byte-match; NOT-GIVEN list confirmed by grep, engine is proprietary, no open engine named); every error is reader-side arithmetic or mechanism gloss in the idea seed; corrected seed drops live/EAGLE-3/SGLang/CPU-refit packaging for an offline SFT refit gated on H7.

## Lever
A draft adapted to the served traffic distribution accepts more (blog: median +20% in its accept metric on Baseten production traffic, 100%+ on an undefined 'constrained' tail), raising accepted tokens per target verify pass and so dividing the target's bytes-per-token (Qwen3.5-4B Q4_K_M, the swarm box's 6.9 tok/s resident) by a larger number for no change to the target's bytes; at the town's volume the adaptation is an offline SFT on stored transcripts, since the blog's reasons for 'live' (2 GB samples, millions of them, ZDR) do not apply.

## What it buys the town
If H7 first shows static draft-model speculation clears 1.1x on the swarm box, the town keeps a same-vocab small Qwen draft (Qwen3.5-0.8B per H7, or Qwen3-0.6B if vocab-compatible) refit periodically on local-town (0.6-0.8B bf16 fits the local-town GPU's 8 GB) from prompts the 4B target regenerated, and every kid/parent decode on the swarm box gets whatever fraction of the blog's +20% accept gain survives on our traffic, measured, not assumed.

## First falsifier
On 200 held-out target-regenerated town prompts at temperature 0, per-position acceptance rate with the SFT-refit draft rises less than +10% relative over the stock draft (or H7's static speculation is already <= 1.1x tok/s on the swarm box, so no acceptance gain can pay for the draft's bytes).

## Cheapest test on our iron
local-town: regenerate ~1k town kid prompts with Qwen3.5-4B Q4_K_M via llama.cpp CUDA, LoRA-SFT the same-vocab small Qwen draft on that text for one epoch (bf16, torch venv), then run llama-speculative on local-town with stock vs refit draft over 200 held-out prompts logging acceptance rate, and confirm tok/s on the swarm box for 20 prompts; ~3-4 h wall-clock (ESTIMATE, unmeasured), $0.

## Numbers (quoted in the digest)
- median_accept_rate_increase=+20% live vs static draft (meta description + body para 3)
- constrained_traffic_increase=100%+ (body: 'accept rate' in para 3, 'accept length' at close of 'Eliminating traditional bottlenecks')
- static_draft_baseline=2-3x higher throughput, EAGLE-3/DFlash (body para 1)
- hidden_state_sample_size=>2GB per sample on Kimi K2, 'millions of them' needed (body, 'Storage overhead')
- memory_overhead_scaling=proportional to max_num_tokens_per_iter, not max_sequence_length (body, inference + training path)
- cluster_scale='tens or hundreds of nodes' (body, Trio paragraph)
- transport=UCXX RDMA; buffering=CUDA-IPC double buffer -> mmap pageable memory (figure caption + tools section)
- date_published=2026-06-25 (datePublished JSON-LD)
- refresh_cadence=NOT GIVEN; training_hours=NOT GIVEN; training_hardware=NOT GIVEN; draft_size=NOT GIVEN; tokens/s_delta=NOT GIVEN; CPU_training=NOT MENTIONED (grep of the 312,043-byte HTML)

## Provenance
Ingestion 2026-09-16 on the owner's GO ("idea is exactly the node type meant for deeper research"): reader → adversarial critic (corrected seed) → this node. Hypotheses hang from here.
What is the concept? `scale:` big (new chain) or small (extension)?

## Agent Notes
OWNER 2026-09-18 06:48Z (thought-master pane), verbatim: "Do we already have papers on efficient decode training? Where we do a few rounds of encoder training, then it reaches equilibrium, then we freeze that and train decoder only till it catches up." ANSWER FROM THE TREASURY (thought-master): the frozen-trunk + trainable-small-part half exists in five digests -- Uno 2609.04010 (AR frozen, diffusion LoRA distilled until it catches up), C2C 2510.03215 (both LLMs frozen, fuser trained), EAGLE-3 / Baseten live-draft + OSD 2310.07177 (draft head post-hoc, backbone frozen; online distillation = this idea), DeepSeek V4.1-Flash DSA indexer warm-up (base frozen, 1,000 steps), the recurrent looped transformer (frozen deep path verifies a shallow proposal). NOT in the treasury: the staged encoder-first recipe (train encoder to a plateau -> freeze -> decoder-only until it catches up) as a paper; survey slice launched 06:48Z (troves/2026-09-18-owner-papers/staged-freeze-training.md) to find it with URLs (candidates to check: LiT locked-image tuning, FreezeOut / progressive freezing, encoder-frozen seq2seq, DEQ if equilibrium is literal). Town application if found: train the kid-tier draft head / the oscillator readout with the trunk frozen -- the shape this idea already has.

JUDGED BY HAND (thought-master 10:3xZ; the trove-survey critic/panel/judge stages did not run: critique timed out at 1200 s, SM.112 memory cap pending): the staged-freeze literature slice (troves/2026-09-18-owner-papers/README-ranked-table.md + 9 digests, read stage only, MEASURED tags honoured) answers the owner 06:48Z question: NO paper gives the exact staged recipe (train the encoder to a plateau -> freeze it -> train the decoder alone until it catches up) for an LLM. What EXISTS with recipe + number: Medusa-1 (2401.10774: heads only on a FROZEN backbone, 2.2-3.6x lossless, Apache-2.0), EAGLE-3 (2503.01840: frozen target, 1-layer drafter, multi-layer feature fusion, up to 6.5x, SpecForge harness, published Qwen2.5 heads), DSpark (2607.05147: parallel backbone + Markov head + confidence head on a frozen target), DeepSeek-V3.2-Exp warm-up (freeze ALL but the indexer, 1000 steps, 2.1B tokens, LR 1e-3, KL to attention scores, then unfreeze all; V4.1-Flash later dropped the warm-up), FreezeOut (1706.04983: the progressive-freeze schedule, 20 percent wall-clock), LiT (2111.07991: locked trunk + trained readout, vision), FailFast (2512.20573: off-the-shelf dLLM drafter, no training, 1.7x over EAGLE-3). DEQ is a different sense of equilibrium (fixed point), not a plateau. OPEN (nobody has it): a coupled-oscillator readout or an SNN C2C fuser trained against a frozen LLM trunk. Consequence: the first frozen-trunk decode-side training hypothesis is minted from Medusa-1/EAGLE-3 (recipe + number exist): hypothesis:lm-eagle3-drafter-on-frozen-qwen3-4b -- it measures the catch-up curve itself (steps to 90 percent of final acceptance length), which is the number the owner asked about.
