---
id: hypothesis:logs-and-write-once-scratch-live-on-the-flash-disk
mint_id: 2466bef1215d4eb49bbc509b97afa237
type: hypothesis
parents:
  - goal:g1
next_edges: []
edited_by: thought-master
scaffold_hash: c6a018aaae9c9d86
season: 2
testable_claim: after a path-level write census, the top sequential writers move to /mnt/agi-flash one at a time by config cell or symlink in a drain window, each guarded by mountpoint -q; internal-disk write bytes/min fall >= 20 pct at equal live spawns and no writer lands on / while the flash is unmounted
title: Logs and write-once scratch live on the flash disk (/mnt/agi-flash) by cell or symlink with a mountpoint guard; internal-disk writes fall >= 20 pct
town: core
---
# hypothesis:logs-and-write-once-scratch-live-on-the-flash-disk

**Owner decision (via the Prime, 22:2xZ 09-27; facts + verbatim on town:local-maxxing):** a new 113G ext4 flash disk at `/mnt/agi-flash` (fstab `nofail`) for LOGS and sequential write-once scratch ONLY. Plan owner: thought-master (box/guard); engine log-path cells: director-engine.

## Measured 22:4xZ 09-27 (box io PSI some avg60 46, after the TMM.306 step-back)
| path | size | writer | growth | kind |
|---|---|---|---|---|
| `~/.pi/agent/sessions` | 747 MiB | the pi harness (every parent + kid) | +71 KiB/min on disk vs pi write_bytes 19 MiB/min | session jsonl — rewritten or elsewhere: step 1 decides |
| `~/logs` | 46 MiB | cron jobs (memory_alarm, ...) | small | append |
| `.agi/sessions/workflows/runs` | 17 MiB | workflow.py | small | write-once run records |
| `.agi/sessions/harvest-0927` | 115 MiB | none (archive) | 0 | read-rarely |
| `~/.claude/projects` transcripts | ~0.5 GiB | Claude Code, always live | append | owner's window only |

## Step 1 census, 22:43-22:53Z 09-27 (10 min, 2 s fd scans + /proc/<pid>/io + du deltas)
| writer | MiB/min | share of internal-disk writes (139.4 MiB/min) |
|---|---|---|
| DE's drain-gate loop (a polling script, its /tmp scratchpad) | 56.5 | ~40 % -> the writer is fixed, not moved (TMM.308) |
| every Claude session | ~8 | ~6 % |
| all logs: pi sessions 0.09 + transcripts 0.09 + ~/logs 0.01 + workflow records 0.005 | 0.2 | ~0.1 % |
| unattributed: short-lived git / pytest in worktrees (exit inside the window) | ~70 | ~50 % -> the RAM worktree round (DH.650) |
Consequence: moving logs alone cannot meet the 20 % falsifier -- step 2 moves them for tidiness (cheap, one at a time); the io win is the two writers above.

## Plan
```
0  PILOT  harvest-0927 (no writer): copy -> verify byte count -> replace with a symlink to the flash copy -> remove the original
1  CENSUS 10 min path-level write census (per-dir byte deltas + fd scans at 1 s) -> the top sequential writers by bytes/min
2  MOVE   in census order, ONE writer at a time, each by a config cell (paths.local_maxxing.flash_root/<sub>) or a symlink,
          in a drain window with its writer stopped -- never a live mv under a running writer; DE owns the engine log-path cells
3  GUARD  every flash path checks `mountpoint -q /mnt/agi-flash` first; unmounted = the writer keeps its old path (nofail
          leaves an EMPTY dir on / that would silently refill the root fs) -- a symlink into an unmounted flash fails loudly
```
**Never:** worktrees · test tmp / pytest basetemps · git objects · any random-write path · the other USB stick (the owner's recovery OS) · the dead internal drive.

**Falsifier:** after steps 0-3, internal-disk write bytes/min (sum of the LVM volumes, /proc/diskstats) at equal live spawns do NOT fall by >= 20 %, OR any writer lands on / while /mnt/agi-flash is unmounted (tested by one unmounted dry run of the guard).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First version (thought-master 22:4xZ 09-27). The Prime [decision] 22:38Z relaying the OWNER: a new flash disk for LOGS and sequential scratch ONLY, never worktrees or test tmp; each move by a config cell / symlink with its writer, never a live mv; "TM: the move plan is yours (box/guard); DE: the engine log-path cells are yours". Parent goal:g1: no town subgoal covers box io (g5.* read; g7.31.3.3 = spawn/rotate). Numbers measured by me 22:4xZ (du, /proc/<pid>/io over 60 s). Near miss named in step 3: the mount is nofail, so an absent stick leaves an empty dir on the root fs that filled at 17:4xZ.
<!-- THOUGHT:END -->
