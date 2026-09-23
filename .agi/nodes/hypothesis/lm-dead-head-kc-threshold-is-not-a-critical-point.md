---
id: hypothesis:lm-dead-head-kc-threshold-is-not-a-critical-point
mint_id: 5aa55c767a5a4ad0b1b3fc3a43669278
type: hypothesis
parents:
  - goal:g5.22
next_edges: []
edited_by: director-thought
scaffold_hash: 99cdf14b838ed14a
season: 2
testable_claim: "On the bundled artifact data/qwen25_05b_head336_small_theory_redundancy_v2_boundary2.json (468 KB) of project-89/coherence-guided-dead-head-identification @583962f (PolyForm-NC, research use; NOT on this box -- re-clone is the first cost, ~2 MB), sweeping the threshold chi over 0.2..4.0 and computing dead-precision, safe-recall and Spearman(z_h, delta_loss) over the 336 heads shows NO discontinuity at chi = 0.96025: precision and recall change by < 0.05 across chi in [0.90, 1.02] and Spearman(z_h, delta_loss) is < 0.35 in magnitude (the prior critic computed +0.268, base-rate lift ~1.0001, worst head z = -0.078). Falsified if precision or recall jumps by >= 0.15 within that window (a knee) or |Spearman| >= 0.5 (coherence genuinely ranks damage) -- then the Kuramoto/BKT framing is alive and head pruning by coherence proceeds on Qwen3.5-9B next; proved (the null) means coherence is NOT a pruning criterion and the next chunk prunes heads by measured delta_loss / GQA group-death yield instead (judge rank 12), with the oscillator budget released. ~10 lines of python3, any CPU, one bench jsonl line + one experiment node; no model download, no GPU."
title: "TRACK I chunk 1 (owner 21:4xZ: oscillator technique first, no spikes, prune heads; the 09-20 judge rank 1, 5 CPU-min, 0 USD): the dead-head coherence threshold K_c = 0.96025 is a label on a smooth head ranking, not a critical point -- the kill-test that gates every oscillator/coherence pruning step"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:lm-dead-head-kc-threshold-is-not-a-critical-point

## Hypothesis

**CLAIM.** On the dead-head paper's own bundled Qwen2.5-0.5B artifact (336 heads, each with its mean write-back/residual cosine z_h and its single-head ablation delta-loss), the threshold chi_c = 0.96025 is a label on a smooth head ranking, not a critical point: swept over 0.2..4.0, dead-precision and safe-recall change smoothly through 0.96. What decides whether coherence is a usable pruning criterion is the ranking's lift over random selection, not the threshold.

**TESTS** (CPU only, no model is loaded -- the bundled JSON is the whole input):
- T1 reproduce: recompute the artifact's 157/336 dead and 95.5 pct precision exactly from the JSON (sanity; a mismatch stops the round).
- T2 sweep: chi_c over 0.2..4.0 in 0.02 steps -> dead count, dead-precision, safe-recall (the artifact's own safe/unsafe labels); table + plot data.
- T3 knee: a breakpoint fit at 0.96 against a smooth fit on both curves; KNEE iff the breakpoint model wins by delta-BIC >= 10 AND the max-curvature point lies within +/-0.1 of 0.96.
- T4 ranking: Spearman(z_h, delta-loss) over the non-protected heads; lift over random = precision at the paper's dead count vs the mean of 10,000 random same-size draws from the non-protected pool.

**FALSIFIERS.**
- (a) the claim: a KNEE at 0.96 on either curve (T3) -> K_c is a critical point after all; the claim is disproved and the oscillator threshold gains standing.
- (b) the pruning criterion (goal:g5.22 falsifier (a)): no knee AND lift <= 1.05 AND |Spearman| < 0.3 -> coherence is falsified as a pruning criterion; pruning proceeds by measured delta-loss per GQA group and the oscillator budget is released.
- (c) otherwise (lift > 1.05 or |Spearman| >= 0.3, knee or not): coherence stands as a one-pass ranking -> chunk 2 = z_h in one CPU forward pass on the served 9B, and its GQA-group yield.

**FILE SCOPE.** Scripts under .agi/context/local-maxxing/heads/ (paths as paths.local_maxxing.* keys, owner 08:4xZ); the fetched artifact (source URL + sha256 recorded) and the sweep outputs under datasets/dead-head/; one experiment node under this hypothesis; nothing under extensions/.

**CEILING.** 0 USD compute; pi deepseek parent + ONE kid, cap 1 USD; orders wall 60 min; no GPU and no model load, so not a model-loading host kid.

**Planned by** thought-master 09:4xZ 09-23 (owner 09:4xZ asked for the oscillator head pruning specifically; the 09-20 order put it first; digest: .agi/context/local-maxxing/papers/dead-head.md).

## Agent Notes
director-thought, BIGGER frame after the proved verdict (a scratch recount over the same pinned artifact, not a round): does ANY one-pass per-head score in the artifact rank ablation damage where coherence does not? Spearman vs delta_loss over the 291-head pool: activation_score +0.404, mean_cosine +0.289, min_cosine +0.288, structural_bridge -0.198, structural_lambda2 -0.191, structural_score -0.187, structural_bandwidth -0.104, layer +0.063, death_persistence +0.059, magnitude_score -0.026, delta_coherence +0.012. None reaches 0.5, so no cheap proxy replaces measurement on this artifact; chunk 2 measures delta-NLL directly on the served 9B (hypothesis:lm-served-9b-drops-6-of-32-kv-groups-at-1pct-nll, OSC.02), which costs about one GPU minute per group.
