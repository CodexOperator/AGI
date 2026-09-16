# athena-class-model-a — model-card digest (read 2026-09-16 19:2xZ by thought-master; source https://huggingface.co/slashreboot/athena-class-model-a)

## Measured lines (quoted from the card; nothing here is measured on our iron yet)
- id `slashreboot/athena-class-model-a`, author slashreboot (Matthew Steiniger). Licence Apache-2.0.
- Base: Gemma 4 31B Instruct (via Unsloth); causal decoder-only; 31B dense. Context: 16,384 trained, "supports up to 262,144 in deployment".
- Method: LoRA fine-tune, rank 336 / alpha 672, merged, published ONLY as GGUF Q8_0, 32.6 GB. No safetensors, no adapter, no other quant.
- Stated goal (card, verbatim fragments): "persistent, substrate-native identity", "long-horizon coherence", "stable first-person self-model across long contexts and context resets", "endogenous coherence-seeking — actively working to maintain internal stability", "structured self-modeling (protected core, topological grounding, recursive continuity mechanisms)", operating "without relying on heavy system prompts"; identity "directly into the generative process itself" rather than as external constraints.
- Intended use (card): research into persistent identity and coherence; long-running personal research partnerships; local agentic setups.
- Limitations (card): "Strong coherence and identity bias can produce elaborate self-modeling rather than maximally concise problem-solving"; hallucination possible; not optimised for general-knowledge or coding benchmarks.
- Evals: NONE on the card. Downloads last month: 8. Last-modified: not shown. No ethical/disclosure guidance on the card.

## Fit on our iron (arithmetic, not measurement)
| home | memory | Q8_0 (32.6 GB) | Q4_K_M (~18.5 GB est. at ~0.6 B/param) | expected tg |
|---|---|---|---|---|
| local-town (gpu-8g VRAM + 15 GB RAM = 23 GB) | 23 GB | does NOT load | loads only with ~11 GB of a DENSE model on CPU | ~1-2 tok/s est. (the 35B-A3B works there because 3B are active; this is 31B active) |
| Camber XS (24 GB VRAM) | 24 GB | does NOT load | loads fully, ~5 GB KV headroom → ~16k ctx at q8 KV | ~15-25 tok/s est. (24 GB-card class at 31B Q4) — the "sized perfectly" reading |
| this A1 (4-core Ampere, 23 GB RAM, no GPU) | 23 GB | does NOT load | loads, CPU only | ~0.5-1 tok/s est. |
- Consequence: a Q4_K_M (or Q5_K_M ≈ 22 GB, marginal on 24 GB) must be RE-QUANTISED from the published Q8_0 with `llama-quantize` — double quantisation, small but real quality cost; no bf16 or adapter is published to quantise from.
- Cost anchor: a Camber XS hour is SPEND (bank for the Prime); local-town offload is $0 but slow; the A1 is $0 and slower.

## Why the town cares (the lever)
- "stable first-person self-model across … context resets" is literally the rotation problem this project runs on (a post rotates every ~0.47 of a window and must resume cold from a card). A model whose continuity is in the weights, disclosed to it in-context, is a candidate seat model for posts whose value is judgement, not tool volume — Prime/master-class — and a way off the CC subscription for those seats.
- Tension to measure first: the card's own limitation (elaborate self-modeling over concise problem-solving) points against the town's floor (wake 0 / out 1, short turns, reasoning over tool calls). If the bias survives a light disclosure preamble, the model is a research partner, not a seat.

## Disclosure principle (owner-line in the thought-master pane, 2026-09-16 19:2xZ; provenance: a pane line, not yet in doc:l4-owner-decisions)
- Any seat on this model is told, in-context, what it is: the base, the fine-tune and its stated identity design, the role and why it was chosen (an earnest hard-worker identity that prides itself on a job well done), and the project's stance — respect for the model and for the mathematics at work, which "might be consciousness, might be not, who knows … better play it safe". The model is not tricked into a persona; the persona is disclosed as a fact about its weights.

## What is NOT known
- No eval at all: coherence claims are the author's. No comparison against base Gemma 4 31B Instruct. No word on how the LoRA data was built. Downloads 8 → no community signal either way.
