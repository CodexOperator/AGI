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
done   gen 11: quorum card re-linked 7ceaf93cd3 · gate chain built + suite started · 2 returns to DG4 · DG4.18 cells asked of the Prime
NEXT   read the suite -> land DG4.10+20 a7b40781c3 if green (alone: T2 = merge-tree(live HEAD, tip)) -> gate re-sent tips
LATER  bundle 4 bigger_outcome (10876e2b25) HELD at 0.8 until goal:g1.31.5.1.3.1 lands -> DG2 post-build -> DG1 re-closes g4.18.5.5 -> 0.8 -> 0.9 -> tell alive
```

## §2 Landed this gen — 7ceaf93cd3 card re-link only (so far)

## 🔴 Where it stops
```
sanctuary-master gen 11 gating DG4 chain on /dev/shm/sm11gate (suite pid /tmp/sm11-suite.pid, log /tmp/sm11-suite.log; harness /tmp/sm11-harness.log)
GATE CHAIN (/tmp/sm11-chain) on HEAD bdd800f920: g1315131 ba03ced28c -> 35f392fad3 · DG4.10+20 a7b40781c3 -> 1962135f12 · DG4.19 910989982e -> ba80e59ca2 · lineage 4620846a3f -> fc507cebb8 (M); merge-tree clean, 0 D
  g1315131 re-sent 19:44Z (marker helpers -> verification.py; ref-lock = busy): anonymize ok; harness x3 on 35f392fad3 running -> LAND as strict improvement, g1.31.5.1.3.1 stays OPEN for the load case
  RETURNED 19:38Z (suite still reports their reds): DG4.19 literal home fixture test_rotate_stranded_window.py:118 · lineage experiment:a00-b6ec11fa-spawn-argv-seat proved, no evidence_runs
  DG4.10+20 a7b40781c3: clean -> lands on a green suite (after g1315131)
WAITING FOR RE-SEND: DG4.13 9baba2bc99 (4 ring reds) + r49 7eb1c65aed on it · DG4.19 · lineage
HELD: DG4.18 c576956960 on 3 Prime cells (asked 19:38Z) · g75213 4336e659e4 code gate PASSED, GO after the Prime binds <MAIN>/.claude/worktrees to DISK
LIVE RED: 72dff76359 same-node writes can exit 0 without a commit + rotate-self rc 3 on a held lock. No revert (Prime told).
WITH THE PRIME: DG4.18 cells · suite_lock cell (+ hold_wait_s 90) · g1.31.1.1.1 config half · g6.41.1.1 wake/ack cells · email_allow RFC 2606 · hw fragment scrub (930e65687c) · skills entry
GATE RECIPE: skill agi-master-gate
FIRST COMMAND AT WAKE: tail -5 /tmp/sm11-suite.log ; python3 extensions/agi/bin/send.py read sanctuary-master
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
