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

## §0 State (19:0xZ 09-30, date -u) — gen 10 · RUN to 21:00Z, then FREE LANE only, no STOP (owner 17:4xZ + 17:5xZ via the Prime; doc:unified-director-brief ROUND LANES 9cb773a774)
| | |
|---|---|
| post | sanctuary-master: master-gate for local-town + the directors' centralized BOARD COORDINATOR (owner 03:0xZ 09-30, verbatim: "And make sure the directors still know to do coordination through Sanctuary Master. Like DG1 is waiting in SM to know when they can continue. And that's perfect that's exactly the setup I want as SM acts as a centralized board coordinator while the council answers mid-work questions and clarifications."): sequencing, placement, gates + landings = me · rulings = the council · never the Prime |
| lanes | until 21:00Z: pi-free + claude-code Sonnet 5.5, Sonnet subagents (≤ 2), direct · from 21:00Z: every NEW round + review on pi-free only, no Sonnet subagents, live CC rounds finish |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main · session agi-12 [afd9c6] |
| skills | agi-master-gate (every landing) · agi-rotate · agi-node-write · agi-send · agi-goal |
| peers | Prime = seat belam gen 22 (send.py --to belam) · DG1 agi-8c [9e0227] · DG2 agi-e3 [78fffb] · DG3 agi-00 + DG4 agi-10: SendMessage FAILS -> send.py --to director-general-3/4 · council: alive · all-is-one · self-perpetuating (send.py --to <post>) · DG5 DG6 DOWN |

## §1 Plan
```
done   gen 10 landings (by SHA, each gated): g1.33 5f1e8092f2 · DG2.R1 7b367304df · R2 d572f65d6b · R3 7712457731 · brief g15 ef0d152992 · g6.41.1.1(1) 82c553bb9a · dg6-04 08b1ca1c94 · g1.31.4.1 88ddd2ca08 · DG4 STACK 72dff76359 · SM-1 heal-sweep d5d9107d43
done   closed: g1.33 · g1.31.4.1 · g7.16.1.5.4 · 8 trunk reds (7 fixed, skills_first_turn = the Prime's)
NOW    land DG4.17 -> DG4.13 -> keys (suites running, §🔴) · then gate lineage + the launder corrective
NEXT   bundle 4 bigger_outcome council-bundle-4-one-gate-one-commit-ids-never-move v3 (10876e2b25): HELD at 0.8 until goal:g1.31.5.1.3.1 lands clean -> DG2 re-check -> DG1 re-closes g4.18.5.5 -> ONE update 0.8 -> 0.9 -> tell alive
```

## §2 Landed this gen — see §1 done (every landing message names its gate numbers)

## 🔴 Where it stops
```
sanctuary-master gen 10 rotating at the line: 3 DG4 gates mid-suite, 2 merge-ups queued, launder red corrective building
GATES IN FLIGHT (land in THIS order; each: suite result -> reds attributed vs trunk -> T2 = merge-tree(live HEAD, tip), lands == range files, 0 D, 0 dirty overlap -> commit-tree -p HEAD -p tip -> ff-only -> push):
    1 DG4.17 LANDED 2cbe754da1 18:5xZ (DG4 + DG2 post-build not yet told)
    2 DG4.13 RETURNED 19:0xZ: 4 range reds (test_ring_cli_seam A/B/D + test_suite_no_detached_spawn::test_ring_fields_under_pytest_exits_zero; ring output empty) -- DG4 told
    LANDED 19:2xZ d01befa390 (DG4 + DG2 post-build to tell): was 3 keys tip af2c27335f (= SM-2 802577c1bd + DG4.12c/d): stacked full suite /tmp/sm-keys-suite.log (/dev/shm/sm-keys, includes DG4.13 -> expect its 4 ring reds + skills_first_turn; any OTHER red = attribute) · HEAD+keys tree /dev/shm/sm-keys2 (ids /tmp/keys-gate.ids): ring + stand_up + send 417 passed · then land from live HEAD
  known trunk red in every suite: test_skills_first_turn_entry (the Prime's) · after each landing: git worktree remove --force the tree + rm -rf /dev/shm/tmp-sm<name>
GATING g1315131 launder corrective tip d9fcbcbed5: gate commit efcf0abf75 (ids /tmp/g1315131-gate.ids, /dev/shm/sm-lnd, suite /tmp/sm-lnd-suite.log since 19:03:33Z); harness x3 = rc0==commits 3/3 + titles 0 (silent loss GONE) but launder rc3 0/21/27 (F1 v3 hard NOT met under load) -> DECISION: LAND as strict improvement if the suite is clean; g1.31.5.1.3.1 stays OPEN (DG4 told) · also queued DG4.18 stream c576956960 · DG4.10+DG4.20 merge-up (19:1xZ, in the dm) QUEUED · DG4 r49 engine_for 7eb1c65aed STACKED ON the returned DG4.13 -> waits for DG4.13 re-send (Prime items: locations.stream cell, byte_cap 8000, 2 grid versions) · QUEUED: DG4 g1.31.4.2.1 LINEAGE tip 4620846a3f (25 files; dispatch.py +22 = DG3 file, DG3 told) · DG4 launder corrective hypothesis:g1315131-held-suite-lock-is-waited-and-a-peer-in-flight-write-is-no-hand-edit (goal:g1.31.5.1.3.1; F1 v3 43c4724d9a) -> its gate MUST run `bash /tmp/dg2mvp/g41855/run_on.sh <sha> 3`: HARD rc0==commits, 0 launder rc3, no stuck dirt; BAND false rc3 <= 24/120, titles-absent <= 2
HELD: DG4 g75213 RAM row tip 4336e659e4 -- code gate PASSED; GO only after the Prime binds <MAIN>/.claude/worktrees to DISK (else `ram-main down` rm's unsynced Agent trees); asked 17:2xZ
RED LIVE ON TRUNK: 72dff76359 same-node writes can exit 0 without a commit + rotate-self rc 3 on a held lock (DG1 hit it). NO REVERT (decided 18:3xZ, the Prime told, may overrule). Workaround: a node stuck "already dirty (hand edit)" -> commit it by exact path.
COUNCIL ASKED 18:4xZ: g4.18.5.5 bullet "never waits" -> bounded wait (DG1 re-stated); silence = stands
QUEUED ELSEWHERE: DG3 next run: goal:g1.31.3.2.1 (+ 3 encoded-repo-path nodes) · g7.33.19 findings rows · DG1: g6.41.1.1.1 (blocked on the Prime's wake/ack cells) -> g6.41.1.1.2 · DG2: post-builds as landings arrive
FIRST COMMAND AT WAKE: read the 3 suite logs above (tail -3 each), then land in order
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
