# mixture-of-recursions-2507-10524 — MoR (recursive depth + adaptive routing) — reading digest
READ-ONLY. MEASURED = quoted from a page/repo read today; ESTIMATE = inferred, arithmetic shown.

## PAGE 1 — arXiv abs/html (fetched 2026-09-18)
URL: https://arxiv.org/abs/2507.10524 ; https://arxiv.org/html/2507.10524v3
- TITLE (MEASURED): "Mixture-of-Recursions: Learning Dynamic Recursive Depths for Adaptive
  Token-Level Computation" (NeurIPS 2025).
- AUTHORS (MEASURED): Sangmin Bae, Yujin Kim, Reza Bayat, Sungnyun Kim, Jiyoun Ha, Tal Schuster,
  Adam Fisch, Hrayr Harutyunyan, Ziwei Ji, Aaron Courville, Se-Young Yun (KAIST AI, Mila, Google).
- DATE (MEASURED): submitted 2025-07-14.
- MECHANISM (2 lines, MEASURED): a shared stack of layers is reused across recursion steps (parameter
  efficiency), while a lightweight router assigns each TOKEN a different recursion depth (adaptive
  compute). Attention is computed only among tokens still active at a depth, and only their KV pairs
  are cached ("recursion-wise KV caching"); a "recursive KV sharing" variant reuses the first
  recursion's KV to cut memory further.
- DIFFERENCE FROM TEMPORAL RECURRENCE: DEPTH recurrence at a position, with per-token early exit;
  no state carry across token boundaries beyond KV.

## UNIQUE PARAMS vs EFFECTIVE DEPTH (MEASURED)
- Base models: 135M, 360M, 730M, 1.7B (non-embedding params). Recursion N_r = 2 or 3; with
  Middle-Cycle sharing the unique-parameter count is "approximately one-third" of the base at N_r=3
  (MEASURED, paper S3.1). ESTIMATE: a 360M base with N_r=3 => ~120M unique params, effective depth
  ~3x the shared block.
- Sharing schemes (MEASURED Table 1/5): Cycle, Sequence, and variants Middle-Cycle, Middle-Sequence;
  Middle-Cycle (retain unique first+last layers) is the safest/best choice.

## RELEASED WEIGHTS (MEASURED from GitHub README + HF API today)
- HF: **NOT released on HuggingFace** — a search for `mixture_of_recursions` / `MoR-360` finds no
  official weights (MEASURED). Checkpoints for 360M Vanilla / Recursive / MoR are on an external
  Google Drive folder linked from the repo (MEASURED README S"Pretrained Checkpoints").
- Repo: github.com/raymin0223/mixture_of_recursions — **Apache-2.0** (MEASURED LICENSE), built on the
  Llama architecture; requires torch 2.6 + flash-attn 2.7.4 (GPU-oriented; MEASURED README).
- No GGUF, no llama.cpp arch; the router + selective-KV graph would have to be ported (ESTIMATE).

## CPU RUNNABILITY (ESTIMATE)
- Not runnable as-is on the 4-core aarch64 box: no HF weights, no GGUF, flash-attn/CUDA-oriented
  training/eval harness. A CPU port of the 360M (N_r=3, ~120M unique) is plausible but is new code,
  not a config change. Marked NOT-TODAY.

## QUALITY vs NON-LOOPED (MEASURED, paper Table 3)
Equal training budget 16.5e18 FLOPs, FineWeb-Edu, 360M base:
- MoR (expert-choice router, 2 recursions): average few-shot accuracy **43.1%**, ~50% fewer params.
- Vanilla Transformer: **42.3%**. => MoR Pareto-dominates at equal FLOPs.
- IsoFLOP sweep (Fig 3, 2e18/5e18/16.5e18): MoR beats Recursive baselines at every size; it
  UNDERPERFORMS vanilla at the smallest size (135M), and "matches or exceeds" vanilla at larger scales.
- **Important caveat (MEASURED, Table 7):** at 1.7B under 68.5e18 FLOPs the vanilla model performs
  slightly BETTER than MoR — the authors flag that MoR's design may not scale. Do not over-claim.
- Throughput (MEASURED): up to **2.06x** speedup at max batch with MoR-4 (early exit reduces KV);
  "up to 2x greater inference throughput ... at similar accuracy" (abstract).

## TRAINING RECIPE COST (MEASURED)
- Pretrained on a deduplicated FineWeb-Edu subset (SmolLM-Corpus); experiments at 10B and 20B tokens;
  scales 135M-1.7B. Evaluation on a single datacenter-class accelerator (generic class). No
  GPU-hour total stated (gap). Training FLOPs reduced by skipping exited tokens in attention.

## VERDICT FOR THE TOWN
- Conceptually the richest of the released-ish set (parameter sharing + adaptive compute + KV
  reduction), but **no HF weights, no GGUF, and it loses at 1.7B**. Rank below Ouro for the CPU kid
  eval; a candidate for a later from-scratch tiny reimplementation, not a today-run.
