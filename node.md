---
id: idea:lm-dead-head-coupling-scan
mint_id: 2a64dd181b29411f8270ea5c9e845f9c
type: idea
parents:
  - goal:g5.22
next_edges: []
edited_by: thought-master
scaffold_hash: cc015006f24072c0
season: 2
tags:
  - local-maxxing
  - treasury
title: GQA-group dead-head KV compaction on Qwen3-0.6B (g=2), scan as D1 prior
town: local-maxxing
---
# idea:lm-dead-head-coupling-scan

## Source
doc:dead-head — "Coherence-Guided Dead-Head Identification in Frozen Transformers: A Zero-Parameter Geometric Threshold from Coupled-Oscillator Criticality" (https://github.com/project-89/coherence-guided-dead-head-identification); digest `.agi/context/local-maxxing/papers/dead-head.md`; critic grounded=4/5 — Numbers trace to source bytes but the framing does not: ground truth is zero- not mean-ablation, death_persistence is a batch-timer fraction not a recurrence quantity, the '157 dead' rule is not 'z<0.96', the paper's SmolLM2 234 contradicts its own bundle's 261, and the artifact itself refutes the K_c story (precision rises monotonically through chi_c=0.96, Spearman(z,dL)=+0.27); what survives is GQA-group KV compaction tested on Qwen3-0.6B (g=2) and the artifact as a free D1 ground truth.

## Lever
The only cost-saving mechanism the source demonstrates is Level-2 GQA compaction: when every query head sharing a KV head is below the coupling threshold, drop the whole group, which removes that group's K/V/Q/O weight slices and its KV-cache bytes on every decoded token (SmolLM2 g=3: KV 81,920 -> 59,392 B/token, -27.5%, params -5.98%, +0.53 nats @1024), gated combinatorially by group size (Qwen2.5-0.5B g=7: 3/48 groups); the coupling scan itself (32 x 128-token forward passes) is a free ranking signal, not a bytes lever, and its rank correlation with zero-ablation damage is only +0.27.

## What it buys the town
On the swarm decoder Qwen3-0.6B's KV cache is 28 layers x 2 x 8 heads x 128 x 2 B = 114,688 B/token (~235 MB at 2k context, comparable to its Q8 weights), so every fully-dead pair of its 224 g=2 KV groups is a permanent per-token bandwidth cut on the town's own decode model; separately, the artifact's 336 zero-ablation deltas on Qwen2.5-0.5B are a free head-level ground truth to score D1's per-layer-normalized mean-ablation importance against, with no GPU.

## First falsifier
Run coherence_anatomy_scan.py on Qwen/Qwen3-0.6B and count KV groups (q-head pairs) with both heads dead: if fewer than ~10% of the 224 groups are fully dead, or if removing them (zero the pair's o_proj slices, measure loss on a held-out slice) costs more than the SmolLM2 +0.53 nats for the bytes saved, the lever is dead on the town's model.

## Cheapest test on our iron
local-town torch venv (cuda, or cpu at fp32 2.4 GB), `python scripts/coherence_anatomy_scan.py --model Qwen/Qwen3-0.6B --device cuda --output qwen3.json` (32 x 128 WikiText-2 tokens, ~5 min, $0), then a 20-line script pairing q heads 2i,2i+1 per layer to count fully-dead groups and, on the swarm box with json only, Spearman(z_h, delta_loss) plus the chi_c sweep on the bundled Qwen2.5-0.5B artifact (already done here: rho +0.268, no feature at 0.96).

## Numbers (quoted in the digest)
- chi_c=0.96025=0.679*sqrt(2) (paper.tex abstract; scan.py L41)
- tau_death=0.03465 d=768, 0.03000 d=1024, 0.03207 d=896, 0.03098 d=960, 0.01500 d=4096, 0.01897 d=2560 (Table tab:main-matrix)
- Qwen2.5-0.5B: 24 layers x 14 heads=336; dead 157, protected 45 (boundary 42 'first=2,last=1', bridge 3), alive 134; TP 150, FP dead-unsafe 7, safe_recall 0.479, dangerous_keep_rate 0.696; ground_truth_loss_threshold 0.022858 = 1% of baseline 2.285843; seq_len 128, 8 calib + 8 eval seqs, device mps (artifact clr_theory)
- Qwen2.5-0.5B dead per layer (derived from clr_theory.decisions): L0-1 0, L2 8, L3 6, L4 10, L5 8, L6 5, L7 8, L8 9, L9 12, L10 11, L11 13, L12 6, L13 9, L14 6, L15 8, L16 11, L17 4, L18 5, L19 7, L20 1, L21 5, L22 5, L23 0
- Qwen2.5-0.5B per-head ablation delta_loss over 336 heads: min -0.0119, median 0.00425, max 0.3949; sum over 157 dead heads = 1.027 vs joint dead_only +1.203 @128 (derived from head_results + timing proxy)
- Qwen2.5-0.5B worst single head (L2 H5, dL 0.395, z=-0.078) is inside the dead set; 7 dead-but-unsafe heads have z from -6.19 to -0.078 (derived from artifact)
- Qwen2.5-0.5B z_h group means: dead -1.22 (std 1.86), alive 2.79 (std 1.78), unsafe 0.098, Cohen's d 2.20 (base_rate_analysis.json)
- Qwen2.5-0.5B repeatability seeds 7/11/19: dead_count 156/159, dead_precision 0.9615/0.9811, dead_only_delta_loss 1.128/2.077/1.753 (repeatability_summary_v1.json)
- Qwen2.5-0.5B redundancy pass: 62/134 alive heads redundant, precision 0.9516; dead+redundant eval loss 4.371 vs baseline 2.246 (artifact redundancy_pass)
- combined_delta_loss (dead+redundant removed): 1.847 GPT-2, 1.430 GPT-2M, 2.125 Qwen2.5-0.5B, 2.051 SmolLM2, 1.604 OpenLLaMA (threshold_transfer_summary.json)
- GPT-2 3-seed dead_only_delta_loss mean 2.794 std 0.158 (repeatability_summary_v1.json)
- SmolLM2 Level-2: 44/160 KV groups dead (27.5%), KV 81,920->59,392 B/token, params 361,821,120->340,194,240, prefill +30.96% @1024, dLoss +0.53206 (paper GQA section; smollm2_level2_kv_compaction_v1.json)

## Provenance
Ingestion 2026-09-16 on the owner's GO ("idea is exactly the node type meant for deeper research"): reader → adversarial critic (corrected seed) → this node. Hypotheses hang from here.
What is the concept? `scale:` big (new chain) or small (extension)?
