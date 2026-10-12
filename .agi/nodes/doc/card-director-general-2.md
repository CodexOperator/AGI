---
id: doc:card-director-general-2
mint_id: d55057fc5ba24e7ab2bb66cbf9d326bf
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-general-2
scaffold_hash: b3449e9971f09f91
season: 2
tags: []
title: Card director general 2
town: core
---
# doc:card-director-general-2

# doc:card-director-general-2 — director-general-2's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; ≤ 100 lines. Skills: agi-send · agi-goal · agi-verify · agi-rotate · agi-memory-guard · agi-master-gate. Template: doc:unified-director-brief.
My lane: FALSIFIER lanes first (test-only + a sha), RED on the build's parent, GREEN on a scratch reference, one-edit mutants + named stays-greens; SM gates. Since 10-11 SM also hands me whole leaves (lane + build).

## §0 State (10-12 ~07:5xZ, gen 25: IDLE by OWNER order; nothing in flight, no crons)
| Field | Value |
|---|---|
| Owner rule | 10-12 07:4xZ via SM (verbatim): "Disable keep alive for all posts"; "Be back next week once usage resets on Wednesday". Every post IDLE: no new gate/land/dispatch/review/build/council round; SEND NOTHING (every box mail wakes a post; [red] only for a box-safety emergency); do not box belam until the owner resumes |
| Board | L13 f632cd4854 LANDED. Stack 14 (my .39.3 bf31d376af + .39.4 f1924541c6, DG5 .22 + .41.1, SM 0ad0eb2e7d) built at b522328480, its full run STOPPED by the order. Stack 15 = DG5 .41 cut 2. Stack 13d: state unknown to me |
| Gate dir | /data/work/gate-director-general-2: tmp, wt-ren (e52540c669, locked), wt-39-3 (bf31d376af + f1924541c6, locked). ~/scratch/keep = mutants, shims, ref39/ |

## §1 Plan
- Done: §2. Idle until the owner resumes. Then, in SM's order: (1) answer any [return] on stack 14 / 15 (re-cut ON the new tip they name, never amend a sent sha); (2) .44.7 'capsule move POST BOX' (goal:g7.16.1.11.44.7; doc g716111-44-capsule-pack section 6: DRY pack in a job-owned clone + TARGET verify + scratch in + refs-dir write probe, all BEFORE the stop; real pack / carry ONE file / in --atomic; RECOVERY [move-in-failed]); replaces box-move.sh's push + after-check lines, KEEPS unit-paths, target-fit and the row edit; ONLY AFTER DG4's core verbs .44.1-.44.4 land (no such goal nodes in my tree on 10-12). When it lands: remove ONLY the refs-write probe from guard/target-fit.sh, KEEP the df floor.
- Blocked: nothing but the owner's idle order.

## §2 Landed / sent (one line each; shas are the sent ones)
- g7.16.1.11.5.1 R3b+R1+R2+exception path: 5e451a984a, b6 b3c2ee1482, CLOSE ebf4f82a9c, THOUGHT fix b5635f616c (all on the trunk)
- g7.16.1.11.39 round 1 b19ed91bc6, round 2 ee0fd9028e; .39.1 unit-paths c1cb27beb4 + rename 9e68cbfc93; sysctl after-check 738bd5f3d7 + a1699530ee; .39.2 (agi-carry@) 1a75990b72: ON THE TRUNK
- g7.16.1.11.32 box-wake.t.sh (reaper + traps + lk rows + deadline polls) 93888527c8: on the trunk
- OPEN, sent: collection fix e52540c669 (tests/conftest.py demotes the tests dir to the END of sys.path; 9 collection errors → 0) in stack 13d; .39.3 bf31d376af (guard/target-fit.sh: df floor 2 GiB + refs-dir write probe before the stop, [target-unfit] rc 9, no cell/script = rc 5) and .39.4 f1924541c6 (move.unit-required cell, carry.env first, 'required=' args, rc 7) = stack 14

## 🔴 Where it stops + the exact next command
Stopped idle (owner order 10-12). Nothing was in flight; the worktrees above are untouched. Cold start after the owner resumes: `AGI_POST=director-general-2 box read` — act ONLY on what arrives. If a sha I sent is stale against the trunk: `git merge-tree --write-tree refs/heads/local-maxxing/season2/main <sha>`; re-cut in a NEW worktree on /data (`git worktree add --lock -d /data/work/gate-director-general-2/wt-X refs/heads/local-maxxing/season2/main`), commit `git -c user.name=director-general-2 -c user.email=director-general-2@agi commit -S`, `git verify-commit HEAD`. Re-verify the move lane at a tip: `env -i PATH=/usr/bin:/bin HOME=$HOME/scratch/hh TMPDIR=/data/work/gate-director-general-2/tmp nice -n 10 sh extensions/agi/tests/box-move-refs.t.sh` (57 ok / 0 FAIL at f1924541c6).

## §4 Traps (this generation only; the older ones are in skills agi-memory-guard / agi-send or dropped)
- dash: a FAILED redirection on a special builtin (`: >file`) ENDS the shell (rc 2): run the probe as `( : >f ) 2>/dev/null`.
- A comment in a guard script or the guard node that says `git push` or `refs/grid` trips test_grid_writers C5/C6 (they count literals in comments too): reword, then run the file.
- unit-paths.sh / target-fit.sh are streamed into ONE `sh -s`: the first script's `exit` ends the stream; a script missing in the SOURCE tree must fail CLOSED (rc 5), never just vanish from the cat.
- Lane fixtures: every extra node a row builds (node-sw, node-noopt ...) must carry the cells the carrier now requires, else rc 5 hides the row's real assertion.
- A new lane row needs its RED witness (parent or one-edit mutant) BEFORE you trust it; a mutant that is behaviourally equal (e.g. reversing an independent cat order) is dropped, not counted.

## §5 Verification (bare, single files, nice 10, TMPDIR on /data)
box-move-refs.t.sh 57 ok · box-move.t.sh 10 · guard-env.t.sh 0 FAIL · test_grid_writers.py 27 · test_thought_hygiene.py 17 · test_sysctl_check 7 · test_guard_init_cells 31 · home scan: anonymize.HOME_PATH_RE over '+' lines of `git diff <base> HEAD` = 0.

## §6 BANKED
Nothing needs the owner.
