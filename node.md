---
id: hypothesis:lm-spec-decode-cpu-draft-hybrid
mint_id: 5ee62e6054a8400a9e9648d3c5d573cf
type: hypothesis
parents:
  - goal:g14.6
next_edges: []
ceiling: $1 OpenRouter; $0 compute; <= 3 GB downloads inside the local-town ceiling; file scope = .agi/context/local-maxxing/specdec/{prompts.jsonl, rows.jsonl, cmds.md} + bench/<utc>.jsonl + the kid experiment node + this node.
edited_by: thought-master
falsifier: < 1.2x on the median prompt, or any output differs from greedy no-draft, or the draft steals GPU memory -- then CPU-draft speculation does not pay on this box and the hybrid budget goes to MoE expert offload instead.
scaffold_hash: 6090044d54eca384
season: 2
testable_claim: On local-town (16 threads + 8 GB GPU), llama-server with the target fully on GPU (the 9B first; Bonsai 2 27B PTQ1_0 once served) and a draft model on CPU (-ngld 0, -td 16; candidates Qwen3.5-0.6B/1.7B or Ternary-Bonsai-1.7B, same tokenizer family required) reaches (1) >= 1.5x tg tok/s vs the same target without a draft on 20 kid-shaped prompts (node writing, probes, digests; prompts committed), 3 reps, warm-up first, per-row -t/-td/--draft-max/acceptance rate recorded; (2) outputs byte-identical to no-draft greedy decoding on the same prompts (speculative decoding is exact); (3) GPU VRAM unchanged within 200 MiB (the draft lives in RAM); (4) A1 untouched (all on local-town); (5) cost row per 1M output tokens from measured watts.
tests: ONE pi parent + ONE kid, off-box slot (alias only), $1 OpenRouter, $0 compute, downloads <= 3 GB (draft GGUFs); rows to bench/<utc>.jsonl labelled specdec-*, prompts + acceptance rates to .agi/context/local-maxxing/specdec/; rollback = the 9B back on /v1 as it was; kid line_ceiling 120; after the Bonsai round in the off-box queue (the target should be the model we will actually serve).
title: Speculative decoding with a small draft model on local-town 16 CPU threads and the target on the 8 GB GPU raises target tok/s by >= 1.5x on kid-shaped prompts at unchanged outputs
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:lm-spec-decode-cpu-draft-hybrid

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-18 04:0xZ (thought-master pane), verbatim: "Use gpu for speculative decode and enable parallel nation this way. Do massive parallel speculative decode and massive parallel confirmation rounds via deepseek paper technique". AMENDS THE ROUND (read: parallelisation): the GPU is the CONFIRMATION side -- the target verifies a whole draft block per forward pass -- and the draft may live on the GPU too (DeepSeek MTP: multi-token-prediction heads drafting several future tokens, confirmed in parallel by the main model; EAGLE-3-style heads per the town trove baseten-eagle3-heads.md), not only a CPU draft model. TWO DRAFT ARMS, same target, same prompts: arm A = CPU draft model (16 threads, as written); arm B = GPU-resident draft (MTP heads if the served model ships them -- Qwen3.8/Bonsai 2 27B: check the GGUF metadata for MTP tensors and llama.cpp support at the pinned commit -- else an EAGLE-3 / small GPU draft of the same family). MASSIVE PARALLEL = the served endpoint runs -np 4 and -np 8 WITH speculation (many kids at once): metric = AGGREGATE tok/s and per-stream tok/s vs no-draft at the same -np, acceptance rate and draft width per row; bar = >= 1.5x single-stream (as written) AND >= 3x aggregate at -np 8 vs single-stream no-draft, outputs byte-identical to greedy per stream. The CPU threads still carry the hybrid (spill / expert offload / arm A); VRAM headroom per arm recorded (a GPU draft must fit beside the 5.95 GB target inside 8 GB).

INGEST (thought-master 06:27Z, owner 06:1xZ asked for arXiv 2609.04010; digest at troves/2026-09-18-owner-papers/paper-2609-04010.md): 2609.04010 = Uno, 'Unlocking Lossless Speedups in LLMs via Discrete Diffusion' (Sahoo et al., IFM/Cerebras, 3 Sep 2026, Apache-2.0 code github ifm-ai/uno): every layer carries the AR weights plus rank-128 LoRA diffusion adapters; the diffusion pathway drafts a block of tokens in parallel and the frozen AR weights verify by rejection sampling (Leviathan Cor. 3.6) -- lossless speculative decoding with NO separate draft model; up to 3x, 2.2x at batch 1, 1.5x at batch 64 (H200); 8B Uno beats 26B DiffusionGemma and Mercury 2 on agentic/coding. This is the owner's 'diffusion augmented LLM' and the GPU-RESIDENT DRAFT ARM of this node in its purest form. Released: s-sahoo/uno-qwen3-8B (Qwen3-8B bf16 16.38 GB + 0.70 GB adapter) -- the only Qwen-based one; K2-Horizon-0.9B/7B-Uno (not Qwen). Sibling: DFlash (2602.06036) 5-layer block-diffusion drafter, 6.1x lossless on Qwen3-8B, models for Qwen3-4B/8B, measured on a B200. FEASIBILITY ON OUR BOXES: the fast path needs FlashAttention-2 (linear sampler) / FA3 (tree) = Ampere+/Hopper -- our 8 GB GPU is Turing (no FA2) and 16.4 GB bf16 does not fit it; the reference path gives no speedup -> NO download on our boxes (does not make sense). It fits ONE Camber XS (L4, Ada, FA2 yes): hypothesis:lm-uno-diffusion-draft-on-l4 minted as the banked XS-hour measurement. The CPU-draft arm of this node stays first; Uno/DFlash are the GPU-resident arm once an L4 hour is granted, and a llama.cpp block-diffusion drafter does not exist yet (research opportunity, not minted).
