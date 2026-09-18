# medusa — Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads
READER: research-reader (read-only). TROVE APPEND-ONLY. Read 2026-09-18 UTC.

## PAGE 1 — arxiv.org/abs/2401.10774 (checked 2026-09-18)
- TITLE (MEASURED): "Medusa: Simple LLM Inference Acceleration Framework with Multiple
  Decoding Heads"
- AUTHORS (MEASURED): Tianle Cai, Yuhong Li, Zhengyang Geng, Hongwu Peng, Jason D. Lee,
  Deming Chen, Tri Dao (Princeton, UIUC, Together AI, UChicago). YEAR: submitted 16 Jan 2024;
  ICML 2024. ID: arXiv:2401.10774.
- MECHANISM (MEASURED, abstract): add extra decoding heads predicting multiple future tokens
  in parallel; tree-based attention constructs candidate continuations verified simultaneously.
  TWO recipes: Medusa-1 = heads fine-tuned on top of a FROZEN backbone LLM (lossless accel);
  Medusa-2 = heads trained jointly with backbone (special recipe). This is literally the
  "freeze trunk, train decode-side draft head" pattern.
- HEADLINE NUMBERS (MEASURED, web index of abs/paper; not re-derived from PDF this read):
  Medusa-1 on Vicuna-7B gives ~2.2-3.6x speedup without quality loss. (Quote seen:
  "Medusa augments LLM inference by adding extra decoding heads ... achieving 2.2-3.6x
  speedup" — alphaxiv/abs index 2026-09-18.) TREAT as MEASURED-from-index, pending PDF check.
- COMPUTE/SPEED SAVED (MEASURED): 2.2-3.6x inference speedup (not training compute).
- CODE/LICENCE (MEASURED, GitHub FasterDecoding/Medusa): Apache-2.0. Draft heads released for
  Vicuna / Zephyr / etc.
- QWEN-CLASS TRUNK? Original = Vicuna/LLaMA-class. The METHOD is trunk-agnostic; Qwen variants
  exist in the wild (EAGLE-3 Qwen heads, below).
- FIT: strongest direct precedent for a frozen small LLM trunk + trained draft head.
