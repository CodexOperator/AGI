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

## §0 State (19:38Z 09-30, date -u) — gen 11 · RUN to 21:00Z, then FREE LANE only, no STOP (owner 17:4xZ + 17:5xZ via the Prime; doc:unified-director-brief ROUND LANES 9cb773a774)
| | |
|---|---|
| post | sanctuary-master: master-gate for local-town + the directors' centralized BOARD COORDINATOR (owner 03:0xZ 09-30, verbatim: "And make sure the directors still know to do coordination through Sanctuary Master. Like DG1 is waiting in SM to know when they can continue. And that's perfect that's exactly the setup I want as SM acts as a centralized board coordinator while the council answers mid-work questions and clarifications."): sequencing, placement, gates + landings = me · rulings = the council · never the Prime |
| lanes | until 21:00Z: pi-free + claude-code Sonnet 5.5, Sonnet subagents (≤ 2), direct · from 21:00Z: every NEW round + review on pi-free only, no Sonnet subagents, live CC rounds finish |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main · session: see config:posts row |
| skills | agi-master-gate (every landing) · agi-rotate · agi-node-write · agi-send · agi-goal |
| peers | Prime = seat belam gen 22 (send.py --to belam) · DG1 agi-8c [9e0227] · DG2 agi-e3 [78fffb] · DG3 agi-00 + DG4 agi-10: SendMessage FAILS -> send.py --to director-general-3/4 · council: alive · all-is-one · self-perpetuating (send.py --to <post>) · DG5 DG6 DOWN |

## §1 Plan
```
done   gen 10 landings: g1.33 5f1e8092f2 · DG2.R1-3 · brief g15 ef0d152992 · g6.41.1.1(1) 82c553bb9a · dg6-04 08b1ca1c94 · g1.31.4.1 88ddd2ca08 · DG4 STACK 72dff76359 · SM-1 d5d9107d43 · DG4.17 2cbe754da1 · keys d01befa390
done   gen 11: g1315131 a2e42a3bf0 · DG4.10+20 5a7a3bb828 · lineage + DG4.19 returned · DG4.18 cells asked of the Prime 19:38Z · DG2 told post-build
NEXT   DG2 post-build on a2e42a3bf0 -> DG1 re-closes g4.18.5.5 -> bundle 4 (10876e2b25) ONE update 0.8 -> 0.9 -> tell alive
```

## §2 Landed this gen
- a2e42a3bf0 g1315131 (goal:g1.31.5.1.3.1 fix; stays OPEN for the load case) · 5a7a3bb828 DG4.10+20 (goal:g1.31.5.1.1)
- chain suite 7684 passed / 9 failed (8 lineage + the Prime's skills_first_turn); harness x3 rc {0:120}, rc3 0, dirty 0

## 🔴 Where it stops
```
sanctuary-master gen 11 at 20:09Z: 2 landed, gate idle, no suite or gate tree of mine running (/dev/shm/sm11* removed)
WAITING FOR RE-SEND: lineage 4620846a3f (8 reds: fake target 'hypothesis:x' vs the trunk's DG5.01 target check + evidence_runs on experiment:a00-b6ec11fa-spawn-argv-seat) · DG4.19 910989982e (home-path fixture test_rotate_stranded_window.py:118) · DG4.13 9baba2bc99 (4 ring reds) + r49 7eb1c65aed on it
WAITING ON DG2: run_on.sh a2e42a3bf0 3 (post-build) -> bundle 4 chain
HELD: DG4.18 c576956960 on 3 Prime cells (asked 19:38Z) · g75213 4336e659e4 code gate PASSED, GO after the Prime binds <MAIN>/.claude/worktrees to DISK
LIVE RED (older): 72dff76359 same-node writes exit 0 w/o commit -- a2e42a3bf0 is the fix; watch the next rotate-self rc
WITH THE PRIME: DG4.18 cells · suite_lock cell (+ hold_wait_s 90) · g1.31.1.1.1 config half · g6.41.1.1 wake/ack cells · email_allow RFC 2606 · hw fragment scrub (930e65687c) · skills entry (test_skills_first_turn_entry red on trunk)
GATE RECIPE: skill agi-master-gate · pipelined chain = one suite for N tips, reds attributed on a pair tree
FIRST COMMAND AT WAKE: python3 extensions/agi/bin/send.py read sanctuary-master
```
## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path; never switch branches, stash or reset |
| a write-path gate | green suite + matching dry-runs MISSED 72dff76359: also run DG2's concurrent harness (run_on.sh) landed vs control |
| a harness metric with noise on the control | run the control too (titles-absent 2/22 on df14730e89) before calling a bar hard |
| a live code path (heal, brief, driver.sh, guard/) | measure its FIRST live run on MAIN's data before GO (boot-resume: 0 seats; briefs identical) |
| hardware / home tokens | never print: find + replace inside python, print counts; write.py dry-run diffs echo the old line |
| rotate flattens the quorum card | re-link: `ln -sfn ../../nodes/doc/card-sanctuary-master.md .agi/sessions/quorum/sanctuary-master.md` |
| rotate-self may fail rc 3 on a held suite lock (the live red) | check `ls .agi/sessions/verify-suite.lock`; if it fails, rotate by hand per skill agi-rotate |
| write.py sub with `\n` | stored literally: use `replace body N:M <file>` (paragraph guard: widen to a blank line) |
| a post rotates mid-thread | its old session name dies: re-read ListAgents / rotation records before a send |
| a bigger_outcome before the directors' outcomes | never: DG1 writes one OUTCOME per goal first |
| card stamps | read `date -u`, never estimate |

## §5 Verification: every landing = merge-tree rc 0 + lands == range + 0 D + full suite with reds attributed (baseline suite when a red is unclear)

## §6 BANKED
goal:g1.31.4.2.1.1 copilot hooks: PARKED (DG4 option b); one real copilot probe = spend, banked to the Prime 19:3xZ (rec: stay parked until copilot runs)
