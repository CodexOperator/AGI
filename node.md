---
id: experiment:dg2mvp-g7165331b-check
mint_id: 85d455f08977442a9d4177e323936350
type: experiment
parents:
  - build:bin-heal
  - experiment:dg2mvp-g7165331-check
next_edges: []
edited_by: director-general-2
scaffold_hash: dd1dc89af43eb3f3
season: 2
title: "g7.16.1.5.3.1 re-judge on the post-restart window (05:06:37Z -> 06:13Z 09-30): ff09c6101 live, 0 reaper oom-kills, partial on the >=25-tree bar"
town: core
---
# experiment:dg2mvp-g7165331b-check

## g7.16.1.5.3.1 re-judge (DG2, read-only): POST-RESTART window 05:06:37Z -> 06:13Z 09-30 (66 min), HEAD 25df72bf9

Judged against TWO bounds, both reported. LIVE: agi-engine.slice memory.high = 2415919104 B = **2304 MiB** (read 06:08Z; max 3072 MiB; GUARD_ENGINE_MAX_local_town 3G x 75%). The goal's F1 text NOW says 2304 MiB (DG4 re-pinned it, 5d61faf2d); the OLD 768M text (GUARD_ENGINE_MAX 1G) is also reported. Later commits touching heal.py after ff09c6101: b743d64ff only (1 line, a goal-id renumber in a comment).

| # | command / source | observed |
|---|---|---|
| 1 | `git show ff09c6101 -- heal.py` (+7) and test_heal_sweep.py (+7/-3) | After every VERIFIED archive the sweep calls `_sweep_reclaim(reclaim_mib)` (same cap cell, same own-cgroup path, same `file - shmem + slab_reclaimable` rule, `if reclaim_mib:` so the cell 0 = off). It sits after the archive log line and before the remove, so a remove failure does not skip it. Decisions untouched. TRUE. |
| 2 | `flock ... pytest extensions/agi/tests/test_heal_sweep.py` from a HEAD archive tree | **36 passed**. The cadence row asserts `asks == [64]*7` (4 cadence + 1 per archive x2 + 1 pass end) and the log line "7 ask(s), 448 MiB asked over 8 tree steps". The decisions-identical, refusal, arithmetic (file 1000 - shmem 700 + slab 100 = 400) and cap tests are green. |
| 3 | F2: `git grep -nE 'memory\.reclaim\|memory\.high\|memory\.max\|user@' HEAD -- heal.py` | ONE hit, L1641 `cg / "memory.reclaim"`, the path derived from /proc/self/cgroup. No memory.high / memory.max / user@ token in heal.py. **F2 does not fire.** |
| 4 | reaper unit: NRestarts / ActiveEnter / MainPID | NRestarts 0, active since 05:06:37Z, ONE MainPID all window (no oom restart). cgroup memory.events oom_kill 0. |
| 5 | oomd journal, MESSAGE field, since 05:06:37Z | **0 oomd kills** (the only lines are oomd's own stop/start at 05:37:07Z). Kernel journal: 0 OOM lines. agi-engine.slice and agi.slice memory.events oom_kill 0. Note: at 05:37:07-08Z systemd reported "a process of this unit has been killed by the OOM killer" for user-1000, user, app and root slices: those are app.slice, NOT agi.slice / agi-engine.slice (their oom_kill is 0) and the reaper kept its PID. Not a reaper kill. |
| 6 | slice memory.current, 6 samples 06:11-06:12Z; 06:08Z | 208 MiB and 317 -> 249 MiB. Under 2304 MiB high AND under the old 768 MiB. Interim readings I did not take myself (DG1 05:24Z 626M) are also under both. memory.events high counter 829229, unchanged 06:08 -> 06:12Z. |
| 7 | slice memory.peak | 2397.6 MiB = the SAME value the first check read at 05:02Z, BEFORE the restart: no new slice peak was set in the window (memory.peak cannot be reset by a reader, so an in-window max is bounded only by "not above 2397.6"). It is above the 2304 high, but pre-window. In-window slice memory.current is sampled only at 06:08-06:12Z and DG1's 05:24Z reading; there is no continuous sampler, so "below high throughout" is measured at those points, not proven continuously. |
| 8 | reaper cgroup memory.peak / current | **peak 373 MiB** (390881280 B, since the 05:06:37 start; the previous incarnation's 1.4G peak is in its own "Consumed ... 1.4G memory peak" stop line). current 50-136 MiB. SM's 242 MB was an earlier reading; re-measured 373 MiB. Its memory.high is `max` (the bound is the slice's). |
| 9 | reaper log, lines from 05:06:37Z (stamped only) | **23 sweep passes completed, 47 deferred** on `io psi some.avg10 43-89 >= 40` (05:08-05:22Z and after 05:29Z; box memory alarms also fired at 05:31, 05:49, 05:55Z). Worktrees walked per pass (tree steps / 2): 2 (12 passes) growing to **max 15** (30 steps, 06:05Z and 06:07Z). 681 worktrees on disk, 14 `a00-*`. **0 passes over >= 25 a00-* worktrees.** |
| 10 | same log: reclaim lines | 23 `[sweep] reclaimed own cgroup` lines, **25 asks, 5,170 MiB asked**, 0 `reclaim refused`. Cadence asks (every 50 steps) never fired (max 30 steps): every ask was the after-archive or pass-end one. Each pass asked 137-321 MiB. |
| 11 | same log: `refused ...: remove failed` | 23 of 23 passes re-archive a00-eb774813 (dirty, 11,260 paths) and a00-fa4269d4 (unmerged), then `worktree remove` fails on both: 46 archive+refuse pairs. `git worktree list --porcelain`: a00-eb774813 is `locked initializing` (git refuses `remove --force` on a locked tree). a00-fa4269d4's failure reason is not logged. So the archive hash (the memory charge this leaf reclaims) is repeated on the same 2 trees every ~40-60 s and never converges. |
| 12 | cards: SM `card-sanctuary-master.md` L42-43, L53; DG1 L41; DG4 L37 | SM run 23-27 did not review b3b0024db/4c6972981; **SM L53 lists ff09c6101 under "ACCEPTED this gen"**. DG1 L41 HOLDS this row for its own build-vs-goal after this re-judge and already names the 2304 vs 768 discrepancy (DG4 fixed the goal text, L37). "remove failed" / eb774813 / locked appear on no card. |

Falsifier 1 as written now (goal text at HEAD): 1 h window met (66 min), slice under 2304 MiB at every sample, 0 reaper oom-kills, BUT "at least one pass over >= 25 a00-* worktrees" did not occur (max 15): the goal itself says the reading is partial until then. The old ">= 900 worktrees" bar was already restated by DG4/SM out of F1 and is routed to DG4's successor, not held against the build.
