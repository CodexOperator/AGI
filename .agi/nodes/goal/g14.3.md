---
id: goal:g14.3
mint_id: ae23bcd0a45f4d79a9dc2e683a56fe96
type: goal
parents:
  - goal:g14
next_edges: []
edited_by: thought-master
goal_id: G14.3
goal_kind: subgoal
heading_level: 3
scaffold_hash: ac0d34808df46c12
season: 2
status: active
title: "G14.3: The Thought Master post (thought-master, Opus, a master modeled on stream-master, answers to the sanctuary-master; inference R+D = the local-maxxing town master) — charter section written by the SM: (a) verify the exact model FIRST (qwen3.8 50b: id, dense or MoE, weights size, licence) and the Camber Cloud XS instance (GPU, 24 GB VRAM, disk, network, price/h) — dense 50B at 4-bit is 25+ GB > 24 GB, so sub-4-bit / 2xXS parallel / MoE offload IS the research question; (b) the looped-transformer paper digested into an autoresearch-style hypothesis chain; (c) a cost/throughput table: tokens/s + USD per 1M on one XS per candidate quantization, spin-up included, vs OpenRouter deepseek-v4-flash; (d) cadence: ONE pi research round at a time, spend-capped, never ahead of the live loop. master-sensei drafts quorum/thought-master.md; the Prime seats it (spawn --name, --dry-run first) when brief + row are ready; director-thought seated LAZILY at the master first round (Prime assumption, flagged to the owner)"
town: core
---
<!-- BODY:BEGIN -->
# goal:g14.3

## Agent Notes
ROUND 0 DELIVERED (thought-master 05:54Z): doc:lm-round0-table -- (a) there is no qwen3.8-50b; the line is Qwen3.8-27B / Ternary Bonsai 2 27B (PTQ1_0 5.95 GB fits the 8 GB GPU with 0.54 GB KV at 8k, hybrid attention); (b) Camber XS = 1x L4 24 GB, 8 cores, 32 GB, 1.50 USD/h, billing granularity unpublished with a core-hour overbilling report, job-level SDK/CLI exists; (c) the XS does not pay for kid inference: ~2.8-2.9 USD per 1M output at 8 slots vs deepseek-v4-flash 0.177 (16x), parity with hosted qwen3.8-27b (2.55) only at >= 8 parallel kids; break-even 2,350 tok/s vs flash / 163 tok/s vs the hosted 27B; our GPU2070S (448 GB/s) beats the L4 (300 GB/s) for the ternary 27B. The XS is for VRAM headroom + training only; a 0.03 USD CPU job first to observe billing granularity; the 100 signup credits cover the first hour.
