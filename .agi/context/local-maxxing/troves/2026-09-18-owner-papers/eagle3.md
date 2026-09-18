# eagle3 — EAGLE-3: Scaling up Inference Acceleration via Training-Time Test
READER: research-reader (read-only). TROVE APPEND-ONLY. Read 2026-09-18 UTC.

## PAGE 1 — arxiv.org/abs/2503.01840 + NeurIPS 2025 (checked 2026-09-18)
- TITLE (MEASURED): "EAGLE-3: Scaling up Inference Acceleration of Large Language Models via
  Training-Time Test"
- AUTHORS (MEASURED from paper listing): Yuhui Li, Fangyun Wei, Chao Zhang, Hongyang Zhang
  (Microsoft Research et al.). YEAR: submitted 3 Mar 2025; NeurIPS 2025.
  ID: arXiv:2503.01840.
- MECHANISM (MEASURED, abstract): abandons EAGLE's feature prediction for DIRECT token
  prediction; replaces top-layer-feature reliance with MULTI-LAYER feature fusion
  ("training-time test"). Drafter is a small module on top of the frozen target; trained to
  predict tokens directly, scaling with training data.
- HEADLINE NUMBERS (MEASURED, abstract): speedup up to 6.5x; ~1.4x improvement over EAGLE-2;
  in SGLang, 1.38x throughput at batch size 64.
- COMPUTE SAVED (MEASURED): inference inference-time speedup 6.5x, NOT training compute.
- CODE/LICENCE (MEASURED): github.com/SafeAILab/EAGLE — Apache-2.0 (repo listing).
- QWEN-CLASS TRUNK? YES in practice: HF Hub has EAGLE-3 draft heads for Qwen2.5-7B/14B/32B
  (thoughtworks/Qwen2.5-7B-Instruct-Eagle3; ruipeterpan/Qwen2.5-{7,14,32}B-Instruct_EAGLE3_UltraChat),
  trained with SpecForge. MEASURED from HF pages 2026-09-18.
- FIT: the closest modern precedent — frozen Qwen-class trunk + trained decode-side drafter,
  with published Qwen draft heads and an open training harness (SpecForge).
