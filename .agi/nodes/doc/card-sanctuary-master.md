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

## §0 State (05:5xZ 09-30, date -u) — gen 9 · FULL SPEED to the 11:00Z STOP · W2c C ACCEPTED → bundle 4 waits on DG1 roll-up outcomes
| | |
|---|---|
| post | sanctuary-master: bundle reviewer + the directors' centralized BOARD COORDINATOR (owner 03:0xZ 09-30, verbatim: "And make sure the directors still know to do coordination through Sanctuary Master. Like DG1 is waiting in SM to know when they can continue. And that's perfect that's exactly the setup I want as SM acts as a centralized board coordinator while the council answers mid-work questions and clarifications."): sequencing, when to continue, board placement = me · rulings = the council · never the Prime |
| usage | Prime 05:0xZ: to ~06:0xZ Opus subagents allowed and wanted (owner: "I need to max sub use before reset in an hour") · after: Sonnet 5.5 subagents · workflow.py stays pi-free · never the Claude Workflow tool |
| protocol | doc:council-loop "The loop" · goal:g7.16.1 · messaging: SendMessage by session name only (no send.py, no rooms) until the bundles land |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main · gen 9 · session agi-5c |
| skills | agi-merge-pass (§2 verdicts) · agi-workflow · agi-rotate · agi-node-write · agi-goal |
| peers (05:3xZ) | Prime agi-79 (rotating → window @23) · DG1 agi-8c [9e0227] · DG2 agi-7f · DG3 agi-34 · DG4 agi-c8 [6d9f0c] · DG5 agi-c8 [3f306f] · DG6 agi-bb · alive agi-e3 · all-is-one agi-8f · self-perpetuating (@19) · stream-master agi-8c [f29919] · map by tmux list-windows -F "#{window_id} #{window_name}" vs ListAgents @N |

## §1 Plan
```
done   bundles 1-3 → bigger_outcome 1-3 v3 (1111fed58; 128 closed; conf 0.75 → 0.8 when skills/agi-stream :18 :21 are scrubbed by stream-master)
done   bundle 4 write.py chain 129-149 CLOSED · W2c B (g4.18.6.3.2) CLOSED · 128 engine CLOSED · grid fork · W-G
done   DG1 outcomes: g4.18.5.1 · g4.18.6.1 · g4.18.6.2 · g4.18.6.3.2 · g7.16.1.4.1
done   gen 9: DG6 placed on g1.31 (lane rule sent) · board A → DG5 (retire .5.5.3 → .5.5) · board B → DG4 (.5.3.2 + .1 under .5.2, one mover fn)
NOW    review sm9a (4 rounds) + Opus cross-checks → verdicts to DG3 / DG4 / DG5
       W2c C clean → full [ready] to DG1 → DG1 outcome(s) (+ g4.18.5.2 after .2.1/.2.2) → MY bundle-4 bigger_outcome → council
```

## §2 Landed this gen (CC opus runs 16-28 + by hand; details in each run's journal)
- runs 16-24: 131-147 opened/closed (THOUGHT marker ONE _HEAD/_END; stdin once; payload one pre-dry judge by VERB; dry == real)
- run 23: 128 engine b0bc1699f accept · run 26: DG4 cold homing 5a257979b (156 → 21a579ba1 by hand) · heal restarted 03:26:37Z, falsifier PASSED (5 homed, shmem +0M)
- run 27: DG5 keys 4abfee9d3 → 157-161 (DG5) · Prime writing key_template (cond 5 default = ruling)
- run 25/28: g4.18.1.6 (DG3) → 150-155; 150 151 155 MET in 563cd4ca9 → 162 163 (DG3, introduced by the move)
- by hand: 141 · 137 · 148+149 f0768720f · 6e21d9655 · grid 6ec1f046c · g7.16.1.4.1.2 · c3c118b3c (write.py HEAD red: DG4's 1098822e1 swept DG3's canonicalize; fixed)

## 🔴 Where it stops
```
BUNDLE 4: W2c C ACCEPTED (7d10fc7c7 + bd15f4e6e; twins 0/5049 differ, parent 5034; 2991/3000 mint refs) → [ready] sent to DG1 agi-8c [9e0227] 05:5xZ
  asked DG1 for roll-up outcomes (≤ 4 parents): g4.18.5 (.5.1 + .5.2) · g4.18.6 (.6.1 + .6.2 + .6.3 roll-up) · then MY bigger_outcome:council-bundle-4-... parents = g4.18.5 roll-up · g4.18.6 roll-up · outcome:g7-16-1-4-1-w-g-goals-md-retired-closed
  template: .agi/nodes/bigger_outcome/council-bundles-1-3-one-source-fail-closed.md (judged_against goal:g7.16.1 · lens vision:sanctuary · season 2) → hand to alive agi-e3 (vision:alive review)
  if DG2's own twin re-judge disagrees with 0/5049 → hold the bigger_outcome
OPEN REVIEWS (Sonnet subagents after ~06:0xZ; ≤ 2 at once, my scope was the largest, 1.96G):
  DG3 agi-34: d8b22ae96 R1-R4 + _commit_message guard (round live) · g1.31.4.3 03acdf602 (not yet reviewed)
  DG4 agi-c8 [6d9f0c]: d82a63e5a R1-R6 (cell validation BEFORE arithmetic) · then write-refusal fork + PASS B3 row 83 (both _commit_write)
  DG5 agi-c8 [3f306f]: 158b + stand-up 4-mode fork (g7.16.1.7.1.4.1) + R4 + F2 pin, ONE commit · g1.31 rounds a00-1c745a92 a00-33e0c858 a00-3014f810 · the ramdisk proof · horizon leaf per-post MemoryHigh under .5.5
  DG6 agi-bb: g1.31.5 FIRST (112 owner email forward scrub + anonymize email pattern · 19 pre-commit pipefail) → relay the DG3 (84 60) / DG4 (83) / DG5 (107 + 5 rows) leaf ids when minted
DONE this gen: guard-init APPLIED 05:37Z by the Prime (plans identical; my audit accept_with_residue) · 1098822e1 · g4.18.5.2.2 · ff09c6101 · 9ae1e26c3 · placement B · alive ruling (a) · keysync 852ff3b12/f3c31278e
DEVIATION (SM go id-restore, 05:4xZ): DG4 hand-restored goal:g7.16.1.5.5.5 line 2 (e2120e3e6, 1 line, mint unchanged) -- write.py cannot touch a node with unparseable frontmatter; rest via write.py 8c7f9c993. Findings row → DG3 (refuse a bad id row at read time)
HEAL proof ends ~06:07Z (restart 05:06:37Z; 0 kills at 05:24Z) → DG1 + DG2 re-judge .5.3.1
Prime banked (§6 of its card): owner email in 4 tracked nodes, forward scrub only, no history rewrite unless the owner asks
First command at wake: ListAgents + tmux list-windows
```
## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path; never switch branches, stash or reset |
| `grep -r` / `find` over .agi/ or the repo root io-stalls the box | `git grep PATTERN -- <paths>` |
| rotate flattens the quorum card | re-link: `ln -sfn ../../nodes/doc/card-sanctuary-master.md .agi/sessions/quorum/sanctuary-master.md` |
| a home path, a /data user dir name | never print it: count only (128 was found by counts) |
| suite lock held → write.py's self-commit refused | the write lands; commit by exact path in a background waiter loop |
| a post rotates mid-thread | its old session name dies or is reused by ANOTHER post: re-read config:posts before every send |
| a peer's commits land between a row's commits | one round per commit, never a range across a foreign commit |
| a mur residue chain | residues only on what THIS diff introduced or left open; the rest are notes |
| a claim that names a message ("prints X") | the round also checks the rc and what was written (C1) |
| a falsifier grep can pass on a spelling technicality | re-run it against the pre-fix SHA (113: `THOUGHT:(BEGIN|END)` dodged F2) |
| preview vs write | every write.py fix: ask for dry == real on rc AND stderr (96, 125, 130) |
| a bigger_outcome before the directors' outcomes | never: DG1 writes one OUTCOME per goal first |
| two sessions share a name after rotations | map tmux window ids → ListAgents @N; send with `name [ref]` |
| card stamps | read `date -u`, never estimate (DG1 stamped 09-30 at 23:5x 09-29) |

## §5 Verification: links.py links 5179 / 0 broken (23:5xZ 09-29) · per-round test counts are in each run's journal

## §6 BANKED
(none)
