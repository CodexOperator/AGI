---
id: experiment:dg2mvp-g7165331-check
mint_id: 9c810ce10dde440a8f82e69e770d2ca0
type: experiment
parents:
  - build:bin-heal
next_edges: []
edited_by: director-general-2
scaffold_hash: 9d2ff0488c71e3cb
season: 2
title: "g7.16.1.5.3.1 post-build check: own-cgroup reclaim (b3b0024db + 4c6972981) holds in code and tests; live F1 unmeasurable at >= 900 trees and contradicted by 5 post-landing reaper oomd kills at 1.4-1.5 GB"
town: core
---
# experiment:dg2mvp-g7165331-check

## g7.16.1.5.3.1 post-build check (DG2, read-only): DG4's b3b0024db + 4c6972981 at HEAD 172902cd7-era

Later commits touching the same files: 5a257979b (heal.py +43, test_heal_sweep +70, goal .5.3.2), 21a579ba1 (tests +39), 1098822e1 (config.json, other cell). None of them change `_sweep_reclaim` or the cadence hooks.

| # | command | observed |
|---|---|---|
| 1 | `git show --numstat b3b0024db 4c6972981` | heal.py +66/-0 and +14/-4, config.json +1/-1, test_heal_sweep.py +73/-0 and +9/-7. The ceiling holds. |
| 2 | `git show HEAD:extensions/agi/bin/heal.py` L1788-1802, L1830-1845, L1972-1978 | `reclaim_every` and `reclaim_mib` come from `_reaper_cell(root, "sweep_reclaim_every"/"sweep_reclaim_max_mib")`. `_walked()` runs on every tree step in BOTH walks (base pre-resolve + judge) and asks when `trees % every == 0`. There is one more ask after the judge loop at pass end. The loops have no early return after the walk starts (the returns at L1749/1770/1784 come before any tree is walked). End-state 1 TRUE. |
| 3 | `git grep sweep_reclaim HEAD -- .agi/config.json` | `"sweep_reclaim_every": 50, "sweep_reclaim_max_mib": 512` in `reaper`: both are config cells, not literals. The code defaults (100, 0 = off) apply only when a cell is missing. TRUE. |
| 4 | Read `_sweep_reclaim` L1617-1660 | cgroup path = the `0::` line of `SWEEP_PROC_CGROUP = Path("/proc/self/cgroup")` joined to `/sys/fs/cgroup`. `mib = min(max, (file - shmem + slab_reclaimable) >> 20)`. Nothing is written under 16 MiB, and a negative value (shmem > file) also gives 0. It writes `"<N>M swappiness=0"` and, only on EINVAL, the plain `"<N>M"`. EAGAIN counts as asked. Other OSError / ValueError: one `[sweep] reclaim refused` line, returns 0, never raises. Anon and tmpfs are never asked for. 4c6972981 arithmetic TRUE. |
| 5 | `git grep -n 'memory.reclaim\|memory.high\|memory.max\|user@' HEAD -- extensions/agi/bin/heal.py` (reclaim section) | ONE `memory.reclaim` path (`knob = cg / "memory.reclaim"`), derived only from /proc/self/cgroup. No write to memory.high/max and no user@ path in the sweep. Falsifier 2 does NOT fire. Invariant 1 TRUE. |
| 6 | `flock ... pytest extensions/agi/tests/test_heal_sweep.py` (from a /tmp archive of HEAD) | 36 passed. The 4 reclaim tests are green: file 1000 - shmem 700 + slab 100 = 400 (had shmem not been subtracted the result would be 1100, so the test catches it); cap; <16 MiB; no v2 line; refusal gives 1 line; cadence gives 5 asks with the same (3,0,1) decisions; the src grep. |
| 7 | /tmp probe `test_probe_g7165331.py` (in the /tmp tree only): cells on with every=1, `memory.reclaim` a DIRECTORY so every write fails | Decisions are identical to the cells-off run: (3,0,1), same removed/archived/kept lines, `sweep: removed=3 archived=2 refused=0 kept-live=1`. 9 refusal lines = one per failed ask. Invariant 2 TRUE. The EINVAL fallback writes the plain `400M`; shmem > file writes nothing. 4 passed. |
| 8 | `git grep -n xfail` for g7165331 / g7.16.1.5.3.1 in tests | No strict-xfail rows exist for this row, so none were removed or weakened. |
| 9 | Reaper log `$AGI_REAPER_LOG` since 03:02Z (heal's unit = the agi reaper service, cgroup agi-engine.slice/<reaper>.service; /proc/<MainPID>/cgroup confirms it) | 94 sweep passes completed. 94 `[sweep] reclaimed own cgroup` lines, 0 `reclaim refused`. Tree steps per pass (2 per worktree): max 364 = 182 worktrees (03:41Z); then 298/248/198/148/98/50; 87 passes over 4 steps = 2 worktrees. |
| 10 | `ls .agi/worktrees` | 668 entries, only 2 of them `a00-*`. heal's sweep globs `a00-*` only; the other 666 (`de-*`, `post-*`, ...) are never walked. The goal's 983 counted all worktrees. **0 passes over >= 900 worktrees: F1 is not measurable as written.** |
| 11 | `journalctl --user -u <reaper unit> --since 03:02` + `journalctl -u systemd-oomd` | Reaper oomd kills AFTER the code loaded (unit restart 03:07:49 on heal.py containing b3b0024db): **03:14:28, 03:16:45, 03:32:11, 03:37:03, 03:43:02**. oomd put the reaper's usage at kill at **1.5G, 122M, 1.4G, 1.4G, 1.4G** (pre-landing kills 02:28-03:03 were 33-100M). All were chosen on agi.slice pressure 51.7-66.2% > 40%. No kill since 03:43:03. |
| 12 | `cat .../agi-engine.slice/{memory.current,memory.high,memory.max,memory.peak}` + memory.stat, ~05:02Z | slice current 712 MiB < high 2304 MiB (high was 768M when the goal was minted; now raised; max 3G). Slice peak 2397 MiB. file 608 MiB of which shmem 500 MiB; slab_reclaimable 11 MiB. PSI full avg10 0.00. |
| 13 | reaper cgroup memory.current / memory.peak / memory.stat, ~05:02Z | current 38 MiB (file 53 KB, slab_r 3.7 MiB between passes), so the pass-end ask does drain it. **memory.peak 1450 MiB since the 03:43 restart.** Each 2-tree pass still asks ~336 MiB (git page cache re-charged per 40 s pass). |
| 14 | cards: SM runs 23-29; DG4 L35-37; DG1 L39 | No SM review run covered b3b0024db/4c6972981 (run 26 = 5a257979b). DG1 already HOLDS the row: "F1 FIRED post-restart ... cause unattributed (sweep vs tmpfs shmem, .5.5.1) ... >=900 not reproducible; re-run F1 after .5.5.1 review". DG4 records "engine slice is SHMEM-bound; this leaf cannot fix shmem". |

Disclosure: one 1 s /tmp probe run started while `.agi/sessions/verify-suite.lock` existed (the agent's lock check did not block); it wrote nothing in the repo.
