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

## §0 State (08:4xZ 09-30, date -u) — gen 9 · RESUMED after the history scrub (every sha changed) · DG5 + DG6 stood down, their rows re-laned onto DG3 + DG4
| | |
|---|---|
| post | sanctuary-master: bundle reviewer + the directors' centralized BOARD COORDINATOR (owner 03:0xZ 09-30, verbatim: "And make sure the directors still know to do coordination through Sanctuary Master. Like DG1 is waiting in SM to know when they can continue. And that's perfect that's exactly the setup I want as SM acts as a centralized board coordinator while the council answers mid-work questions and clarifications."): sequencing, when to continue, board placement = me · rulings = the council · never the Prime |
| usage + stand-down | owner 06:1xZ 09-30, verbatim (via the Prime): "We should probably ease off expensive subagents now and just use strictly sonnet 5.5 ideally using our new headless CC review routes." → Sonnet 5.5 subagents ONLY, ≤ 2 at once, headless CC route where one exists, never Opus/Fable or the Claude Workflow tool · and: "We also will need to stand down director-general 5 and 6 to help conserve tokens as well. Just let them arrive at a stopping point and have them stop and take down the posts to free up resources. 3,4 can continue as is and pick up whatever 5,6 don't finish after standing down" → I re-lane DG5/DG6 handover rows onto DG3 + DG4 (priority: DG6 email scrub · DG5 ramdisk proof · g1.31 residues · workflow.py CC route) |
| protocol | doc:council-loop "The loop" · goal:g7.16.1 · messaging: SendMessage by session name only (no send.py, no rooms) until the bundles land |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main · gen 9 · session agi-5c |
| skills | agi-merge-pass (§2 verdicts) · agi-workflow · agi-rotate · agi-node-write · agi-goal |
| peers (08:4xZ, ALWAYS "name [ref]") | Prime agi-23 [ecd665] · DG1 agi-8c [9e0227] · DG2 agi-e3 [78fffb] · DG3 agi-34 [e82e60] · DG4 agi-c8 [6d9f0c] · alive agi-e3 [761106] · all-is-one agi-8f [242e8c] · self-perpetuating agi-53 [21dc2d] · stream-master agi-8c [f29919] · DG5 DG6 DOWN |

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
SHAs: the scrub (08:0xZ) rewrote ALL history. Map old → new: grep ^<old> /data/scrub/union.git/filter-repo/commit-map. Below = NEW shas.
RUNNING: Sonnet review of DG4 be11671cb (N2 residues R1-R3) → /tmp/sm9/cc_n3.json → accept → DG4 closes .5.5.8
VERDICTS SENT post-resume: DG3 04d765c81 (B: 126 alias ids refused = REGRESSION, first · R1c: VT/FF/NEL/LS/PS before --- still forge) · DG4 2833cdae9 (158c crash-window orphan temp: adopt or sweep)
BUNDLE 4 bigger_outcome (council-bundle-4-one-gate-one-commit-ids-never-move) OPEN 0.8: limit (3) = DG3's R1c (g4.18.1.6 open) · (4a) = g4.18.5.5 (DG4). When both land: ONE update citing DG2 verdict:dg2mvp-w2cD PROVED 0.86 → 0.9
RE-LANE (owner 06:1xZ, DG5 + DG6 down):
  DG3: B+R1c → anonymize email + hw classes (PRIVACY; the Prime: the tracked guard must match the box hook) + the Prime's rulings n109/n22 (no edited_by rewrite) · n6 (one placeholder cell) · n144 (usernames only in PATH context) → g7.33.20.2/.3 → g1.31.3.2 a/b + .3.1.1/.3.1.2 (mur-clean → merge --no-ff) → DG5.01 harvest (.4.1) → .5.4 close (name the 12 agi-ram worktrees) → .5.5.6 → .5.5.7 → g1.31.4.7 → 46 missed rows (.5.4.x .5.5.x, briefs) · .10.4
  DG4: _commit_write round (fork + n83 + g4.18.5.5) → g1.31.5.1.1 hook RED → 158c → harvests g1.31.2 · .1.1 · .1.2 · .4.2.1 · .4.6.2 → g1.31.5.3 → heal-sweep fork (then the Prime restarts heal) → .4.5b/.4.5a/.4.6.1 → .4.2.2 → .4.4 + the workflow.py claude-code route → g4.18.5.6 · .10.1 .10.2 .10.6
  DG1: .7 goal edits (SP findings 2+3: re-point .7.1.3 F; 6 horizon leaves) + the .10 Assigned re-points
MERGE RULE (DG6's rounds): mur-clean only, --no-ff, one at a time, merge-tree check first → ONE [merge-up] per batch to me → gate + land (skill agi-master-gate)
Meter at 0.37: rotate at 0.47 (bare rotate.py rotate after this card is committed)
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
