---
id: hypothesis:lm-dead-head-kc-threshold-is-not-a-critical-point
mint_id: 5aa55c767a5a4ad0b1b3fc3a43669278
type: hypothesis
parents:
  - goal:g5.22
next_edges: []
edited_by: thought-master
scaffold_hash: 99cdf14b838ed14a
season: 2
testable_claim: "On the bundled artifact data/qwen25_05b_head336_small_theory_redundancy_v2_boundary2.json (468 KB) of project-89/coherence-guided-dead-head-identification @583962f (PolyForm-NC, research use; NOT on this box -- re-clone is the first cost, ~2 MB), sweeping the threshold chi over 0.2..4.0 and computing dead-precision, safe-recall and Spearman(z_h, delta_loss) over the 336 heads shows NO discontinuity at chi = 0.96025: precision and recall change by < 0.05 across chi in [0.90, 1.02] and Spearman(z_h, delta_loss) is < 0.35 in magnitude (the prior critic computed +0.268, base-rate lift ~1.0001, worst head z = -0.078). Falsified if precision or recall jumps by >= 0.15 within that window (a knee) or |Spearman| >= 0.5 (coherence genuinely ranks damage) -- then the Kuramoto/BKT framing is alive and head pruning by coherence proceeds on Qwen3.5-9B next; proved (the null) means coherence is NOT a pruning criterion and the next chunk prunes heads by measured delta_loss / GQA group-death yield instead (judge rank 12), with the oscillator budget released. ~10 lines of python3, any CPU, one bench jsonl line + one experiment node; no model download, no GPU."
title: "TRACK I chunk 1 (owner 21:4xZ: oscillator technique first, no spikes, prune heads; the 09-20 judge rank 1, 5 CPU-min, 0 USD): the dead-head coherence threshold K_c = 0.96025 is a label on a smooth head ranking, not a critical point -- the kill-test that gates every oscillator/coherence pruning step"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:lm-dead-head-kc-threshold-is-not-a-critical-point

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
