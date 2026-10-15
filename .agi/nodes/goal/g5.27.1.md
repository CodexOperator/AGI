---
id: goal:g5.27.1
mint_id: 0f25fdd69fcb424eb7e424dcfefcb19d
type: goal
parents:
  - goal:g5.27
next_edges: []
confidence: 0.8
edited_by: belam
goal_id: G5.27.1
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: 53e978ec6278029e
season: 2
seeds:
  - hypothesis:lm-local-candidate-within-10pct-of-deepseek-v41-flash-on-the-battery
status: active
tags:
  - local-maxxing
  - switch
  - battery
title: "G5.27.1: THE BATTERY + REFERENCE -- HumanEval + IFEval scored identically for every local candidate and for deepseek-v4.1-flash, the gap table that decides standing (owner 21:5xZ 09-20)"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# goal:g5.27.1

## Agent Notes
**Owner source (2026-09-20 21:5xZ, verbatim on goal:g14, relayed via goal:g5.27):** "if any of these ideas pan out let the chain mint an mvp that ties all the different chains together that contributed and make a build node and start using it. So start using our own you to run your own kids and parents if performance starts approaching within %10 of deepseek v4.1 flash bench performance." Trajectory (21:4xZ): "overall trajectory is maximize evaluation performance on the local model."

**Commits to.** The first half of G5.27's commitment: build the actual gap table, not just the rule for reading one. Score deepseek-v4.1-flash (the reference, via OpenRouter, temperature 0, one sample) on the SAME two evals every local candidate has already been measured on where possible — HumanEval 164 (execution pass@1, the ABC harness, same template) and IFEval 541 (official strict prompt-level accuracy) — then build the gap table (candidate x eval, absolute and relative, paired discordant counts vs the reference where the eval supports pairing) against the five local rows already measured in ABC.01/ABC.02 (A, A2, B, C1, C2). This chunk is measurement only: it does not call the switch, does not mint an mvp, and does not touch the GPU (the reference row is API-only; a local candidate's IFEval row, if still missing, is a separate later chunk under this same subgoal).

**Invariants.** Every eval uses the identical protocol already established for the local rows (greedy, thinking off, one sample, same request shape); the gap table is the only place a candidate's standing is read from, never a single number quoted alone; USD and tok/s ride along on every row so cost is never separated from capability; a proof of "within 10 pct" is a trigger, never a switch by itself.

**Falsifiers.** (a) If the reference itself cannot be scored cleanly on one of the two evals (rate limits, a harness mismatch, a template confound) the WHY names exactly which eval and why, and that eval is held missing from the gap table rather than estimated. (b) If every local candidate sits below 0.9x the reference on either eval, the switch does not fire this round — recorded as a real gap, not hidden, and G5.27's own falsifier (b) starts counting toward "no candidate reaches 90pct after G5.22/7/9 each land a chunk."

**Done when.** The gap table exists in `datasets/switch-rule/<date>/` with real numbers on both evals for the reference and every local candidate measured so far, and the switch verdict (fires / does not fire, per row) is stated plainly on the hypothesis node.

**First chunk (minted):** `hypothesis:lm-local-candidate-within-10pct-of-deepseek-v41-flash-on-the-battery` (SWR.01) — the reference row + the gap table against the five existing local rows. G5.27.2 (the mvp/build/switch mechanics) is minted only when a switch verdict actually needs to be acted on, per the owner pace rule.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
owner ask 2026-09-21: renumber local-maxxing research g5.27.1 → g5.27.1 (g5 continuation after g5.21; mint_id preserved; town:local-maxxing kept); no director assignment
<!-- THOUGHT:END -->

SWR-B.03 landed (director-thought): arm B IFEval scored 541/541, strict 0.778189 (421/541) vs threshold 0.781886 (423 needed) -- does NOT fire, short 0.37pp, inside the +/-0.4pp unseeded-langdetect floor (mur-confirmed: 10 independent re-runs on the committed file gave 420x6/421x3/422x1, so 0.778189 is one valid sample of that floor, not fabricated). Loose 0.815157, instruction-level 0.851319. gap_table.md row landed under experiment:a00-4eec4fce-e9b330 (kid); experiment:a00-5f73ccd9-bc9dc8 (kid) is the mid-round generation step, verdict pending by design (superseded by the completing kid, not still-open work). Arm B: FIRES on HumanEval (92.2pct rel), does NOT fire on IFEval (89.57pct rel) -- two-eval hypothesis not satisfied by arm B alone; C1/C2 IFEval still unmeasured. mur-director-thought/swr-b-03: accept_with_residue, 1 confirmed residue (stale resume path in the pending kid, fixed post-review), 1 refuted (llama-server restore wording), 1 note (stale gap_table.md provenance header, fixed). No demotion.
