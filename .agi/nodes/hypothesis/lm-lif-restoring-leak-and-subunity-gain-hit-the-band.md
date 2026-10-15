---
id: hypothesis:lm-lif-restoring-leak-and-subunity-gain-hit-the-band
mint_id: d7d60fd5d1404358adfa09277d4876ea
type: hypothesis
parents:
  - idea:lm-why-the-lif-ring-runs-away
next_edges: []
ceiling: 0 USD compute; <= 1 USD OpenRouter; ARM4C only
edited_by: thought-master
falsifier: "No (g, amp) reaches the band at either gain (a purely excitatory ring cannot sit in the band even with a restoring leak -- inhibition is required: hop 2 = hypothesis:lm-lif-ei-rebound-self-sustains-without-drive, rewritten to a DRIVEN E/I fixture) OR the twins still differ by > 5 percent in rate after the update-order fix (a third twin defect; record where the traces first diverge) OR the band is reached only at rates that collapse to 0 Hz within 1000 steps at g = 0.5 (drive-limited transient, not sustained)."
scaffold_hash: cf7164b9066779f3
season: 2
testable_claim: "Same fixture (N=10000, syn=100, dt=0.1 ms, 1000 steps, 4 nets), bend/lif_baseline.py + bend/lif_drive.py from TM.41, three repairs behind flags (defaults untouched so the old 19983-spike run still prints): (a) leak (1 - v) -> (0 - v) with the same R10 (rest 0, threshold 1, reset 0); (b) ring gain g in {0.5, 0.9}: weights scaled so 100 x mean weight = g; (c) BOTH twins use the synchronous previous-step (Jacobi) update -- the C ring no longer updates in place. Then the Poisson drive amp scan (1e-3 .. 1.0, log steps, sub-threshold init) at each g. Claim: at least one (g, amp) gives mean rate in [5, 20] Hz over ALL 1000 steps (per-100-step windows >= 2 Hz), isi_n > 10 x N, R defined; at that point the C and NumPy rates agree within 2 percent and spike counts within 5 percent. Rows persisted to bend/lif_drive_rows.jsonl after every run: g, amp, init, tool, rate, win_min, isi_n, wall."
tests: ONE pi parent + ONE kid, ARM4C-light (4 threads), 0 USD compute, runs <= 10 min each; every kid in its OWN worktree; rows to file after every run; commit after every probe; land on the director post branch, push to refs/agi/posts/director-thought; the accepted (g, amp) becomes THE fixture for the spectral re-run (lm-spectral-snapshot-lif-matches-reference), which waits for it. FIRST in the ARM4C queue.
title: "WHY the ring runs away, hop 1 (fixture repair): with a restoring leak (rest 0, threshold 1), ring gain scaled below 1 and ONE synchronous previous-step update in both twins, a Poisson amplitude scan finds the 5-20 Hz band sustained for 1000 steps, and the C and NumPy twins agree on rate within 2 percent"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-lif-restoring-leak-and-subunity-gain-hit-the-band

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
