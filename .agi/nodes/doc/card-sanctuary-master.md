---
id: doc:card-sanctuary-master
mint_id: 9a4a831c938a4501b30d37248ad319c0
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 3e856c7e9b80c2ab
season: 2
title: Card sanctuary master
town: core
---
# doc:card-sanctuary-master

# doc:card-sanctuary-master — sanctuary-master's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; ≤ 100 lines; written DURING the work so a dead session is resumable.

## §0 State (15:46Z 10-01, date -u) — WORKING: wind-down LIFTED (owner 15:1xZ via belam, verbatim on goal:g7.16.1.11: "keep going until we finish the goal bundle now") · no gate running
| | |
|---|---|
| post | sanctuary-master: master-gate for local-town + the directors' centralized BOARD COORDINATOR (owner 03:0xZ 09-30): sequencing, placement, gates + landings = me · rulings = the council · never the Prime |
| lanes | owner 02:27Z + 07:00Z 10-01: Sonnet 5.5 for everything; every MUR = workflow.py run agi-merge-up-review --harness claude-code (NOT pi-free) · DG5 pi-free · DG3 Opus medium ≤ 3 · VIZ LAST · research placement = thought-master's own |
| holds | g7.16.1.11 HOLD: no NEW round on key / identity / signing / rotate / spawn-row / write-gate (Prime-laned exceptions only: G4 stand-up) |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main · session: see config:posts row |
| skills | agi-master-gate (every landing) · agi-memory-guard (box) · agi-rotate · agi-node-write · agi-send · agi-goal |

## §1 Plan
```
done   seated 13:08Z · box reboot 14:42Z, heal resume, own posts row ca9b4e81a · orphan grep scope stopped 13:21Z · row 60 CLOSED live (DG2)
done   4 landings (§2) · C2 mur run + RETURNED to DG5 (5 residues) · .env finding banked: belam agreed (A) masters/Prime run director murs
done   G7 2e94bd1f3 + TM-new a001a3c61 landed (whole-.agi/context leak -> rule in skill agi-master-gate 62e1fc541; Prime accepted)
NEXT   C2: re-mur -2 accept_with_residue -> RETURNED 17:0xZ (landmine test, 1 suite account, Dispatch line cut, self-cited evidence_runs, a00-273b2e39 list form); next re-send: read the small delta myself + evidence dry-run + links schema, then gate; Falsifier 1 naming routed to DG1. Was: re-mur RUNNING since 16:36:38Z (run mur-season2-loops-goal-g1-31-4-6-2-a00-3014f810-2; args in scratchpad c2b-mur-args.json) -> then gate + land, numbers to belam. Was: re-mur pi-free (load1 < 16, io avg60 < 50) -> numbers to belam
LATER  place a round (DG5 16:46Z, verified: inbox/director-general-5.md cursor line 112 sits past my unread 16:37Z line 111 -> send.py read says empty while a [decision] waits; the advancer is unnamed) · place a round: the nudge sweep skips pid-0 / recover-false rows or checks window name = seat (SP [red] 15:2xZ; belam cleared 5 rows 6efa87be4) · DG3: tip-guard fork -> then merge_gate cells · map v0 last
```

## §2 Landed this gen (each landing message carries its gate numbers)
- 900728906 G4 (DG3) · b30042219 g73360-b (DG2) · 6c87be791 G6 (DG3: v4 drop-in AGI_BOX) · fec9f352f G5 (DG3: send treats a v5 post as a peer) · 2e94bd1f3 G7 (DG3: strace -b execve) · a001a3c61 TM-new research (key comments + DT-1 home path fixed in-gate)
- suites: chain 7773 / 1 · G6 7776 / 1 · G5 7787 / 1 · G7 7790 / 1 · TM-new 7790 / 1 -- the 1 = test_skills_first_turn_entry, red on pure HEAD fafb9eefb (the trunk's)

## 🔴 Where it stops
```
sanctuary-master: G5 landed fec9f352f; waiting on DG3's G7 merge-up and DG5's C2 re-send; no gate running
G7: merge-tree vs live HEAD rc + --name-only · range = merge-base..tip · tmpfs gate tree /dev/shm/<gate> + own TMPDIR · full suite under the mem guard · land by commit-tree
C2: run key mur-season2-loops-goal-g1-31-4-6-2-a00-3014f810 (args in my scratchpad: rebuild from the [merge-up] dm) -- re-mur only after DG5 says the 5 residues are closed
HELD: MAP v0 60817b0ac (DG2; gotty 127.0.0.1:8787 read-only) -- VIZ LAST; gate reads anonymize.py filter verb, config.json map cell, gotty sha256 pin, --permit-write=false
HELD: g75213 7cd127824e code gate COMPLETE -> GO on the Prime's DISK bind (re-derive T2)
UNOWNED (DG4 down; never land a returned tip): lineage 4620846a3f · DG4.13 9baba2bc99 + r49 7eb1c65aed · DG4.18 c576956960
WITH THE PRIME: merge_gate cells (after the tip-guard fork) · council.residue_leaves · hold_wait_s (g1.31.5.1.3.1.1) · DG4.18 cells · C2 (DG5, held class): merge-up 83f492f11 (goal:g1.31.4.6.2, +681/-7, 0 prod lines) QUEUED -- I run its mur once the Prime lanes it · skills_first_turn (the only trunk red)
FIRST COMMAND AT WAKE: python3 extensions/agi/bin/send.py read sanctuary-master
```

## §4 Traps (learned this gen; rules live in skills)
| trap | rule |
|---|---|
| my /dev/shm gate trees + suites are charged to MY scope (926 MB shmem at 13:0xZ) | start a suite only at MemAvailable >= 4 GiB + PSI low; never two at once under pressure; stop = every pid with cwd under the gate path, then worktree remove |
| a stray /tmp/.agi project marker | reddens root-discovery tests (test_workflow root rows, test_commands wrapper-flag): moved aside to /tmp/agi-stray-copy-created-20261001T021319Z |
| test_suite_live_checkout_worktree red | a post wrote its live card mid-test: passes alone |
| systemctl --user stop <bare name> | resolves .service, rc 5, the .scope lives: name '<unit>.scope' (g73360-b) |
| heal sweep | loads heal.py fresh each pass: a landed heal fix is live without a reaper restart |
| a test falling through a fake seam | can launch a REAL pi: read every slice/stage test's red for a real binary in the traceback |
| pipelined chain gate | one suite for N tips; attribute reds on a pair tree without the suspect range |
| old uid vs group agi | fixed by the Prime 11:4xZ (default ACLs on refs, comms, spawn-budget, inbox, worktrees) |
| rotate flattens the quorum card | re-link: ln -sfn ../../nodes/doc/card-sanctuary-master.md .agi/sessions/quorum/sanctuary-master.md |
| MAIN shared | commit by exact path; never switch branches, stash or reset |

## §5 Verification: every landing = merge-tree rc 0 + T2 newcomers byte-identical to HEAD + 0 D + anonymize + evidence dry-run + full suite with every red attributed (alone / pure-HEAD tree)

## §6 BANKED
- goal:g1.31.4.2.1.1 copilot hooks: PARKED (a real copilot probe = spend, the Prime's)
- a00-fa4269d4's 40 files pinned off-repo: /data/work/agi-pins/a00-fa4269d4.20261001T0247Z.tar.gz (the tree stays; refusal live)
- .env is 600 belam:belam, no group ACL (verified 15:3xZ): NO agi-* director can dispatch (provisioning PermissionError) -> (A) masters/Prime run directors' murs [recommended; today's practice] · (B) group:agi read ACL [owner's money: owner's call] -- sent to belam 15:3xZ
