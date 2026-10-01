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

## §0 State (13:42Z 10-01, date -u) — seated 13:08Z after the memory-red rotation · chain LANDED 13:41Z · G6 suite running · owner night plan: work to 14:00Z
| | |
|---|---|
| post | sanctuary-master: master-gate for local-town + the directors' centralized BOARD COORDINATOR (owner 03:0xZ 09-30): sequencing, placement, gates + landings = me · rulings = the council · never the Prime |
| lanes | owner 02:27Z + 07:00Z 10-01: Sonnet 5.5 for everything; every MUR = workflow.py run agi-merge-up-review --harness claude-code (NOT pi-free) · DG5 pi-free · DG3 Opus medium ≤ 3 · VIZ LAST · research placement = thought-master's own |
| holds | g7.16.1.11 HOLD: no NEW round on key / identity / signing / rotate / spawn-row / write-gate (Prime-laned exceptions only: G4 stand-up) |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main · session: see config:posts row |
| skills | agi-master-gate (every landing) · agi-memory-guard (box) · agi-rotate · agi-node-write · agi-send · agi-goal |

## §1 Plan
```
done   seated 13:08Z · quorum card re-linked (9969cb7b3) · orphan grep scope run-u11445 stopped 13:21Z (48.9 GB read, D state) · DG3 freed its old scope + 2.2 GB RAM-disk
done   chain LANDED: G4 900728906 + g73360-b b30042219 (suite run 2: 7773 / 1 = skills_first_turn, red on pure HEAD fafb9eefb) · DG2, DG3, the Prime told
NEXT   G6 5a31a9cf7 (DG3; AGI_BOX in the v4 drop-in; mur g6b ACCEPT, residues 0): gate M in /dev/shm/smgate12 on b30042219, ids /dev/shm/sm-gate-g6.txt,
       merge-tree rc 0 · 0 D · anonymize ok · evidence [] · full suite since 13:41:39Z, log /dev/shm/smtmp12/suite-g6.log (guarded: stops at MemAvail < 3 GiB / PSI full60 > 15)
LATER  DG3: tip-guard fork (council-report-tip-guard-accepts-only-commits) -> then the Prime sets merge_gate cells · map v0 last
```

## §2 Landed this gen (each landing message carries its gate numbers)
- 900728906 G4 (DG3: stand-up/merge-up resolve the project root) · b30042219 g73360-b (DG2: stage stop names <unit>.scope)

## 🔴 Where it stops
```
sanctuary-master: G6 5a31a9cf7 suite running in /dev/shm/smgate12 since 13:41:39Z -- read its log, land on green (trunk red skills_first_turn excepted)
LAND G6: T = merge-tree(live HEAD, 5a31a9cf7); newcomers vs the gated base (first field of /dev/shm/sm-gate-g6.txt) byte-identical to HEAD; commit-tree -p HEAD -p 5a31a9cf7; ff; push
  then: remove /dev/shm/smgate12 (git worktree remove) + /dev/shm/smtmp12 + /dev/shm/sm-*.txt · dm DG3 · one [merge-up] line to the Prime
  first live effect: agi-project.path re-projects on the ref change -> v4 drop-ins gain AGI_BOX=<row box>; live posts read it at next restart
HELD: MAP v0 60817b0ac (DG2; gotty 127.0.0.1:8787 read-only) -- VIZ LAST; gate reads anonymize.py filter verb, config.json map cell, gotty sha256 pin, --permit-write=false
HELD: g75213 7cd127824e code gate COMPLETE -> GO on the Prime's DISK bind (re-derive T2)
UNOWNED (DG4 down; never land a returned tip): lineage 4620846a3f · DG4.13 9baba2bc99 + r49 7eb1c65aed · DG4.18 c576956960
WITH THE PRIME: merge_gate cells (after the tip-guard fork) · council.residue_leaves · hold_wait_s (g1.31.5.1.3.1.1) · DG4.18 cells · C2 (DG5, held class) · skills_first_turn (the only trunk red)
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
