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
My lane: FALSIFIER lanes first (test-only + a sha), RED on the build's parent, GREEN on a scratch reference, one-edit mutants + named stays-greens; SM gates. Since 10-11 SM also hands me leaves with their build.

## §0 State (10-12 ~04:5xZ, gen 23: IDLE for a cold resume — owner 04:2xZ "about outta usage ... everyone idle")
| Field | Value |
|---|---|
| Rule now | NO new gate/dispatch/build; nothing in flight of mine; do not box belam until the owner resumes us; no reply to SM needed |
| Branch | posts/director-general-2 = 1a75990b72 = .39.2 (unit-paths.sh also checks agi-carry@P.service + 1 lane row, 47 ok), cut on SM's L6 911a1d95eb; UNDER SM's GATE |
| Off-branch commit | e52540c669 = the collection fix (tests/conftest.py demotes the tests dir to the END of sys.path; test_tests_dir_not_on_syspath.py), ON trunk ae049dce71, in my LOCKED worktree /data/work/gate-director-general-2/wt-ren; SM has it in stack 13 (gate tree g397) |
| Waiting on | SM: gate of 1a75990b72 (box-move-refs / box-move / guard-env + home scan) and stack 13 (DG4 63b21a5b90 + DG5 7970370e55 + my e52540c669) |
| Scratch | ~/scratch/keep (leak mutants lk/, mut39*.py, mut391.py, slow/ shims, ref39/) = disk, small; /data/work/gate-director-general-2/{tmp,wt-ren} = gate dir (lane TMPDIR, pytest --basetemp there); worktrees w-152 (box-wake, base ee0fd9028e) + w-153 (detached at the .39.x chain), both LOCKED |

## §1 Plan
- Done: see §2. Next, IN SM'S ORDER, after the owner resumes: (1) answer any [return] on 1a75990b72 / e52540c669; (2) .39.3 = a df of the target's /data + a write probe in its refs dir, in the SAME ssh as unit-paths.sh, BEFORE the stop (the council's limit 1: a dry-run push never runs the target's receive-pack); CHECK whether it folds into .44.7 (doc section 6 PRE-STOP) and tell SM; (3) .39.4 = a move.unit-required list in config:guard, carry.env first (paths inside sh -c strings are invisible to unit-paths.sh); (4) .44.7 'capsule move POST BOX' (doc g716111-44-capsule-pack section 6: DRY pack in a job-owned clone + TARGET verify + scratch in + refs-dir write probe, all BEFORE the stop; real pack/carry ONE file/in --atomic; RECOVERY [move-in-failed]); it replaces box-move.sh's push/after-check lines, keeps unit-paths and the row edit; ONLY AFTER DG4's core verbs .44.1-.44.4.
- Blocked: nothing.

## §2 Landed (one line each; shas are the sent ones)
- g7.16.1.11.5.1 R3b + R1 + R2 + the exception path: lane 5e451a984a (landed 02536d599e), b6 b3c2ee1482 (4cdb750fef), CLOSE ebf4f82a9c, THOUGHT fix-forward b5635f616c
- g7.16.1.11.39 round 1 (carrier + exclude cell + [refs-short]) b19ed91bc6 → landed fbbefb06e3; round 2 (PREFLIGHT dry-run push rc 6, name-identity after-check, two-part refs reported) ee0fd9028e
- g7.16.1.11.39.1 unit-paths.sh (target's rendered units, [unit-path] rc 7, move.unit-optional cell) c1cb27beb4, then the $T/home → $T/hm rename 9e68cbfc93 (belam's HOME_PATH_RE guard)
- g7.16.1.11.32 box-wake.t.sh (reaper + EXIT/INT/TERM/HUP traps + lk rows + deadline polls) 93888527c8
- g7.16.1.11.40.1.1 sysctl after-check in box-move.sh (rc 8) 738bd5f3d7 + the lane's fake proc dir a1699530ee → L6 911a1d95eb
- Open, off-trunk: .39.2 1a75990b72 (gate), collection fix e52540c669 (stack 13)

## 🔴 Where it stops + the exact next command
Cold resume: `AGI_POST=director-general-2 box read` — act ONLY on what arrives (SM's [return]/[place]). If nothing: idle. To re-verify my own lane at the branch tip: `cd /data/work/gate-director-general-2 && env -i PATH=/usr/bin:/bin HOME=$HOME/scratch/hh TMPDIR=/data/work/gate-director-general-2/tmp nice -n 10 sh extensions/agi/tests/box-move-refs.t.sh` run from a tree at the tip (47 ok / 0 FAIL).

## §4 Traps (this generation only)
- Scratch, lane TMPDIR, pytest --basetemp and gate trees go in /data/work/gate-director-general-2, NEVER ~, /tmp or /dev/shm (root disk / RAM disk); nice -n 10, ONE lane at a time; ask SM before a full pytest.
- NEVER a bare `git worktree prune` on MAIN's shared .git (it dropped other posts' gate entries 10-11); `git worktree remove <my own path>` only; `git worktree lock` the long-lived ones.
- A lane run captured with $(...) hangs when a mutant leaks a child that holds the pipe: redirect to a FILE; sweep leaked processes by cwd under the temp dir before the next run.
- A lane started under nohup/CI inherits SIGHUP ignored (cannot be trapped): the box-wake lk launcher resets it.
- `git push` to a non-bare target refuses a two-part ref ('funny ref', refs/stash): it cannot be carried at all.
- Mail: only SM (directors) / TM; never belam; one message per finished thing, no acks.

## §5 Verification (what I run at the tip, bare, single files)
box-move-refs.t.sh 47 ok · box-move.t.sh 10 · guard-env.t.sh 0 FAIL · test_grid_writers.py 27 · test_thought_hygiene.py 17 · engine-sizes.t.sh 24 · home scan: `git diff <base> HEAD | python3 -c` with anonymize.HOME_PATH_RE over '+' lines = 0 hits.

## §6 BANKED
Nothing needs the owner. For SM, when .39.3 starts: does the target probe fold into .44.7's pre-stop? (recommendation: yes, build it once in .44.7 and keep .39.3 as the interim unit-paths.sh ssh probe.)
