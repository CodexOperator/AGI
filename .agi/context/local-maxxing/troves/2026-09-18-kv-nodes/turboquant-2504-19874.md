# turboquant-2504-19874 — TurboQuant + PolarQuant + QJL — reading digest
READ-ONLY. MEASURED = quoted from page read; ESTIMATE = inferred, arithmetic shown.
Sibling: paper-2510-03215.md (C2C) — not redone here.

## PAGE 1 — arXiv abs/html v1 (fetched 2026-09-18)
URL: https://arxiv.org/html/2504.19874v1 ; https://arxiv.org/abs/2504.19874
- TITLE (MEASURED): "TurboQuant: Online Vector Quantization with Near-optimal Distortion Rate"
- AUTHORS (MEASURED): Amir Zandieh (Google Research), Majid Daliri (NYU), Majid Hadian
  (Google DeepMind), Vahab Mirrokni (Google Research).
- DATE (MEASURED): arXiv:2504.19874v1 [cs.LG] 28 Apr 2025. Licence CC BY 4.0.
- ABSTRACT (MEASURED, quoted): "randomly rotating input vectors, inducing a concentrated Beta
  distribution on coordinates ... simply apply optimal scalar quantizers per each coordinate.
  ... we propose a two-stage approach: applying an MSE quantizer followed by a 1-bit Quantized JL
  (QJL) transform on the residual, resulting in an unbiased inner product quantizer."
- LOWER BOUND (MEASURED, quoted): TurboQuant "closely matches these bounds, differing only by a
  small constant (≈2.7) factor".
- KV-CACHE RESULT (MEASURED, quoted from abstract): "for KV cache quantization, we achieve absolute
  quality neutrality with 3.5 bits per channel and marginal quality degradation with 2.5 bits per
  channel."
- 2.5-BIT ALLOCATION (MEASURED, quoted): "in our 2.5-bit setup, 32 outlier channels are quantized at
  3 bits, while the remaining 96 channels use 2 bits, leading to an effective bit precision of
  (32×3 + 96×2)/128 = 2.5". 3.5-bit uses a different outlier ratio.
- CLAIM SCOPE (MEASURED): it is a general online VQ algorithm (vector search + KV cache), NOT a
  KV-cache-specific system. No serving kernel in the paper. Data-oblivious: no calibration data.

## PAGE 2 — Google Research blog (fetched 2026-09-18)
URL: https://research.google/blog/turboquant-redefining-ai-efficiency-with-extreme-compression/
- DATE (MEASURED, page): announces TurboQuant "to be presented at ICLR 2026"; PolarQuant "to be
  presented at AISTATS 2026"; QJL also introduced.
- MECHANISM (MEASURED, quoted): TurboQuant uses "PolarQuant ... and Quantized Johnson-Lindenstrauss
  (QJL)". QJL "reduces each resulting vector number to a single sign bit (+1 or −1) ... requires
  zero memory overhead."
- KV MEMORY CLAIM (MEASURED, quoted): "reducing the key value memory size by a factor of at least
  6x" with "perfect downstream results" on needle-in-a-haystack; "quantize the key-value cache to
  just 3 bits without requiring training or fine-tuning".
- NOTE (MEASURED discrepancy): blog says 6x / 3 bits; paper abstract says 3.5 bits neutral, 2.5
  bits marginal. 6x ≈ 16/2.7 bits effective (ESTIMATE: 16/3 ≈ 5.3x; 16/2.5 = 6.4x).
- QUALITY (MEASURED, blog): chart aggregates QA, code generation, summarization vs KIVI and
  PolarQuant; TurboQuant "optimal scoring performance" in dot-product distortion and recall.

## PAGE 3 — community implementations (fetched 2026-09-18)
URLs: https://github.com/OnlyTerp/turboquant ; https://github.com/0xSero/turboquant ;
      https://pypi.org/project/turbokv/ ; https://github.com/vivekvar-dl/turboquant
- "TurboKV" (what owner likely means): MEASURED — PyPI package `turbokv` v0.1.0 = "First
  open-source implementation of TurboQuant (arXiv 2504.19874)"; claims "4-7x LLM KV cache
  compression ... near-zero quality loss. No training, no calibration." Homepage
  github.com/vivekvar-dl/turboquant.
- 0xSero/turboquant (MEASURED): "3-bit keys, 2-bit values ... Triton kernels + vLLM integration",
  tested RTX 3090/5090. Caveat (MEASURED, quoted): "Savings are 30.9% of total KV because TQ only
  compresses the 10 full-attention layers (40% of KV)" on a hybrid-attention MoE.
- OnlyTerp/turboquant (MEASURED): "Random rotation + scalar Lloyd-Max quantizer that shrinks the KV
  cache to 3–4× smaller than FP16, no calibration data required."
- CODE STATUS (ESTIMATE): no upstream Google code; all are third-party clean-room, GPU/Triton only.
  No CPU path found in any of the above → NOT directly usable on ARM4C as-is.
- LICENCE (MEASURED): pypi turbokv page did not state SPDX in fetched text; repos mixed. TREAT AS
  UNVERIFIED until per-repo LICENSE read.

## BYTE TABLE (ESTIMATE — arithmetic shown)
Formula: bytes = 2 (K and V) × layers × kv_heads × head_dim × seq_len × bytes_per_elem.
Note: only layers with full attention count; many modern models use GQA so kv_heads << heads.
For a 9B-class and 27B-class at fp16 (2 bytes) vs 8-bit (1), 4-bit (0.5), 3-bit (0.375):
- 9B-class (ESTIMATE, Qwen3-8B-like: 36 layers, 8 kv_heads, head_dim 128):
  per token per layer = 2 × 8 × 128 × 2 B = 4096 B = 4 KiB fp16.
  4k tokens: 36 × 4 KiB × 4096 = 603,979,776 B ≈ 576 MiB fp16.
    8-bit 288 MiB; 4-bit 144 MiB; 3-bit 108 MiB.
  32k tokens: ×8 = 4608 MiB ≈ 4.5 GiB fp16; 8-bit 2.25 GiB; 4-bit 1.125 GiB; 3-bit 864 MiB.
- 27B-class (ESTIMATE, Qwen3-32B-like: 64 layers, 8 kv_heads, head_dim 128):
  per token per layer = 2 × 8 × 128 × 2 B = 4096 B = 4 KiB fp16.
  4k tokens: 64 × 4 KiB × 4096 = 1,073,741,824 B ≈ 1.0 GiB fp16.
    8-bit 512 MiB; 4-bit 256 MiB; 3-bit 192 MiB.
  32k tokens: ×8 = 8192 MiB = 8.0 GiB fp16; 8-bit 4.0 GiB; 4-bit 2.0 GiB; 3-bit 1.5 GiB.
- CAVEAT (ESTIMATE): real byte counts depend on exact layer/kv-head counts per checkpoint; treat as
  ±20%. llama.cpp q8_0 = 1.0625 B/elem, q4_0 = 0.5625 B/elem (32 vals + 2-byte scale per 32-block)
  → slightly larger than the ideal 1.0/0.5 above. See llama-cpp digest.
- ARM4C RELEVANCE (ESTIMATE): a 27B model at 32k context needs ~8 GiB fp16 KV alone — exceeds the
  ~7 GiB free on ARM4C and the 8 GB box. 4-bit KV → 2 GiB, which is the only way a 27B at 32k is
  even discussable on CPU+RAM; weights still dominate. 9B at 32k fp16 = 4.5 GiB KV + ~5-6 GiB
  weights (q4) ≈ 10 GiB → fits ARM4C only at reduced context or KV quant.
