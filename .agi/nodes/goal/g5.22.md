---
id: goal:g5.22
mint_id: 5271be1d649847a79aa2afcaa722b0e8
type: goal
parents:
  - goal:g5
next_edges: []
confidence: 0.8
edited_by: belam
goal_id: G5.22
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: f9725fc3dd3274c8
season: 2
seeds:
  - hypothesis:lm-dead-head-kc-threshold-is-not-a-critical-point
  - hypothesis:lm-dead-head-prune-by-oscillator-coherence
  - hypothesis:lm-eagle3-drafter-on-frozen-qwen3-4b
  - hypothesis:lm-kv-slot-save-beats-reprefill
  - hypothesis:lm-rig-fetch-supervisor-enforces-the-bytes-rules
  - hypothesis:lm-rpc-cpu-split-pays
  - hypothesis:lm-spec-decode-cpu-draft-hybrid
  - idea:lm-cross-layer-topk-index-reuse
  - idea:lm-dead-head-coupling-scan
  - idea:lm-draft-refit-own-traffic
  - idea:lm-eagle3-head-per-byte
  - idea:lm-hunch-cluster-parallel-speculation
  - idea:lm-hunch-per-layer-draft-kv-share
  - idea:lm-kda-constant-state-kv-bytes
  - idea:lm-kv-bytes-ledger-q4-cache
  - idea:lm-model-stockpile
  - idea:lm-nodes-as-kv-caches
  - idea:lm-online-draft-distillation-cpu-split
  - idea:lm-searched-swa-pattern-zero-train
  - idea:lm-self-spec-small-draft-head
  - idea:lm-two-node-vram-split
status: active
tags:
  - local-maxxing
  - track-i
  - inference
title: "G5.22: TRACK I — inference-side optimisation of the local models the town runs its parents and kids on: oscillator/coherence head pruning WITHOUT spikes first, then context and throughput from the DeepSeek-class papers, then every technique layered (owner 21:4xZ 09-20)"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# goal:g5.22

## Agent Notes
**Owner source (2026-09-20 21:4xZ, verbatim on goal:g14):** "as far as using the models for parents and kids I wanna: Apply the oscillator technique first without any spike stuff just trying to prune heads, see if we can increase context limits and token throughput via techniques in the other papers we have from deepseek etc, (we have a ton of cpu threads here and a ton of ram), and also applying all the techniques layered." Pace: "super slow … super small chunks."

**Commits to.** Make the local models the town actually runs its parents and kids on (today Qwen3.5-9B Q4_K_M and Bonsai 2 27B PTQ1_0 on the rig) cheaper per token and longer in context by layering *existing* inference-side techniques, in this order: (1) head pruning guided by the oscillator/coherence method, with no spiking machinery; (2) context and throughput levers from the DeepSeek-class papers already in the trove (MLA/NSA-style KV, MTP/spec-decode, TurboQuant-class KV quantisation, kv-slot, eagle3) — each measured alone; (3) the survivors layered, so that a new optimisation is *composed* from off-the-shelf ones. Spiking work (bend2 language mapping) stays a side track under G14.5 and enters here only as a learned, measured piece.

**Invariants.** Every lever is measured on the same bench rows (tok/s at empty and 16K context, peak VRAM, J/token, KLD or pass@1 vs the unmodified model) before and after; a lever that costs > 2 points on the G5.27 battery is not kept whatever its speed; nothing here modifies weights (that is G5.23); the resident server is restored after every GPU window; one paid round at a time.

**Falsifiers.** (a) The oscillator/coherence ranking is falsified as a pruning criterion if the K_c threshold shows no knee and coherence does not rank head damage (first chunk) — then pruning proceeds by measured Δloss/GQA-group yield and the oscillator budget is released. (b) The goal itself is falsified if, after each lever has one measured chunk, no lever *or* layering improves tok/s or context by ≥ 20 % at ≤ 2 battery points — then the local models are served as-is and the effort moves to G5.23.

**Done when.** A layered configuration is measured end to end on a real round (a parent + kid on the served model) and its rows sit in the G5.27 gap table; the mvp that G5.27 mints cites this goal's contributing chains.

**First chunk (minted):** `hypothesis:lm-dead-head-kc-threshold-is-not-a-critical-point` (the 5-CPU-minute kill-test). Sub-sub-goals are the director's to mint (G5.22.1 heads, G5.22.2 context/throughput, G5.22.3 layering), same format as this node, before any chunk runs.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
owner ask 2026-09-21: renumber local-maxxing research g5.22 → g5.22 (g5 continuation after g5.21; mint_id preserved; town:local-maxxing kept); no director assignment
<!-- THOUGHT:END -->
