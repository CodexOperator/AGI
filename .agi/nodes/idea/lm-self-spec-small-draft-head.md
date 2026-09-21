---
id: idea:lm-self-spec-small-draft-head
mint_id: f49c4449e600445b9bc1f068176acdf2
type: idea
parents:
  - goal:g5.5
next_edges: []
edited_by: belam
scaffold_hash: 2f971700686e40ee
season: 2
tags:
  - local-maxxing
  - treasury
thought_session: dissolve-legacy-2026-09-19
title: "Self-speculation on a 0.6B: shallow split + factored draft head, gated by batch-verify cost"
town: local-maxxing
---
# idea:lm-self-spec-small-draft-head

## Source
doc:arxiv-2510-05421 — "Draft, Verify, and Improve: Toward Training-Aware Speculative Decoding" (https://arxiv.org/html/2510.05421); digest `.agi/context/local-maxxing/papers/arxiv-2510-05421.md`; critic grounded=4/5 — All paper numbers trace verbatim to the fetched HTML (Tables 1-3, split, H100/A40, 80%, ~3x); the reader's Qwen arithmetic reproduces exactly; errors are attribution (draft head is not stated to be the LM head, no LoRA rank in source, source says 'one shallow forward' not k_spec reads) and seed over-reach (factored head is untested by the paper, GGUF shipping infeasible without engine changes, 70-90 tok/s and 1-2 h unsupported); corrected seed adds a free swarm-box batch-verify-cost gate as the first falsifier.

## Lever
DVI's demonstrated mechanism (one backbone split at a shallow layer, frozen deep path verifies a k_spec=4 draft block losslessly under greedy, draft head trained online by KL-to-verifier-logits then a reward-masked correction; 2.16x on Spec-Bench from 2,000 prompts) saves the second model's bytes and KV entirely, and on tied-embedding Qwen3-0.6B the 26.1% LM head makes the draft head's size the dominant per-draft-token byte cost (reader arithmetic: full-head draft 0.314 vs factored rank-64 draft 0.069 of a full pass) — provided the swarm box's 5-token verify pass still costs about one weight read.

## What it buys the town
If the gate passes, a lossless (greedy) speculative decode of Qwen3-0.6B on the swarm box with no second model in the 23 GB, with the drafter trained on local-town from a few thousand prompts; the reader's ~2x figure is a bytes-ledger ceiling, not a measured number, and shipping into llama.cpp needs either the full tied head or engine changes.

## First falsifier
On the swarm box, llama-bench Qwen3-0.6B Q8_0 with a 5-token batch versus 1-token decode: if the 5-token forward costs >= 2x the single-token forward, the block-verify amortisation the whole ledger assumes is gone and the idea is dead before any drafter is trained (second falsifier: held-out MAT of the factored draft head at k_spec=4 after 2,000-prompt KL-only distillation < 2.0).

## Cheapest test on our iron
Swarm box (arm-cloud, $0, ~5 min): llama-bench batch-5 vs batch-1 forward cost on Qwen3-0.6B Q8_0; then local-town (gpu-8g, torch venv, $0, wall-clock unmeasured): frozen Qwen3-0.6B fp16, a factored rank-64 draft head on the layer-2 output, KL-only online distillation over 2,000 ShareGPT prompts logging tuples up to the first reject, report batch-acceptance curve and held-out MAT at k_spec=4.

## Numbers (quoted in the digest)
- DVI avg speedup=2.16x (Table 2, Avg.)
- EAGLE-2 avg speedup=2.18x; EAGLE-1=2.05x; Hydra=1.96x; Medusa=1.66x; PLD=1.62x; SpS=1.48x (Table 2)
- DVI MAT/speedup per task: MT-Bench 3.07/1.97x, Translation 3.53/2.24x, Summarization 3.55/2.02x, QA 3.61/2.14x, Math 3.04/2.02x, RAG 3.53/2.58x (Table 2)
- EAGLE-2 MAT/speedup per task: MT-Bench 4.75/2.64x, Translation 3.22/1.73x, Summarization 3.96/2.15x, QA 3.70/1.96x, Math 4.73/2.59x, RAG 4.09/2.02x (Table 2)
- split=layer 2 drafter, layers 3-32 verifier; k_spec=4; greedy temperature 0; no tree (Sec 4.1, App A)
- training=2,000 ShareGPT prompts, 1 epoch, 2,000 optimiser steps (Table 1)
- prompt exposures: Medusa 120,000 (~60x), Kangaroo 1,200,000 (~600x), EAGLE 2,400,000 (~1,200x) vs DVI 2,000 (Table 1); 'EAGLE-2 having a 1000x larger training budget' (Sec 4.2)
- KL-only MAT=1.933 speedup=1.435x; PG-only MAT=0.035 speedup=0.341x; CE-only MAT=0.039 speedup=0.335x (Table 3)
- KL-only batch acceptance plateau ~80% (Sec 4.3)
- hardware=single NVIDIA H100, subset repeated on A40 with unchanged rankings (App A)
- Qwen3-0.6B: 28 layers, hidden 1024, vocab 151,936, tied embeddings -> head ~155.6M = 26.1% of ~596M params, two layers = 5.3% (HF config.json, arithmetic ours)
- Qwen2.5-0.5B: 24 layers, hidden 896, vocab 151,936, tied -> head ~136.1M = 27.6% of ~494M, two layers = 6.0% (HF config.json, arithmetic ours)

## Provenance
Ingestion 2026-09-16 on the owner's GO ("idea is exactly the node type meant for deeper research"): reader → adversarial critic (corrected seed) → this node. Hypotheses hang from here.
What is the concept? `scale:` big (new chain) or small (extension)?
