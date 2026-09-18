# dspark — DSpark: Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation
READER: research-reader (read-only). TROVE APPEND-ONLY. Read 2026-09-18 UTC.

## PAGE 1 — arxiv.org/abs/2607.05147 (HTML) + NVIDIA NeMo docs (checked 2026-09-18)
- TITLE (MEASURED): "DSpark: Confidence-Scheduled Speculative Decoding with
  Semi-Autoregressive Generation"
- AUTHORS: not captured on abs page this read (UNVERIFIED beyond blog by Zhongzhu (Charlie) Zhou).
  YEAR: 2026. ID: arXiv:2607.05147.
- MECHANISM (MEASURED, abstract + NeMo docs): draft against a FROZEN target. Parallel backbone
  proposes a whole block in one pass; a lightweight SEQUENTIAL (Markov) head restores intra-block
  token dependency ("suffix decay" fix); a confidence head predicts per-position acceptance,
  driving confidence-scheduled verification. NeMo: "shares and FREEZES the target's embed_tokens
  and lm_head, training only the backbone, the feature projection, the Markov head..."
- HEADLINE NUMBERS (MEASURED, abstract): deployed in DeepSeek-V4 serving; +60-85% per-user
  generation speed at matched throughput vs production baseline MTP-1; mitigates verification
  waste. (Training-compute saving not quoted.)
- COMPUTE SAVED (MEASURED): 60-85% per-user speedup (inference, production).
- CODE/LICENCE: NVIDIA Megatron-Bridge / NeMo AutoModel recipe (docs.nvidia.com) — Apache-2.0
  (NVIDIA repos, standard). NOT independently verified this read.
- QWEN-CLASS TRUNK? Target is DeepSeek-V4 in the paper; the recipe is trunk-agnostic; NeMo
  example generic.
- FIT: DECODE-SIDE small module (parallel backbone + sequential head + confidence head) trained
  against a frozen trunk. Strong structural analog to the owner's "draft head + readout + fuser".
