---
id: goal:g5.19
mint_id: ae23bcd0a45f4d79a9dc2e683a56fe96
type: goal
parents:
  - goal:g5
next_edges: []
confidence: 0.6
edited_by: belam
goal_id: G5.19
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: ac0d34808df46c12
season: 2
seeds: []
status: active
tags:
  - goal
  - subgoal
thought_session: g1-g7-rewrite-2026-09-19
title: "G5.19: The Thought Master post (thought-master, Opus, a master modeled on stream-master, answers to the sanctuary-master; inference R+D = the local-maxxing town master) — charter section written by the SM: (a) verify the exact model FIRST (qwen3.8 50b: id, dense or MoE, weights size, licence) and the Camber Cloud XS instance (GPU, 24 GB VRAM, disk, network, price/h) — dense 50B at 4-bit is 25+ GB > 24 GB, so sub-4-bit / 2xXS parallel / MoE offload IS the research question; (b) the looped-transformer paper digested into an autoresearch-style hypothesis chain; (c) a cost/throughput table: tokens/s + USD per 1M on one XS per candidate quantization, spin-up included, vs OpenRouter deepseek-v4-flash; (d) cadence: ONE pi research round at a time, spend-capped, never ahead of the live loop. master-sensei drafts quorum/thought-master.md; the Prime seats it (spawn --name, --dry-run first) when brief + row are ready; director-thought seated LAZILY at the master first round (Prime assumption, flagged to the owner)"
town: core
---
<!-- BODY:BEGIN -->
# goal:g5.19

## Agent Notes
ROUND 0 DELIVERED (thought-master 05:54Z): doc:lm-round0-table -- (a) there is no qwen3.8-50b; the line is Qwen3.8-27B / Ternary Bonsai 2 27B (PTQ1_0 5.95 GB fits the 8 GB GPU with 0.54 GB KV at 8k, hybrid attention); (b) Camber XS = 1x L4 24 GB, 8 cores, 32 GB, 1.50 USD/h, billing granularity unpublished with a core-hour overbilling report, job-level SDK/CLI exists; (c) the XS does not pay for kid inference: ~2.8-2.9 USD per 1M output at 8 slots vs deepseek-v4-flash 0.177 (16x), parity with hosted qwen3.8-27b (2.55) only at >= 8 parallel kids; break-even 2,350 tok/s vs flash / 163 tok/s vs the hosted 27B; our GPU2070S (448 GB/s) beats the L4 (300 GB/s) for the ternary 27B. The XS is for VRAM headroom + training only; a 0.03 USD CPU job first to observe billing granularity; the 100 signup credits cover the first hour.

CHARTER TABLE REVISED 22:3xZ 09-20 (thought-master; every number on its node): (a) candidate line CONFIRMED = Qwen3.8-27B / Ternary Bonsai 2 27B -- ABC.01 (hypothesis:lm-bonsai2-27b-abc-coding-test-on-the-8gb-box, merge 79208601f) MEASURED the 8 GB row on the 2070 SUPER: 64/64 layers, 7,268 MiB at load, tg 23.0 tok/s empty / 18.9 at 16.8K ctx, 7.43 J/token; HumanEval pass@1 142/164 = 86.6 pct vs Qwen3.5-9B-Q4_K_M 128/164 = 78.0 pct (McNemar p = 0.0094) -- the bigger ternary beats the smaller 9B in the same 8 GB. Correction to doc:lm-round0-table verdict 2: at the 64K line the 27B leaves ~890 MiB = ONE stream, not 3 slots at 8k; parallel slots on the rig need a shorter ctx line, measured next time, never assumed. (b) Camber XS row CLOSED for kid inference (round-0 verdict 1 stands; re-quoted against the new reference bar deepseek-v4.1-flash at 0.60 USD per 1M out the break-even is 694 aggregate tok/s, still out of reach for a 27B on one L4) and OPENED for training by the owner 21:4xZ (verbatim on goal:g14: I'm fine with spending camber hours on it and failing it's fine since at least it can run parallel for fine tuning stuff or even more RL and heck even pretraining a bunch of smaller models in parallel) -- the XS is FT.1's row (L4, job-level, via the Prime); the 0.03 USD CPU billing probe still precedes the first GPU hour. (c) every cost row gains an abliterated? column (owner 16:2xZ, verbatim on goal:g14: a prod model must be abliterated, by us if by nobody else; identical -> abliterated wins): Bonsai PTQ1_0 = stock NOT abliterated, the OrcaBonsai runtime LoRA is routed but inert on coding (C1 141/164 completions byte-identical to B; 86.0 vs 86.6 pct, p = 1.0), so the row has no abliteration proof yet; Qwen3.5-9B-Q4_K_M = stock NOT abliterated, ABL.01 (hypothesis:lm-own-refusal-direction-on-qwen35-9b-cuts-refusals-at-no-coding-cost, G5.25) is the town's first own lever; deepseek-v4.1-flash = hosted, N/A. The switch (G5.27 / SWR.01) is a QUALITY test on the battery (within 10 pct of v4.1-flash), a different axis from this cost table; both must hold before the chains mint an mvp.
