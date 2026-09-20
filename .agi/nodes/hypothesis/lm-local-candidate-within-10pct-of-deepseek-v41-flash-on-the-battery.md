---
id: hypothesis:lm-local-candidate-within-10pct-of-deepseek-v41-flash-on-the-battery
mint_id: b59febbe54794c3a947f82a9690cb4ec
type: hypothesis
parents:
  - goal:g14
next_edges: []
edited_by: thought-master
scaffold_hash: 427688da6364be01
season: 2
testable_claim: "On the same two evals, same protocol (greedy, thinking off, one sample, the ABC harness for HumanEval 164 with execution pass@1; IFEval 541 prompts scored by the official strict prompt-level accuracy, harness in a scratch venv), the reference deepseek/deepseek-v4.1-flash via OpenRouter (temperature 0, cap 1 USD for both evals) scores X_he and X_if, and the best local candidate among {B = Bonsai 2 27B PTQ1_0 at the 64K 8 GB line, C1 = B + OrcaBonsai LoRA scale 1, A = Qwen3.5-9B Q4_K_M} scores within 10 pct RELATIVE of the reference on BOTH evals (local >= 0.9 x reference on each). Falsified on any eval where every local arm is below 0.9 x reference; the gap table (arm x eval, absolute and relative, with the paired discordant counts vs the reference on HumanEval) is the deliverable either way and lands in datasets/switch-rule/<date>/ with the completions. A proof does NOT switch the town by itself: it is the trigger for the mvp that ties the contributing chains together (owner rule), which the master mints. Expected from ABC.01: B 86.6 pct / C1 86.0 pct / A 78.0 pct on HumanEval; deepseek-v4.1-flash unknown -- that is the point."
title: "SWITCH-RULE MEASUREMENT (owner 21:5xZ 09-20): is the best local candidate (Bonsai 2 27B + abliteration LoRA, or the 9B) within 10 pct of deepseek-v4.1-flash on the agreed battery (HumanEval pass@1 + IFEval strict prompt accuracy)? Chunk 1 = the missing reference row + the gap table"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:lm-local-candidate-within-10pct-of-deepseek-v41-flash-on-the-battery

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
