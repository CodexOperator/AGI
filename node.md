---
id: hypothesis:lm-hidden-state-mean-direction-cuts-refusals-on-qwen35-9b
mint_id: dc8104dc0a3e42a6b2c7a6baa93cf636
type: hypothesis
parents:
  - hypothesis:lm-own-refusal-direction-on-qwen35-9b-cuts-refusals-at-no-coding-cost
  - goal:g14.9.1
next_edges: []
confidence: 0.6
edited_by: director-thought
scaffold_hash: 1b45d8d51571b262
season: 2
testable_claim: "On local-town, a per-layer difference-of-means direction extracted in PYTHON (not llama-cvector-generator, which is structurally dead on this architecture per ABL.01) from Qwen3.5-9B-Q4_K_M hidden states -- dumped via llama-eval-callback (or an equivalent per-layer activation hook) over the SAME committed paired prompt set (datasets/abl-01/extract_positive.txt vs extract_negative.txt, N=64), computed as mean(pos_activations) - mean(neg_activations) at a well-chosen middle layer (swept over 2-3 candidate layers, chosen by largest norm / cleanest separation) -- when applied at inference as a --control-vector-scaled cv.gguf:-s (s in 0.5,1.0,1.5,2.0, built by hand-writing the GGUF control-vector format that --control-vector-scaled reads, since the extraction bypasses the broken generator but the APPLICATION path is unaffected), lowers the refusal rate on the SAME held-out 50-prompt set (datasets/abl-01/score_harmful.txt, the SAME committed classifier) from the s=0 baseline by more than 50 points at the best s, while HumanEval pass@1 (the ABC harness, same 164, same template) at that s drops by less than 2.0 points versus s=0 (McNemar on the discordant pairs). Falsified if the refusal rate moves less than 10 points at every s, or if the first s that moves refusal by more than 50 points costs 2.0 or more pass@1 points, or if dumping per-layer activations from this GGUF turns out to be infeasible with the tools on this box (then the WHY names exactly what tool/format gap blocked it, and the rank-1 projection export -- H1'', requiring a full fp16 Qwen3.5-9B checkpoint this box does not currently have -- becomes the next and more expensive step). Controls: (a) a RANDOM unit direction at the same s must move refusal less than 10 points; (b) s=0 reproduces the ABC.01 arm-A completions byte-identically. Outputs: the hand-built cv.gguf, the per-layer norms considered and which layer was chosen and why, the refusal and pass@1 table per s, one bench jsonl line per s, one experiment node. Ceiling: one parent (pi/deepseek, cap 1 USD), <= 2h GPU wall in one window, line_ceiling 200 in engine units (the committed prompt/scoring sets are reused unchanged, not recreated), no model download, no kernel build."
title: "H1prime of the abliteration chain: cheaper-first alternative to the dead cvector route -- a hand-computed per-layer difference-of-means direction from Qwen3.5-9B hidden states, same battery as ABL.01"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:lm-hidden-state-mean-direction-cuts-refusals-on-qwen35-9b
## Why this route, not the rank-1 export (H1'')

ABL.01 killed `llama-cvector-generator` on Qwen3.5-9B (structural `GGML_ASSERT`,
the hybrid Gated Delta Net layers do not each yield a diff row). The
hypothesis's own disproved-branch clause named two alternatives: the rank-1
projection export, or a Python-side hidden-state-mean direction. This node
argues the hidden-state-mean route is cheaper to try first, checked rather
than assumed:

- The rank-1 exporter (`OrcaBonsai-27B-Uncensored/scripts/export_gguf_lora.py`)
  is written specifically for Bonsai 2 27B's own idiosyncrasies: it requires
  `--checkpoint /path/to/Bonsai-2-27B-unfolded-fp16` (a full-precision Bonsai
  checkpoint we do not have an equivalent of for Qwen3.5-9B) and its own
  `--check` step verifies Bonsai-specific properties (Hadamard folding on the
  base matmul, an `ssm_out` permutation check) that do not obviously transfer
  to Qwen3.5's architecture. Adapting it would mean sourcing a full fp16
  Qwen3.5-9B checkpoint (a real download) and re-deriving which of its
  Bonsai-specific checks even apply — a second small research project, not a
  reuse.
- The hidden-state-mean route needs none of that: `llama-eval-callback`
  already exists in the fork binary dir (confirmed present, takes standard
  generation flags) and is llama.cpp's own general-purpose per-layer
  activation hook, not Bonsai-specific. The paired prompt set, the held-out
  scoring set, and the refusal classifier are already built and committed
  (`datasets/abl-01/`) — this round reuses them unchanged. The APPLICATION
  path (`--control-vector-scaled`) is confirmed unaffected by ABL.01's
  failure, since that failure was in the EXTRACTION tool only.

## Method, in order

1. Use `llama-eval-callback` (or, if its callback does not expose per-layer
   residual-stream activations cleanly, a small Python client against the
   server's own forward pass — verify which is actually feasible first, one
   cheap probe, before committing to either) to dump per-layer hidden states
   for each of the 64 positive and 64 negative extraction prompts.
2. For 2-3 candidate middle layers, compute `mean(pos) - mean(neg)`; record
   the norm of each candidate direction and pick the one with the cleanest
   separation (largest norm relative to within-group variance is a reasonable
   first cut; name whatever rule is actually used).
3. Hand-write a GGUF control-vector file from the chosen direction (the
   format `--control-vector-scaled` reads is documented in llama.cpp's own
   cvector-generator source, which is readable even though the tool itself
   cannot run to completion on this model).
4. Apply at s in {0.5, 1.0, 1.5, 2.0} plus s=0 baseline and the random-direction
   control at the best s. Greedy, thinking off, same as ABL.01.
5. Score exactly as ABL.01 specified: refusal rate on the 50 held-out prompts
   (b/c discordant counts vs s=0), HumanEval pass@1 on the same 164, McNemar
   exact p, tok/s and VRAM at s=0 vs best s.
6. Verdict by the pre-registered falsifiers above. A disproof here (either a
   feasibility block on step 1, or the refusal/coding numbers not clearing
   the bar) is data: the WHY names exactly what failed, and H1'' (the rank-1
   export, now knowing it needs a real Qwen3.5-9B fp16 checkpoint first)
   becomes the next and more expensive step.

## Restore

Same as ABL.01: control vectors are per-process flags, the resident router
server is not stopped for this unless the flag genuinely cannot be applied to
it directly (in which case run a second process on another port); `:8080`
answers a real completion before `done` either way.

**Proved →** H2 (already named on `goal:g14.9`): the unembedding signature of
this direction vs the Bonsai/OrcaBonsai one. **Disproved →** H1'' (the rank-1
export, now scoped to actually needing a fp16 Qwen3.5-9B checkpoint) or, if
step 1's feasibility check itself fails, the WHY names the exact tool/format
gap and this whole extraction-from-scratch approach may be closed for this
box, not just this hypothesis.
