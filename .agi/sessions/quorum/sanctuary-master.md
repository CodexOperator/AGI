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

## §0 State (13:05Z 10-01, date -u) — gen 11 rotating on the Prime's BOX MEMORY RED (13:04Z) · owner night plan: work to 14:00Z
| | |
|---|---|
| post | sanctuary-master: master-gate for local-town + the directors' centralized BOARD COORDINATOR (owner 03:0xZ 09-30): sequencing, placement, gates + landings = me · rulings = the council · never the Prime |
| lanes | owner 02:27Z + 07:00Z 10-01: Sonnet 5.5 for everything; every MUR = workflow.py run agi-merge-up-review --harness claude-code (NOT pi-free) · DG5 pi-free · DG3 Opus medium ≤ 3 · VIZ LAST · research placement = thought-master's own |
| holds | g7.16.1.11 HOLD: no NEW round on key / identity / signing / rotate / spawn-row / write-gate (Prime-laned exceptions only: G4 stand-up) |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main · session: see config:posts row |
| skills | agi-master-gate (every landing) · agi-memory-guard (box) · agi-rotate · agi-node-write · agi-send · agi-goal |
| peers | Prime = belam · DG1 · DG2 · DG3 · DG5 (new-engine user; ACL fixed 11:4xZ) · TM (research) · council: alive · all-is-one · self-perpetuating · DG4 STOOD DOWN |

## §1 Plan
```
done   gen 11: 13 landings (§2) · bundle 4 -> 0.9 (8d5cd831fb) · 4 orphan scopes stopped 06:2xZ · /tmp/.agi stray marker moved aside
NEXT   re-gate ONE chain: G4 40e921b6e (DG3) + g73360-b 973078aaa (DG2), full suite -- both suites STOPPED by me at 13:05Z on the memory red, no result
LATER  DG3: tip-guard fork (council-report-tip-guard-accepts-only-commits) -> then the Prime sets merge_gate cells · map v0 last
```

## §2 Landed this gen (each landing message carries its gate numbers)
- a2e42a3bf0 g1315131 · 5a7a3bb828 DG4.10+20 · e81abd3f69 DG4.19 · 627c94a040 g7556 · 521ebaa951 .10.3 · 2ed4492434 .10.5 · 6d8ac01d74 DG2.C1
- 9158583d26 .10.7 merge gate OPTION A (inert) · da7cd145c DG2.R4 · deaa32675 crmur · cd8ca3914 g7556 fork · 0e6979bda R-MG · edb74b29e row 60
- post-builds: g1315131 lean 75 · g7556 0.85 · .10.3 0.85 · .10.5 lean 70 · crmur lean 85 · g70 0.92 · dg2-c1 0.9 · row 60 DISPROVED live 0.92 (-> g73360-b)

## 🔴 Where it stops
```
sanctuary-master gen 11 rotated 13:0xZ on the box memory red: no gate running, two tips wait for ONE re-gate
RE-GATE FIRST (only at MemAvailable >= 4 GiB AND memory PSI some avg60 < 10; ONE suite at a time):
  chain HEAD + 40e921b6e (G4: rotate.py main passes root to stand-up/merge-up, +2/-1) + 973078aaa (g73360-b: stop <unit>.scope via mem_cap.scope_unit)
  both pre-checked: merge-tree rc 0, 0 D, anonymize ok; reviews accept (G4 9/9 MET; g73360-b ACCEPT 0 residues)
  green -> land G4 then g73360-b -> DG2 re-runs its 3-path live check on MAIN + lifts dg2mvp-g60; DG3 told; the Prime: stand-up red + grep-orphan red close
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
