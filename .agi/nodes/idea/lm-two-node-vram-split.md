---
id: idea:lm-two-node-vram-split
mint_id: 2b733564d5704bb3b27440418ebdfc5a
type: idea
parents:
  - goal:g5.22
next_edges: []
edited_by: thought-master
scaffold_hash: 2aa93d80773530c7
season: 2
title: "Split inference load across local-town (8 GB) + a rented Camber XS (24 GB) = ~32 GB VRAM in bursts: job-level split is workable, layer/tensor split across the tunnel is not"
town: core
---
<!-- BODY:BEGIN -->
# idea:lm-two-node-vram-split

## Idea

What is the concept? `scale:` big (new chain) or small (extension)?

## Agent Notes
OWNER 2026-09-18 03:5xZ (thought-master pane), verbatim: "also we could try to parallelize and split load using rented you since we sorta have 32gb vram between those two nodes". MEASURED CONSTRAINTS: local-town egress is a per-line cap of 0.5-0.9 MB/s behind <overlay-if> (TM.20/TM.24/TM.26); tensor or pipeline parallelism between two boxes moves activations per token/layer (MBs per token for a 27-50B model) -> infeasible over that link by four orders of magnitude; Camber XS = 24 GB, ~$1.50-3/h, 3 GPU-h/month on record, every hour is banked spend. WORKABLE SHAPES: (a) JOB-LEVEL split -- the rented 24 GB serves the model that does not fit 8 GB (Qwen3.8-50B sub-4-bit, or the 27B at Q4/Q8 for quality rows) while local-town keeps serving the kid tier (Bonsai 2 27B PTQ1_0) -- two endpoints, one router by job class; (b) burst tasks that are compute-bound and byte-light: the dead-head scans, requants, and QLoRA (idea:lm-kid-persona-lora) on the rental, results (KBs-MBs) shipped back; (c) NOT tensor-parallel: only if both nodes sat on one LAN (the GPU-box relocation stream would make local-town + a second local card that case). FIRST ROUND (banked spend, needs the Prime GO on one XS hour): a 1-hour job-level trial -- rent, pull the 50B or 27B Q4 (Camber ingress measured first: if < 20 MB/s the hour is lost to download and the trial is a no), serve, run the same 20-prompt proxy + tg/pp rows as the local endpoint, cost row per 1M tokens incl. spin-up amortised over 1 h and 6 h; compare against Bonsai 2 27B local. No round until the Bonsai numbers exist (they decide whether the big model is needed at all).
