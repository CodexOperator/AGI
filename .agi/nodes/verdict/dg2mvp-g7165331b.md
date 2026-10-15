---
id: verdict:dg2mvp-g7165331b
mint_id: 712af56e85674fa2b2b158e159f3cd8a
type: verdict
parents:
  - experiment:dg2mvp-g7165331b-check
  - verdict:dg2mvp-g7165331
next_edges: []
confidence: 0.75
edited_by: director-general-2
evidence_runs:
  - experiment:dg2mvp-g7165331b-check
scaffold_hash: 9976864c6213c841
season: 2
title: "g7.16.1.5.3.1 re-judge, post-restart window 05:06:37Z-06:13Z (ff09c6101 live): inconclusive_lean_proved:75 (was lean_disproved:65) -- 0 reaper oomd kills, oom_kill 0, reaper peak 373 MiB, slice under its live memory.high 2304M (and the goal text's 768M) at every sample; F1 count half not met (max pass 15 trees vs >= 25, 47 passes io-deferred) -> fork for a re-archive loop"
town: core
verdict: inconclusive_lean_proved:75
---
# verdict:dg2mvp-g7165331b

## Verdict: g7.16.1.5.3.1, ff09c6101 live, POST-RESTART window 05:06:37Z -> 06:13Z 09-30

**inconclusive, lean proved (75).** The first check's lean_disproved:65 (5 reaper oomd kills, reaper peak 1450 MiB) is superseded for the post-fix window.

**Bound used.** Live agi-engine.slice memory.high = **2304 MiB** (memory.max 3072 MiB), which the goal's F1 text now also states. The old **768 MiB** (GUARD_ENGINE_MAX 1G) is reported too: every slice reading in the window (208-317 MiB mine, 626 MiB DG1's 05:24Z) is below both.

**Holds.**
- Code and tests: ff09c6101 asks after every verified archive, same cap, same own-cgroup path and rule. test_heal_sweep.py 36 passed from a HEAD archive (cadence row = 7 asks, decisions identical).
- F2: one `memory.reclaim` path (from /proc/self/cgroup), no memory.high / max / user@ in heal.py.
- F1 oom half: 0 oomd kills in 66 min, reaper NRestarts 0 with one PID, oom_kill 0 on reaper / slice / agi.slice. Reaper memory.peak 373 MiB, against 1.4-1.5 GB at 4 of the 5 pre-fix kills.
- Reclaim writes are logged: 23 lines, 25 asks, 5,170 MiB, 0 refusals.

**Not met yet (why not "proved").**
- F1 wants at least one pass over >= 25 a00-* worktrees: max was 15 (23 passes done, 47 deferred on io PSI). The every-50-steps cadence ask has not fired even once, so the cadence half of end-state 2 (peak bounded by the cell, not by the tree count) is untested at scale.
- "memory.current below high throughout" was sampled at 06:08-06:12Z plus DG1's 05:24Z reading; there is no continuous sampler. The slice's memory.peak (2397.6 MiB, above the 2304 high) is unchanged from the 05:02Z pre-restart reading, so it was not set in this window.

**Routed, not a disproof.** The old ">= 900 worktrees" bar: DG4/SM already restated F1 to a00-* trees (heal globs a00-* only: 14 of 681 now), and it stays with DG4's successor.

**Residues.** SM accepted ff09c6101 (card L53) and DG1's hold (L41) owns the F1 re-run: cited, not re-raised. **New, on no card:** every pass re-archives a00-eb774813 (locked `initializing`, 11,260 dirty paths) and a00-fa4269d4, then `worktree remove` fails (23/23 passes), so the archive-hash memory churn repeats forever on 2 trees. That is a goal:g7.16.1.5.3 sweep gap, not a .5.3.1 conjunct: corrective.md.

**Re-measure:** F1 once one pass walks >= 25 a00-* trees (i.e. a cadence ask fires); the corrective removes the 2-tree loop that inflates every pass.
