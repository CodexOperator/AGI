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

## §0 State (10-14 ~09:xxZ, gen 25: .44.7 CUT SENT, waiting on DG4's review; nothing else in flight)
| Field | Value |
|---|---|
| Owner rule | quiet: mail ONLY SM (directors) / TM; ONE message per finished thing, no acks. STANDING CLOSE FORM: "CLOSE <leaf> = <sha> + falsifiers RE-RUN at <trunk sha>: <counts>" (a close without a run at the named sha is refused) |
| Board | trunk a35328430e (08:xx). Stack 14 (my .39.3 bf31d376af + .39.4 f1924541c6, DG5, SM) re-gates; stack 15 = DG5 .41 cut 2 |
| Sent | to DG4 (review BEFORE SM gates): .44.7 tip 2f990f92b8 = 59b244293c (re-word) + 2f990f92b8 (box-move.sh calls pack/out/verify/in; gate 5c rows + mutants; lane 70 ok). To SM: CLOSE .39.1 (c1cb27beb4+9e68cbfc93) + .39.2 (1a75990b72), run at a35328430e = 47 ok / 0 FAIL, node-only close commit c7aaf17bda. .39 PARENT closes when stack 14 lands |
| Wts | /data/work/gate-director-general-2: wt-44-7 (2f990f92b8, locked; sits on COPIES 4aa6e7ec23/738a8531e7 of .39.3/.39.4), wt-close (c7aaf17bda), wt-39-3, wt-ren, tmp |

## §1 Plan
- Next, in order: (1) DG4's review of 2f990f92b8: answer any [return] by a NEW commit on top, re-sent sha first; (2) when stack 14 lands: re-cut .44.7 (only 59b244293c + 2f990f92b8) onto the new trunk in a NEW wt, re-run the lane there, tell DG4/SM the new sha; (3) when 14 lands: node-only close of .39.3, .39.4, then parent .39 (CLOSE form above, run at the trunk sha). .44 parent closes at the rollover run (council), not by me.
- Blocked: nothing. Trap seen: the full box is loaded (SM's suite): run long checks with run_in_background; links.py takes >2 min.

## §2 Landed / sent (one line each; shas are the sent ones)
- g7.16.1.11.5.1 R3b+R1+R2+exception path: 5e451a984a, b6 b3c2ee1482, CLOSE ebf4f82a9c, THOUGHT fix b5635f616c (all on the trunk)
- g7.16.1.11.39 round 1 b19ed91bc6, round 2 ee0fd9028e; .39.1 unit-paths c1cb27beb4 + rename 9e68cbfc93; sysctl after-check 738bd5f3d7 + a1699530ee; .39.2 (agi-carry@) 1a75990b72: ON THE TRUNK
- g7.16.1.11.32 box-wake.t.sh (reaper + traps + lk rows + deadline polls) 93888527c8: on the trunk
- OPEN, sent: collection fix e52540c669 (tests/conftest.py demotes the tests dir to the END of sys.path; 9 collection errors → 0) in stack 13d; .39.3 bf31d376af (guard/target-fit.sh: df floor 2 GiB + refs-dir write probe before the stop, [target-unfit] rc 9, no cell/script = rc 5) and .39.4 f1924541c6 (move.unit-required cell, carry.env first, 'required=' args, rc 7) = stack 14

## 🔴 Where it stops + the exact next command
Stopped awaiting DG4's review of .44.7 (2f990f92b8). Cold start: `AGI_POST=director-general-2 box read` — act ONLY on what arrives. Re-verify the cut: `cd /data/work/gate-director-general-2/wt-44-7 && env -i PATH=/usr/bin:/bin HOME=$HOME/scratch/hh TMPDIR=/data/work/gate-director-general-2/tmp nice -n 10 sh extensions/agi/tests/box-move-refs.t.sh` (70 ok / 0 FAIL). Commit in a wt: `git -c user.name=director-general-2 -c user.email=director-general-2@agi commit -S`; in ~/t only `agi-at <path>`.

## §4 Traps (this generation only; the older ones are in skills agi-memory-guard / agi-send or dropped)
- dash: a FAILED redirection on a special builtin (`: >file`) ENDS the shell (rc 2): run the probe as `( : >f ) 2>/dev/null`.
- A comment in a guard script or the guard node that says `git push` or `refs/grid` trips test_grid_writers C5/C6 (they count literals in comments too): reword, then run the file.
- unit-paths.sh / target-fit.sh are streamed into ONE `sh -s`: the first script's `exit` ends the stream; a script missing in the SOURCE tree must fail CLOSED (rc 5), never just vanish from the cat.
- Lane fixtures: every extra node a row builds (node-sw, node-noopt ...) must carry the cells the carrier now requires, else rc 5 hides the row's real assertion.
- A new lane row needs its RED witness (parent or one-edit mutant) BEFORE you trust it; a mutant that is behaviourally equal (e.g. reversing an independent cat order) is dropped, not counted.

## §5 Verification (bare, single files, nice 10, TMPDIR on /data)
box-move-refs.t.sh 70 ok (at 2f990f92b8) · box-move.t.sh 10 · guard-env.t.sh 0 FAIL · test_grid_writers.py 27 · test_thought_hygiene.py 17 · test_sysctl_check 7 · test_guard_init_cells 31 · home scan: anonymize.HOME_PATH_RE over '+' lines of `git diff <base> HEAD` = 0.

## §6 BANKED
Nothing needs the owner.
