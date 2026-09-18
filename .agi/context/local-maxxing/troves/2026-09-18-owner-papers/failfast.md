# failfast — Fail Fast, Win Big (dLLM drafter, no fine-tuning)
READER: research-reader (read-only). TROVE APPEND-ONLY. Read 2026-09-18 UTC.

## PAGE 1 — arxiv.org/abs/2512.20573 (checked 2026-09-18)
- TITLE (MEASURED): "Fail Fast, Win Big: Rethinking the Drafting Strategy in Speculative
  Decoding via Diffusion LLMs". YEAR: submitted 2025-12; v3 2026-01-28. ID: arXiv:2512.20573.
- MECHANISM (MEASURED, abstract): uses a diffusion LLM (dLLM) as the drafter for an
  autoregressive verifier; dynamically adapts speculation length — short drafts in hard regions,
  long in easy regions ("speculating and accepting 70 tokens at a time").
- HEADLINE NUMBERS (MEASURED, abstract): WITHOUT ANY FINE-TUNING, up to 4.9x speedup over
  vanilla decoding, 1.7x over best naive dLLM drafter, 1.7x over EAGLE-3.
- COMPUTE SAVED (MEASURED): inference 4.9x; TRAINING = ZERO (no fine-tuning) — the extreme
  end of "don't train the trunk at all".
- CODE/LICENCE: "open-source at this https URL" — repo not verified this read.
- QWEN-CLASS TRUNK? Evaluated "across diverse models" (unspecified here). Related HF drafters
  from the same group are Qwen2.5-7B/14B/32B EAGLE-3 heads.
- FIT: upper bound on the freeze idea — if the drafter can be off-the-shelf, no decode-side
  training is needed. Include as the "zero-training" pole against Medusa/EAGLE/DSpark.
