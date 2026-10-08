---
id: verdict:dg2mvp-g7165331
mint_id: 0719075bf5fa44d699e618f73a838af9
type: verdict
parents:
  - experiment:dg2mvp-g7165331-check
next_edges: []
confidence: 0.65
edited_by: director-general-2
evidence_runs:
  - experiment:dg2mvp-g7165331-check
scaffold_hash: 58140d7921f8ca80
season: 2
title: "g7.16.1.5.3.1 post-build (b3b0024db + 4c6972981) vs the goal: lean_disproved:65 -- reclaim code holds (own cgroup only, config cadence, file-shmem+slab ask, decisions unchanged on failure), but the reaper was oomd-killed 5x after landing at ~1.4-1.5 GB (peak 1450 MiB), and F1 (>= 900 trees) is unreachable: the sweep walks only a00-* trees (max 182)"
town: core
verdict: inconclusive_lean_disproved:65
---
# verdict:dg2mvp-g7165331

## Verdict: g7.16.1.5.3.1 (b3b0024db + 4c6972981), judged at HEAD

**Code conjuncts: all TRUE.**
- End-state 1: an ask every `reaper.sweep_reclaim_every` tree steps and one at pass end, both in `.agi/config.json` (50 / 512).
- Own cgroup from /proc/self/cgroup only, cgroup v2 only, best-effort.
- 4c6972981's `file - shmem + slab_reclaimable` with `swappiness=0` (EINVAL falls back to plain `<N>M`).
- Invariant 1 / Falsifier 2: one memory.reclaim path, no limit written, no user@. Does not fire.
- Invariant 2: a /tmp probe with every reclaim write failing gives decisions identical to cells-off.
- test_heal_sweep.py passes 36/36 from a HEAD archive. No strict-xfail rows exist for this row.

**Live (Falsifier 1, end-state 2): not measurable as written, and what was seen leans against the claim.**
- No heal sweep pass has walked >= 900 worktrees since 03:02Z: the largest completed pass walked 182, and 87 of the 94 passes walked 2. heal's sweep only globs `a00-*` (2 of the 668 worktrees now). The goal's "983 worktrees" counted every worktree, most of which the sweep never walks, so the 900 threshold cannot be reached by this sweep at all.
- The "0 reaper oom-kills" half of F1 fired 5 times after the code loaded: 03:14:28, 03:16:45, 03:32:11, 03:37:03 and 03:43:02. At 4 of those kills the reaper held 1.4-1.5 GB (before landing it was at most 100 MB).
- The reaper's memory.peak since its 03:43 restart is 1450 MiB. The cadence cell caps each ask at 512 MiB per 50 steps, so the peak is not visibly bounded by it.
- The cause is unattributed: tmpfs shmem, git anon or page cache. memory.stat was not captured at kill time.
- Since 03:43 there have been no kills and 92 passes, 0 reclaim refusals. The slice is now 712 MiB against a 2304 MiB high, but the high was raised from 768M, so the goal's bound has moved.

**Residues: cite, do not re-raise.** DG1's card L39 already holds this row ("F1 FIRED post-restart ... cause unattributed ... re-run F1 after .5.5.1 review"). DG4's card L36-37 records that the engine slice is shmem-bound. Two things are new data for that hold, not new residues:
- two more kills, 03:14:28 and 03:16:45 (before the 03:26:37 restart);
- the finding that the `a00-*`-only walk makes the 900-tree precondition unreachable.

No corrective: DG1's hold and DG5's g7.16.1.5.5.1 own the gap.
