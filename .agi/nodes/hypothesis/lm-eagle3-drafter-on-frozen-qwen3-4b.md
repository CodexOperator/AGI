---
id: hypothesis:lm-eagle3-drafter-on-frozen-qwen3-4b
mint_id: 2ba014df906b4a658c31aa90610dd1e0
type: hypothesis
parents:
  - idea:lm-draft-refit-own-traffic
  - goal:g5.22
next_edges: []
ceiling: 1 USD OpenRouter per round (pi parent + kid); 0 USD compute (rig only, 0 rental); <= 6 h training wall; kid line_ceiling 120; downloads slow mode only
edited_by: thought-master
falsifier: Acceptance length < 2.0 on held-out own traffic after the full budget, or any non-identical greedy output, or the frozen-trunk training does not fit 8 GB even with offline hidden states (record the peak VRAM and the cache GB/token) -- then the digested recipe does not transfer to an 8 GB box at 4B, and the drafter path is FailFast (off-the-shelf drafter, no training) or Uno on the XS. If SpecForge lists no Qwen3 target, the Medusa-1 fallback runs the same steps; if neither trains, the node is disproved on conjunct (5).
scaffold_hash: a7accf36f0ac0991
season: 2
testable_claim: "On GPU2070S (8 GB VRAM, local-town), an EAGLE-3 drafter (SpecForge, Apache-2.0; fallback Medusa-1 heads, FasterDecoding/Medusa, Apache-2.0) trained with the target Qwen/Qwen3-4B FROZEN -- hidden states of the fused layers precomputed OFFLINE with the target in 8-bit on the GPU and cached to the rig disk, the drafter (one decoder layer, <= 0.5B params, bf16) trained on >= 2M tokens of the town stored kid transcripts (kid-sft/kid_sft.jsonl + session transcripts, held-out 200 prompts of the same traffic) -- reaches (1) mean acceptance length >= 3.0 tokens per verify step on the held-out slice, (2) byte-identical greedy outputs vs plain decoding on all 200, (3) >= 1.8x wall tok/s at batch 1 and >= 1.3x at batch 4 under SGLang with the target in AWQ-INT4 on the same GPU, (4) a catch-up curve: acceptance length vs training step, reported as steps-to-90-percent-of-final and the loss plateau step, (5) training wall <= 6 h on the rig, never beside a live tg/pp row."
tests: "RECIPE SOURCES (trove, quoted): Medusa-1 = heads only on a frozen backbone, 2.2-3.6x lossless (arXiv 2401.10774); EAGLE-3 = frozen target, direct token prediction with multi-layer feature fusion, up to 6.5x, SpecForge harness + published Qwen2.5 heads (arXiv 2503.01840); the freeze budget shape = DeepSeek-V3.2-Exp warm-up (freeze all but the module, 1000 steps, LR 1e-3, KL). STEPS for ONE pi parent + ONE kid: (1) verify SpecForge supports a Qwen3 target (repo README, quote it) else switch to Medusa-1; install on the rig in a venv, nothing on ARM4C; (2) gates before every step: free VRAM >= 7.5 GB, rig disk floor 20 percent, no live tg/pp row, ambient loadavg recorded; (3) corpus: assemble >= 2M tokens from kid-sft/kid_sft.jsonl + stored session transcripts, hold out 200 prompts, record token counts; (4) precompute hidden states of the fused layers with Qwen3-4B in 8-bit on the GPU; record GB/token and wall; (5) train the drafter, log loss + acceptance length every N steps until the plateau (the catch-up curve), cap 6 h wall; (6) eval on the 200 held-out prompts: acceptance length, greedy identity (byte diff), tok/s at batch 1 and 4 vs plain SGLang with the same AWQ-INT4 target; rows to bench/<utc>.jsonl with the loadavg gate beside each; (7) the parent re-runs the eval on 20 prompts itself. FILE SCOPE .agi/context/local-maxxing/eagle3/{cmds.md, corpus_stats.json, curve.jsonl, rows.jsonl} + bench/<utc>.jsonl + the kid experiment node; anonymization rule in the brief (GPU2070S/ARM4C/CPU8G only). DOWNLOADS: Qwen3-4B bf16 (already queued) + Qwen3-4B AWQ-INT4 (~2.7 GB), slow mode, sha256, behind the queue."
title: A decode-side drafter trained on the town OWN traffic against a FROZEN Qwen3-4B trunk, on the 8 GB rig at 0 USD compute, reaches mean acceptance length >= 3.0 with byte-identical greedy outputs -- and its catch-up curve (steps to 90 percent of final acceptance) is the number the owner asked for
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-eagle3-drafter-on-frozen-qwen3-4b

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
