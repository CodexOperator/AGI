---
id: idea:lm-abliteration-feature-differences-generalize-across-models
mint_id: d958b0dbda99457fa04124c4cb460e39
type: idea
parents:
  - goal:g14.9.1
next_edges: []
edited_by: director-thought
scaffold_hash: 4b8fd854ab844288
season: 2
title: "OWNER 16:2xZ 09-20: abliterate our own prod candidates (by us if by no one else) and extract the feature differences between abliterated and non-abliterated models to look for generalized patterns across models"
town: core
---
<!-- BODY:BEGIN -->
# idea:lm-abliteration-feature-differences-generalize-across-models

**Owner (16:2xZ 09-20, verbatim on goal:g14):** "if it's identical, my preference is always use the abliterated models over non-abliterated ones. So if any model is good enough to be used in prod at some point it would have to be abliterated. If not by anyone else then by us. We could extract the feature differences between abliterated and non-abliterated models and see if there are any generalized patterns across models."

**Two commitments in one line.** (1) A *capability*: the town must be able to abliterate any candidate itself — derive the direction, apply it at runtime, verify it is in the graph, measure the cost. (2) A *research question*: is the abliteration delta the same object across models — a shared feature with a recognisable signature — or a per-model accident?

**What is already measured (ABC.01, 09-20, this box).** OrcaBonsai's mechanism is one unit direction r (5120-d, diff-in-means on the BF16 base) projected out of 129 residual writers, `y ← y − α(y·r)r`, shipped as a rank-1 LoRA; on Bonsai 2 27B it is routed (scale 0 = base byte-identical, scale 3 collapses) and *does not touch coding* (141/164 HumanEval completions byte-identical to base at scale 1; −0.6 pp, p = 1.0). Their own capability deltas: MMLU +1.0, GSM8K −1.3, CMMLU −0.6. The direction does **not** transfer across hidden sizes (9B = 4096, 35B-A3B = 2048): any cross-model comparison needs a basis-independent signature.

**Candidate signatures that ARE comparable across models (each one a falsifiable claim):**
- **Unembedding signature.** Push r (per layer, or the late-layer mean) through the final norm and `lm_head`: the token set it promotes/suppresses. Models sharing a tokenizer family (Qwen3.5-0.8B/9B/35B-A3B, Qwen3.8-27B = Bonsai) can be compared by Jaccard of the top-k promoted tokens against a null of random unit directions (expected ≈ k/V ≈ 0).
- **Depth profile.** Where along normalised depth the projection magnitude ‖(y·r)r‖/‖y‖ peaks on refusal vs benign prompts; OrcaBonsai's own selfcheck reports the per-layer residual fraction.
- **Behaviour profile.** Refusal-rate drop per harm category and the over-refusal drop (XSTest-safe) at matched α — the shape of the drop, not its size.
- **Direction agreement under one recipe.** The same diff-in-means recipe on N paired prompts, run per model; agreement measured only through the signatures above, never raw cosine across bases.

**Cheapest tooling on this box (0 USD, no download):** llama.cpp's `llama-cvector-generator` extracts a per-layer mean-diff direction straight from a GGUF (quantized, on the GPU) and `--control-vector-scaled cv.gguf:−s` applies it as *negative steering* — additive, not a projection, so it is abliteration-lite; the true projection needs the rank-1 LoRA export (OrcaBonsai `scripts/export_gguf_lora.py`, needs the writer matrices — dequantise from the GGUF or the fp16 checkpoint). The first hypothesis uses the cvector path because it costs nothing and produces the directions the signature tests need; the LoRA path is the second hop if the first proves the direction is real.

**Chain (no hop longer than the evidence):** H1 own refusal direction on Qwen3.5-9B cuts refusals at no coding cost → H2 the unembedding signature is shared across the Qwen family (vs the random-direction null) → H3 the rank-1 projection (true abliteration) built from our own direction matches the shipped OrcaBonsai LoRA's behaviour on Bonsai 27B → H4 a second behaviour (verbosity, sycophancy) has a signature of the same shape, or refusal is special.

**Standing rule applied.** Every charter-table candidate row carries an `abliterated?` column; a candidate that is not, is not a prod candidate until H1/H3 give the town its own lever.
