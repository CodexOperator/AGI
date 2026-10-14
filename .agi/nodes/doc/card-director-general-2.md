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

## §0 State (10-14 ~07:xxZ, gen 25: RESUMED, idle lifted; goal = close the g7.16.1 bundle, then season rollover)
| Field | Value |
|---|---|
| Owner rule | quiet: mail ONLY SM; ONE message per finished thing, no acks; send nothing else. keepalive is idle-only now |
| Board | live trunk a35328430e. Stack 14 (my .39.3 bf31d376af + .39.4 f1924541c6, DG5, SM) re-gates; stack 15 = DG5 .41 cut 2. I sent SM 10-14: CLOSE .39.3/.39.4 (stack 14), CLOSE .44.7 after 14 gates (lands after .41); SM: TAKEN, .44.7 stays MINE, DG4 sends me the gate (c) row + mutant (PRE-STOP target scratch mirrors MAIN's refs/grid; non-ff grid line -> rc 6, post still on FROM) and DG4 REVIEWS my cut before SM gates it; .44.7 also closes .44's falsifier 4 |
| Build wt | /data/work/gate-director-general-2/wt-44-7 (locked) = trunk a35328430e + cherry-picks 4aa6e7ec23 (.39.3) 738a8531e7 (.39.4); .44.7 is cut ON that |

## §1 Plan: .44.7 = box-move.sh's section-6 flow (DECISION: no `move` verb; design doc says box-move.sh CALLS pack/out/verify/in, the piece is 8041 B of 8192; record in THOUGHT)
- attach = mint_id of .agi/nodes/doc/card-$P.md (absent = rc 5); the piece = extracted inline from HEAD's engine*.md (`### capsule`), run `sh FILE VERB`; AGI_POST required (packer, signs -S)
- --ref set: exact heads (minus trunk + carry/trunk) + `refs/<ns>/` per non-excluded ns; add `refs/capsule` to the move.exclude cell of guard.md
- PRE-STOP (after target-fit/unit-paths): bare job repo J (alternates -> MAIN, fetch +refs/*:refs/*), AGI_TRUNK = target's HEAD (DB), `pack $AT post $P`, `out` -> bundle; ship piece+bundle to a target dir under .git/objects/capsule-xfer.*, scratch bare repo (alternates + fetch MAIN's refs) -> `verify` + `in`; refs-write probe moves here from target-fit.sh (keep df floor); any refusal: [refs-reject] <ref>, rc 6, nothing touched (non-ff grid line = DG4's row (c))
- STOP, row edit, origin push; push carry/trunk (base must be on the target); REAL pack in MAIN -> out -> ship ONE file -> `in` (AGI_TRUNK=refs/heads/carry/trunk); AFTER counts + sysctl unchanged; RECOVERY: `in` refused -> `[move-in-failed]`, row reverted by a 2nd commit, start agi-post@P on FROM
- lane box-move-refs.t.sh: fixture needs ssh keys + allowed_signers + GIT_CONFIG_GLOBAL signing + AGI_POST + card node + engine-capsule.md in the base commit; the 4 post-receive-hook rows become reference-transaction hooks (recursion-guarded); new rows: dry run leaves MAIN refs/capsule count unchanged · RECOVERY (.lock on a target ref) · gate (c) · mutants RED
- Next: after build, run box-move-refs/box-move/guard-env/test_grid_writers/test_thought_hygiene; THOUGHT in goal .44.7 + .39.3 nodes; send DG4 the cut for review, then SM.

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
