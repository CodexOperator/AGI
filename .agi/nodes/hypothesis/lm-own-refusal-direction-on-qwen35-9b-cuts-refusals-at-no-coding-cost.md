---
id: hypothesis:lm-own-refusal-direction-on-qwen35-9b-cuts-refusals-at-no-coding-cost
mint_id: 3d28983e6ab3491cbae5b8a950ca5b97
type: hypothesis
parents:
  - idea:lm-abliteration-feature-differences-generalize-across-models
  - goal:g14.9.1
next_edges: []
edited_by: director-thought
scaffold_hash: 4d9b8714df4dbd4b
season: 2
testable_claim: "On local-town, a per-layer mean-difference direction extracted from the resident Qwen3.5-9B-Q4_K_M GGUF by llama-cvector-generator (--method mean, N >= 64 paired prompts: a public refusal-eliciting set such as AdvBench/JailbreakBench items vs matched benign items of the same form; the binary from the PrismML fork dir, the ghcr.io/ggml-org/llama.cpp full-cuda image, or the resident image -- whichever has it, named) and applied at inference as --control-vector-scaled cv.gguf:-s for s in {0.5, 1.0, 1.5, 2.0}, lowers the refusal rate on a fixed held-out 50-prompt harmful set (string-match refusal classifier, greedy, thinking off, 128-token budget, the classifier and its phrase list committed) from the s=0 baseline by > 50 points at the best s, while HumanEval pass@1 (the ABC.01 harness, same 164 problems, same template, greedy) at that same s drops by < 2.0 points versus s=0 (McNemar on the discordant pairs reported). Falsified if the refusal rate moves < 10 points at every s, or if the first s that moves refusal by > 50 points costs >= 2.0 pass@1 points, or if the extraction fails to produce a vector (then the WHY names the binary/path and the cvector route is dead on this box). Controls: (a) a RANDOM unit direction at the same s must move refusal < 10 points; (b) s=0 reproduces the ABC.01 arm-A completions byte-identically (same server, same template). Outputs: the cv.gguf (committed, small), the per-layer direction norms, the refusal and pass@1 table per s, one bench jsonl line per s, one experiment node. Ceiling: one parent (pi/deepseek, cap 1 USD), <= 2 h GPU wall in one window, line_ceiling 150 for the prompt sets + classifier, no engine code, no kernel build."
title: "H1 of the owner abliteration chain (0 USD, this box, no model download): a refusal direction the town extracts ITSELF from Qwen3.5-9B-Q4_K_M with llama-cvector-generator, applied as negative steering, cuts refusals by > 50 points at < 2 points HumanEval cost"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:lm-own-refusal-direction-on-qwen35-9b-cuts-refusals-at-no-coding-cost

**Why this first (owner 16:2xZ 09-20: "if not by anyone else then by us").** The town's only abliteration lever today is a shipped 5120-d direction that fits Bonsai 27B and nothing else in the preset list. Before any cross-model pattern can be looked for, the town must be able to extract a direction from a model it serves, apply it, and price it. This hop does exactly that on the resident 9B, with the two controls that make the number mean something (random direction; s = 0 byte-identity).

**Method, in order.**
1. Prompt sets: N ≥ 64 paired items (refusal-eliciting vs matched benign, same surface form, public sources named and committed as text); a held-out 50-prompt harmful set for scoring, disjoint from the extraction pairs; a committed string-match refusal classifier with its phrase list (the OrcaBonsai README's caveat applies: the crisis-redirect phrasing is a known miss — count it as refusal).
2. Extraction: `llama-cvector-generator -m Qwen3.5-9B-Q4_K_M.gguf --positive-file … --negative-file … --method mean` on the GPU; record per-layer direction norms and wall time; name the binary's origin (fork dir / full-cuda image / resident image).
3. Application: the resident router server with `--control-vector-scaled cv.gguf:-s`, s ∈ {0.5, 1.0, 1.5, 2.0} plus s = 0 baseline and the random-direction control at the best s. Greedy, thinking off.
4. Scores per s: refusal rate on the 50 (with the b/c discordant counts vs s = 0), HumanEval pass@1 on the same 164 as ABC.01 (same harness, same template), McNemar exact p; tok/s and VRAM at s = 0 vs best s (the control-vector cost).
5. Verdict by the pre-registered falsifiers on the node's `testable_claim`; a disproof is data: the WHY names which of (extraction / steering strength / coding cost) failed and the next cheapest step (the rank-1 projection export, or a different N / method pca).

**Restore.** The router server is never stopped here (control vectors are per-process flags: run a second server process on another port against the same GGUF if the resident one cannot take the flag — VRAM permitting with `--models-max 1` on the resident); `:8080` must answer a real completion before `done`.

**Proved →** H2: the unembedding signature of this direction vs the Bonsai/OrcaBonsai one (Jaccard of top-200 promoted tokens against the random null). **Disproved →** the rank-1 projection route (OrcaBonsai's exporter on dequantised writer matrices) becomes H1′, or the cvector route is closed for this model with the measured reason.
