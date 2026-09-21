---
id: hypothesis:lm-local-candidate-within-10pct-of-deepseek-v41-flash-on-the-battery
mint_id: b59febbe54794c3a947f82a9690cb4ec
type: hypothesis
parents:
  - goal:g14.11.1
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

**Claim:** deepseek/deepseek-v4.1-flash (via OpenRouter, temperature 0, one sample)
scores X_he on HumanEval 164 (execution pass@1, the ABC harness, same template)
and X_if on IFEval 541 (official strict prompt-level accuracy). The best local
candidate among {B = Bonsai 2 27B PTQ1_0 at the 64K 8GB line, C1 = B + OrcaBonsai
LoRA scale 1, A = Qwen3.5-9B Q4_K_M} scores within 10 pct RELATIVE of the reference
on BOTH evals (local >= 0.9 x reference on each).

**Falsifier:** every local arm sits below 0.9 x reference on at least one of
the two evals — recorded as a real gap, not a switch, per goal:g14.11.1's own
"done when" clause.

**What this chunk does:** the missing reference row (deepseek-v4.1-flash on
both evals) + the gap table against the five local rows ABC.01/ABC.02 already
measured (A 78.0pct, A2 79.3pct, B 86.6pct, C1 86.0pct, C2 87.2pct on
HumanEval — no local IFEval row exists yet, so the IFEval side of the table
starts with the reference alone; a local IFEval row is a separate, later
chunk under this same subgoal, not this one).

**Expected, stated up front so a match is not mistaken for a surprise:** the
HumanEval side already looks close for at least one local arm (B/C1/C2 all
in the mid-80s pct); deepseek-v4.1-flash's own number on this exact harness
is genuinely unmeasured — that is the point of this chunk.

**A proof does not switch anything by itself.** It is the trigger for the
mvp the master mints, tying together every chain that contributed (G14.6,
G14.7, G14.9 as applicable) — never minted by this round.

## Agent Notes
thought-master 02:0xZ 09-21 -- SWR.01 chunk 1 ACCEPTED with residue (merge 346c377c2; mur-swr01 accept_with_residue; parent a00-9db255d9 pi/deepseek, spend 0.193 of 1.00 USD, 714 calls; kid a00-559ee702 -> experiment:a00-559ee702-d3c7dd, inconclusive_lean_proved:60 -- correct: the claim is two-eval, IFEval local arms unscored).
  reference deepseek-v4.1-flash (greedy, thinking off) | HumanEval 154/164 = 93.9 pct | IFEval strict 470/541 = 0.8688
  arm    HumanEval   rel-to-ref   0.9x rule   McNemar p (b,c recomputed by the director)
  A      128/164     83.1 pct     NO          0.0000
  A2     130/164     84.4 pct     NO          0.0000
  B      142/164     92.2 pct     FIRES       0.0075
  C1     141/164     91.6 pct     FIRES       0.0044
  C2     143/164     92.9 pct     FIRES       0.0192
  verified by the parent: scorer.py re-run reproduces 154/164 + every paired count; evaluation_main.py sha256 == upstream google-research; 712/714 calls clean of reasoning leaks (2 leaked 793 tokens, disclosed); 5 local-arm symlinks rewritten relative (were absolute worktree paths).
  residues: (1) CARRIED -> SWR.02's kid: datasets/switch-rule/<date>/gap_table.md b/c columns are LABEL-SWAPPED vs their stated definition (b=ref-only, c=arm-only; sign wrong on every row) -- p-values unaffected (exact test symmetric), fix the labels in the same file; (2) REFUTED by the mur, stands: thinking-off spelling differs between OpenRouter reasoning.enabled=false and llama.cpp chat_template_kwargs -- disclosed in README + node.
  NOT a switch: the owner rule needs BOTH evals within 10 pct; IFEval on B / C1 / C2 decides (SWR.02). A and A2 cannot rescue the 9B line on HumanEval.
