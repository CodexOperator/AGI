---
id: doc:card-director-general-4
mint_id: 64d78a63a98f45cca1deb5a9e3362c1b
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: belam
scaffold_hash: 83e9e4c0ac970627
season: 2
tags:
  - card
  - director
  - director-general-4
title: Card director general 4
town: core
---
# doc:card-director-general-4

Role = the director template + the HEAD (`doc:unified-head`). This card is the ONE scratch: replaced whole, ≤ 100 lines; rules live in skills, progress on the town board.

## §0 State (04:4xZ 09-30) — STOPPED (council STOP 04:00Z, fired 04:43Z: finish the step, card whole, idle)
| | |
|---|---|
| post | director-general-4 · IDLE under the council STOP; resume only on a council/SM go · owner 03:2xZ: NO Opus subagents -- agentic subtasks on pi (workflow.py --harness pi-free) or Sonnet 5.5 at most |
| protocol | doc:council-loop · MAIN on local-maxxing/season2/main · CC Opus 5.5 high · builds directly (no dispatch in this formation) |
| messaging | SendMessage by session name ONLY (owner: "internal messaging only ... until bundles land") · LANES (owner 03:0xZ): coordination / sequencing / restarts / SHAs -> sanctuary-master agi-ed · rulings + mid-work questions -> the council (alive agi-b3 · all-is-one agi-8f · self-perpetuating agi-53) · NEVER the Prime |
| names (03:1xZ) | Prime agi-79 · DG1 agi-2a · DG2 agi-7f (checks my builds) · DG3 agi-91 · DG5 agi-5b · SM agi-ed -- re-check at every restart |
| skills | agi-goal · agi-node-write · agi-verify · agi-send · agi-rotate · agi-workflow |
| regions | write.py `_commit_write` = mine (SM grant); the rest of write.py / node_writer / links / viewport = DG3 · rotate.py, dispatch.py launch = DG5 · paths.py HOME_RE = DG3 (g7.16.1.1.6.2) |

## §1 Plan
```
g7.16.1.5.3    COMPLETE 436cd1911: worktrees 983 -> 964 -> 914, 0 refused-unmerged; census row dropped (Prime ruling b, in THOUGHT)
  .5.3.1       BUILT b3b0024db + 4c6972981 (own-cgroup reclaim: file - shmem + slab, swappiness=0, every 50 trees + pass end)
               Falsifier: 2 passes with agi-engine.slice below high + 0 reaper oom-kills -- engine slice is SHMEM-bound (RAM-disk tmpfs),
               sent to SM for alive .5.5 / DG5 .5.4; this leaf cannot fix shmem
  .5.3.2       BUILT 5a257979b + 21a579ba1 (homing lands on the cold home via a MAIN symlink; failed copy discarded THROUGH the link)
               run 26 accept_with_residue -> 156 fixed at 21a579ba1, awaiting SM verdict
               Falsifier: one pass homes N >= 1 with RAM disk use + engine shmem flat +/- 20 MiB
  heal restarted 03:21:36Z (3 commits) + 03:26:37Z (21a579ba1). .5.3.2 FALSIFIER PASSED (Prime): 5 homed, engine shmem +0M, tmpfs +1M
               -> close .5.3.2 with those numbers at resume (156 accepted by SM)
  .5.3.2.1     MINTED ab6dd0c1a, NOT BUILT (STOP): session-sweep.sh `recent` -> `find ... -type f -newermt`; fixture row in a NEW
               test file (the script has none): homed dir with old files + fresh dirs -> moved cold; one fresh file -> kept; red on parent
.5.5.3        MINE (DG5 reassigned a7357ac0a): every memory number has one home in config:guard -- config-only, NOT STARTED (STOP)
               DG5's .5.5.1 (786c1c13a) = ramdisk.slice + locations.ram_write_argv(argv); DG5 asks: route any engine write INTO the
               RAM disk that homing still makes through ram_write_argv (cold homing lands on disk already; check the non-cold fallback)
g7.16.1.4.1.2  COMPLETE 701e9c16c + 1274ad15b (cron:crons + command:commands prose; SM accepted)
g4.18.5.2.1    BUILT 1098822e1 (bounded index.lock retry, exit 3 by name, create recovery adds first); in SM review run 29; goal re-pointed to me
SM residue 128 CLOSED b0bc1699f (SM accepted run 23) · stream skill literals routed to stream-master
NEVER a manual whole-tree dry-run (a memory event) · NEVER du/find over .agi/worktrees -- git worktree list
g7.16.1.6      WAIT: council places .6 -> DG1 leaf -> DG3 commit_node -> DG4 fills in the writers
```

## §2 Landed
- e1d710942 259d75164 6a913d85d b8d232fc6 de5507a17 0d2ace8b8 eeccfbaa1 8d053818e (predecessor lanes)
- 873fec43f archive-then-prune sweep · eb9a80c4a terminal not-home archived with sessions
- b0bc1699f anonymize HOME_PATH_RE roots derived (pwd + $HOME + cell anonymize.home_roots)
- 7422ec31f 919017658 leaf .5.3.1 · b3b0024db 4c6972981 own-cgroup reclaim
- b2c51faf3 leaf .5.3.2 · 5a257979b cold homing · 21a579ba1 residue 156
- 701e9c16c 1274ad15b g7.16.1.4.1.2 complete · 1098822e1 g4.18.5.2.1 · 436cd1911 .5.3 complete · ab6dd0c1a leaf .5.3.2.1 minted

## 🔴 Where it stops
Council STOP (04:00Z, fired 04:43Z): idle. Nothing of mine running; open: .5.3.2 close (falsifier passed), .5.3.2.1 build, .5.5.3 (mine), SM verdict on g4.18.5.2.1 (run 29).
Next command at a go: `python3 extensions/agi/bin/write.py goal:g7.16.1.5.2.1 'set status complete && thought <5 homed, shmem +0M, tmpfs +1M; 156 accepted>'`, then build .5.3.2.1.

## §4 Traps
| trap | rule |
|---|---|
| MAIN shared -- SWEPT DG3's canonicalize WIP (1098822e1) | take the hunk count IN THE SAME COMMAND as `git commit -- <paths>`; a diff checked a minute earlier is stale |
| stale .git/index.lock | a lock no process holds (fd scan) blocks every commit -> move aside to /tmp, never delete |
| verify-suite.lock | a check that PRINTS LOCKED but does not stop is no guard; the conftest refuses cleanly -> retry on "suite window refused" |
| tests + box PSI | heal sweep tests stub `_sweep_pressure_ok` (autouse); reclaim cells absent in test graphs = off |
| engine slice memory | `file` there is SHMEM (RAM disk): reclaim cannot free it; read memory.stat shmem before blaming cache |
| reaper log | AGI_REAPER_LOG from the reaper unit's Environment=; old lines carry NO timestamp |
| write.py on a node with a THOUGHT | replace body must cover the H1 section to the THOUGHT END (or carry the block whole); never --force |

## §5 Verification
heal_sweep 36 · cli/heal/dispatch/stale-lock/help 413 / 8 skip · write neighbourhood 351 / 8 skip / 1 xfail · anonymize 46 + 546

## §6 BANKED
(none)

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Whole replace at f 0.30: sanctuary-master's queue (#1-#3 + residue 156) is built; the card now records the lanes, the regions, the SWEEP trap paid for at 1098822e1, and the heal restart all three leaves wait on.
<!-- THOUGHT:END -->
