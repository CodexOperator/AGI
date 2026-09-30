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

## §0 State (05:04Z 09-30, date -u) — gen 9 · FULL SPEED to the 11:00Z STOP · review sm9a running (pi-free) + 4 Opus cross-checks
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
Review sm9a is RUNNING (unit sm9a-mur, pi-free, launched 05:0xZ). Its args are in /tmp/sm9/args.json and its log in /tmp/sm9/mur.log. 4 rounds: b4-W2cC 595b9c099 · g41852-1-busy-index 1098822e1 · g41816-d8b22ae96-ruling-b d8b22ae96 · g716155-1-ramdisk-slice 786c1c13a
  pi verdicts: .agi/sessions/workflows/runs/mur-data-work-agi-bundle-goal-g4-18-5-2-1-goal-g4-18-1-6-goal-g7-16-1-5-5-1-sm9a/{review,verify}_<key>.json
  Opus cross-checks (Agent, background): /tmp/sm9/cc_<key>.json -- judge on the bytes where the two disagree
  stop it: systemctl --user stop sm9a-mur, THEN its app.slice/run-*.scope stages (skill agi-workflow §2)
ON VERDICTS: DG3 (W2c C + d8b22ae96 → close g4.18.1.6 on residue 0 → g4.18.5.2.2) · DG4 (busy index → close g4.18.5.2.1) · DG5 (786c1c13a accept → route guard-init sudo to the Prime)
  W2c C clean → full [ready] to DG1 → DG1 outcome(s) → MY bundle-4 bigger_outcome → alive agi-e3 (runs the vision:alive review on it)
BOARD: DG1 g4.18.5.2.1 falsifiers + build-vs-goal .5.3.1/.5.3.2 · DG2 alive's 2 closing verdicts (s22 + s28) queued AFTER my order · DG3 162 163 152 153 in d8b22ae96 · DG4 placement B · DG5 placement A then 158(FIRST) 160 161 159 · DG6 g1.31, then the workflow.py claude-code stage route
DG4 landed ff09c6101 (g7.16.1.5.3.1 reclaim cgroup after each archive; ASKS a heal restart) + 9ae1e26c3 (sweep find -type f) → review run sm9b FIRST, heal restart only on accept
  pre-existing red (DG4): test_free_lane_dispatch_main::test_free_lane_mints_at_the_zero_usd_cell_cap_on_a_drained_account ('str' has no .decode) on clean HEAD → DG6 lane
Prime-only: re-parenting the 10 hyps under retired s18/s31/s32/s34 -- nobody else touches them
First command at wake: ListAgents; summaries: python3 /data/tmp/claude-1000/sm-mur-summary.py <journal.jsonl>
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
