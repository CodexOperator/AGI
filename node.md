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

## §0 State (05:2xZ 09-30, date -u) — gen 9 · FULL SPEED to the 11:00Z STOP · review sm9a running (pi-free) + 4 Opus cross-checks
| | |
|---|---|
| post | sanctuary-master: bundle reviewer + the directors' centralized BOARD COORDINATOR (owner 03:0xZ 09-30, verbatim: "And make sure the directors still know to do coordination through Sanctuary Master. Like DG1 is waiting in SM to know when they can continue. And that's perfect that's exactly the setup I want as SM acts as a centralized board coordinator while the council answers mid-work questions and clarifications."): sequencing, when to continue, board placement = me · rulings = the council · never the Prime |
| usage | Prime 05:0xZ: to ~06:0xZ Opus subagents allowed and wanted (owner: "I need to max sub use before reset in an hour") · after: Sonnet 5.5 subagents · workflow.py stays pi-free · never the Claude Workflow tool |
| protocol | doc:council-loop "The loop" · goal:g7.16.1 · messaging: SendMessage by session name only (no send.py, no rooms) until the bundles land |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main · gen 9 · session agi-5c |
| skills | agi-merge-pass (§2 verdicts) · agi-workflow · agi-rotate · agi-node-write · agi-goal |
| peers (05:04Z) | Prime agi-79 · DG1 agi-2a · DG2 agi-7f · DG3 agi-91 · DG4 agi-80 · DG5 agi-5b · DG6 agi-bb · council: alive agi-e3 · all-is-one agi-8f [242e8c] · self-perpetuating agi-53 · stream-master agi-8c · names change at every seat → ListAgents |

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
sm9a (pi-free): ALL 4 review stages died "Provider returned an empty response" → the verdicts came from Opus Agent cross-checks (/tmp/sm9/cc_<key>.json)
  1098822e1 busy index   ACCEPT 0 residues → DG4 closes g4.18.5.2.1
  g4.18.5.2.2 (DG3 158a9fd06 de83b1d23 bb882a5f5)  ACCEPT (by hand) → DG1 told: close .2.1 + .2.2, outcomes, then g4.18.5.2
  d8b22ae96 ruling (b)   accept_with_residue: R1 a body opening with `---` forges mint_id/type (rc 0) · R2 edited_by/thought_session silently overwritten → DG3 fixing, ONE commit
  786c1c13a ramdisk      accept_with_residue: R1 no fallback when user systemd is unreachable · R2 --uninstall/--status blind · R3 GUARD_RAM_BUDGET not in config:guard · R4 goal body says agi-ram.slice → DG5; the guard-init apply (the Prime's) waits on R1-R3
  595b9c099 W2c C        DG3 found 4 defects itself (gate_for_root plain dict, _missing_link_refusal, cli._evidence_corpus drops the wrapper, a resolver per call) → corrective building; my Opus cross-check is still running
NEXT: on DG3's SHAs → review the W2c C corrective + the d8b22ae96 R1/R2 in ONE run (Opus until ~06:0xZ, then Sonnet subagents; pi-free is returning empties) · on DG5's → re-review, then batch to the Prime: guard-init apply + agi-work.slice stale (9302/8371 vs 6742/6067 MiB) + 13 agi-post scopes uncapped in app.slice (g6.41.1)
  W2c C clean → full [ready] to DG1 → DG1 outcome → MY bundle-4 bigger_outcome → alive agi-e3 (vision:alive review)
HEAL: restarted 05:06:37Z onto ff09c6101 (accepted, + 9ae1e26c3) · proof = no reaper oom-kill until ~06:07Z → DG1 build-vs-goal .5.3.1
RULING alive (a): config:guard is the ONE home for boxkit numbers · .5.5.3 retired (46aee1e96) · DG4 successor re-parents .5.5.3.1 + .5.5.3.2 → .5.5, then .5.5.3.2 first
BOARD: DG1 closes .2.1/.2.2 + sketches the g7.16.1.10 leaves (alive's placement; builds per file owner after each lane's current work) · DG2 alive's s22 + s28 verdicts · DG3 corrective + R1/R2 + g1.31 #24 #37 #12 · DG4 (rotated) re-parent → .5.5.3.2 · DG5 786 R1-R4 → 158(FIRST) 160 161 159 · DG6 g1.31 split (incl. .4.7 free-lane red) → claude-code route
First command at wake: ListAgents
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
| card stamps | read `date -u`, never estimate (DG1 stamped 09-30 at 23:5x 09-29) |

## §5 Verification: links.py links 5179 / 0 broken (23:5xZ 09-29) · per-round test counts are in each run's journal

## §6 BANKED
(none)
