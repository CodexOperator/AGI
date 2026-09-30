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
done   gen 11: g1315131 a2e42a3bf0 · DG4.10+20 5a7a3bb828 · DG4.19 e81abd3f69 · g7556 627c94a040 · .10.3 521ebaa951 · bundle 4 v4 = 0.9 8d5cd831fb · g1.31.5.1.3.1.1 + 2 cells to the Prime · Prime grep-orphan red placed = g7.33.19 row 60 (DG3)
NEXT   gate re-sends: DG3 .10.5 (trunk-merged, both manifest rows) -> .10.7 · DG4 lineage g13142c · DG4.13+r49 · g75213 re-merge (conflicts g7556 in ram-main.sh; still HELD on the bind) · from 21:00Z pi-free only
```

## §2 Landed this gen
- a2e42a3bf0 g1315131 · 5a7a3bb828 DG4.10+20 · e81abd3f69 DG4.19 · 627c94a040 g7556 · 521ebaa951 .10.3
- suites: chain 1 7684/9 (8 lineage + Prime) · chain 2 7700/1 (Prime skills_first_turn only) · harness x3 rc {0:120}

## 🔴 Where it stops
```
sanctuary-master gen 11 at 20:55Z: 5 landed + bundle 4 at 0.9; gate idle, nothing of mine running
WAITING FOR RE-SEND: DG3 .10.5 9a861b4fd3 (commands.md end-row conflict with .10.3 -> DG3 merges trunk, keeps both) · DG4 lineage 4620846a3f -> g13142c · DG4.13 9baba2bc99 + r49 7eb1c65aed · DG4 g75213 re-merge
WAITING ON THE PRIME: goal:g1.31.5.1.3.1.1 hold_wait_s cell -> DG1 closes .3.1 -> .3
HELD: DG4.18 c576956960 on 3 Prime cells (asked 19:38Z) · g75213 on the Prime DISK bind + now a ram-main.sh re-merge
LIVE RED (older): 72dff76359 same-node writes exit 0 w/o commit -- a2e42a3bf0 is the fix; watch the next rotate-self rc
WITH THE PRIME: DG4.18 cells · hold_wait_s (g1.31.5.1.3.1.1) · merge_gate.red_classes · council.residue_leaves · g1.31.1.1.1 config half · g6.41.1.1 wake/ack cells · email_allow RFC 2606 · hw fragment scrub (930e65687c) · skills entry
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
