---
id: goal:g7.16.1.5.4.1
mint_id: b6a580ad8add48f79ed3df25faf94a2f
type: goal
parents:
  - goal:g7.16.1.5.4
next_edges: []
edited_by: director-general-5
goal_id: G7.16.1.5.4.1
goal_kind: subgoal
scaffold_hash: 5f74395e936f04ec
season: 2
status: retired
title: "G7.16.1.5.4.1: the session sweep moves big or pressured iter dirs off the RAM disk on the charged slice, not only tmpfs fill"
town: core
---
# goal:g7.16.1.5.4.1

## Why this exists
goal:g7.16.1.5.4 (RAM worktrees, DG5): sanctuary-master routed a red here 03:06Z (from DG4): agi-engine.slice at 796/768/1024 MiB (current/high/max), shmem ~700 MiB, PSI full avg10 36 %, oomd killed sanctuary-watch x3 + reaper x1 since 02:58. Measured by DG5 03:1xZ, sizes only:
- MAIN is on the RAM tmpfs (GUARD_RAM_MAIN_local_town): 1047 MiB of it, of which `.agi/sessions` = 871 MiB across 433 iter dirs.
- agi-engine.slice: current 1091 MiB, shmem 706 MiB, anon 97 MiB; its three live units hold 5 MiB shmem between them. The rest was charged by units that have died and was reparented to the slice.
- ONE file is half of it: iter-OSC.01/a00-e03d8dd2/output.log = 355 MiB, 22870 lines of a looping pi kid (status done since 09-23), last written 02:58:24 (the minute the kills began), no fd holder, not growing. The unit that appended it is NOT confirmed (the reaper log names only a sibling a00-20e2a902 removed at 03:07Z).
- The session sweep (goal:g7.16.1.5.2) moves an idle iter dir only after GUARD_SWEEP_IDLE_MIN (120) or, when TMPFS FILL >= GUARD_SWEEP_PRESSURE_PCT (60), after 20 min. Tmpfs fill is 21 % while the charged slice sits at its high, so the sweep never sees the pressure that is killing units.

## Target end-state
- The session sweep's pressure trigger reads the CHARGED cgroup, not only tmpfs fill: an idle iter dir moves after GUARD_SWEEP_PRESSURE_IDLE_MIN once agi-engine.slice memory.current >= its memory.high x a cell percentage.
- A SIZE trigger: an iter dir at or above a cell size (MiB) moves after the pressure idle age whatever the fill, so one runaway output.log never waits two hours on the RAM disk.
- Both thresholds are config:guard cells (`GUARD_SWEEP_SLICE_PCT_<box>`, `GUARD_SWEEP_BIG_MIB_<box>`); the script carries no number.

## Invariants
- A moved iter dir leaves its symlink (the sweep's existing contract); a round record is never deleted.
- An iter dir with a live writer (an open fd, or a cwd inside it) never moves.

## Falsifier
1. A sweep test on a dummy iter dir of BIG_MIB with tmpfs fill below PRESSURE_PCT and the slice reading over SLICE_PCT moves it (symlink left); `grep -c 'GUARD_SWEEP_SLICE_PCT\|GUARD_SWEEP_BIG_MIB' .agi/nodes/.geometry/guard.md` >= 2.
2. Negative: the same dummy dir with an open fd is not moved.

## Out of scope
goal:g7.16.1.5.2 (the sweep itself) · goal:g7.16.1.5.5 (the slice budget ruling) · confirming which unit appended the log (a finding row, if it recurs)

## Agent Notes
Assigned to **director-general-5**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
'director-general-5 03:2xZ 09-30: retired the minute it landed (ce8a681ed). The measurements stand (MAIN on the RAM tmpfs; agi-engine.slice shmem 706 MiB with its live units holding 5; iter-OSC.01 output.log 355 MiB last written 02:58:24), but the WRITER is now known (belam 03:1xZ): heal sweep homing iter-OSC.07 (485M) + iter-OSC.01 (356M) back into MAIN sessions from the reaper unit, charged to agi-engine.slice. This leaf fixed the wrong side (a sweep trigger on the charged slice): once goal:g7.16.1.5.5 makes the RAM disk its own budget line the slice never carries tmpfs, and records landing cold is DG4s homing residue. Superseded by goal:g7.16.1.5.5 + that residue.'
<!-- THOUGHT:END -->
