---
id: idea:lm-model-stockpile
mint_id: 1fb89be0a71d4aa98db7166d6d9dfae2
type: idea
parents:
  - goal:g5.5
next_edges: []
edited_by: belam
scaffold_hash: bcaab6d8c839c5b7
season: 2
tags:
  - local-maxxing
  - owner-order
  - ops
thought_session: dissolve-legacy-2026-09-19
title: "Model stockpile: ablated + plain small models on the farm boxes, sized to the 8 GB GPU"
town: local-maxxing
---
# idea:lm-model-stockpile

## Owner order (verbatim, 2026-09-16 ~07:1xZ)
"Bare metal box in [region] with weak processor has almost 500gb of storage, so does the other bare metal box but slower. Can downloaded lots of slightly bigger small ish models. We need to stockpile some good ablated and non-ablated models of all types and sizes. There's a deepseek derisked I think and maybe a few qwen ablated. I don't think deepseek is small enough to just have though l, we're trying to focus on things that can run on the you available either direct or through quantization in combination with our other techniques." — "I'll have to find the HF links but for now proceed without."

## Iron (hardware only; addresses never in the graph)
- local-town: x86-8c 8c/16t, 16 GB, gpu-8g, 339 GB /data — the RUN box (served by hypothesis:gpu-local-town-openai-endpoint).
- encryption-town: i5 2c/4t, 8 GB, 352 GB /data — the ARCHIVE (weak CPU; gigabit LAN to local-town).
- swarm box (core-town): 27 GB free — never a stockpile host.

## Manifest (doc node to mint when the first rows exist)
One row per artifact: hf id · family · params (active/total) · variant (base | instruct | abliterated | distill) · formats kept (safetensors bf16 for ablation/LoRA work; GGUF Q8_0 / Q4_K_M / IQ3 ladder for serving) · bytes · licence · box:path · sha256 · date — every cell quoted from the model card (round-0 rule), nothing from memory.

## Sizing to the 8 GB GPU
≤8B Q4_K_M fully in VRAM; 14B Q4 split to RAM; 30B-A3B MoE split (3B active); 32B dense CPU-mostly; DeepSeek V3/V4 class = out. One full ladder for an 8B ≈ 33 GB → ~10 ladders per box → the list needs a priority order.

## Candidates to VERIFY from model cards (not asserted)
Qwen3 0.6/1.7/4/8/14B + 30B-A3B and their abliterated twins; Qwen2.5 0.5→14B; DeepSeek-R1-Distill-Qwen 1.5/7/14B (+ abliterated); Gemma-3 4/12B; Llama-3.x 3/8B; Phi-4-mini; SmolLM3. Owner's "deepseek derisked" + qwen abliterated HF ids: awaited.

## First falsifier
A model that fits the ladder on paper but measures < 10 tok/s tg on local-town at its smallest usable quant is not stockpile-worthy for serving (archive only).

## Cheapest test
Round 1 of the endpoint (Kid A/C) already measures the first two rows; the stockpile round = a download script with sha256 + a manifest doc node, run ON local-town via the sanctioned ssh command, downloads only to /data.

## Banked
Promotion to goal:g5.21 = the Prime's numbering; HF token / ssh path for the farm boxes = Prime + encryption-town.
What is the concept? `scale:` big (new chain) or small (extension)?
