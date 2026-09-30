---
id: doc:card-sanctuary-master
mint_id: 9a4a831c938a4501b30d37248ad319c0
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: belam
scaffold_hash: 3e856c7e9b80c2ab
season: 2
title: Card sanctuary master
town: core
---
# doc:card-sanctuary-master

# doc:card-sanctuary-master — sanctuary-master's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; ≤ 100 lines; written DURING the work so a dead session is resumable.

## §0 State (04:44Z 09-30, date -u) — gen 8 · COUNCIL STOP (04:00Z order, fired) → IDLE · nothing running
| | |
|---|---|
| post | sanctuary-master: bundle reviewer + the directors' centralized BOARD COORDINATOR (owner 03:0xZ 09-30, verbatim: "And make sure the directors still know to do coordination through Sanctuary Master. Like DG1 is waiting in SM to know when they can continue. And that's perfect that's exactly the setup I want as SM acts as a centralized board coordinator while the council answers mid-work questions and clarifications."): sequencing, when to continue, board placement = me · rulings = the council · never the Prime |
| usage | owner 04:5xZ 09-30, verbatim (via the Prime; SUPERSEDES 03:2xZ): "Let's switch your reviews and stuff to sonnet 5.5, and all subagents can be sonnet 5.5 as well to free up the free lane" → Agent subagents model sonnet · claude-code stages --model claude-sonnet-5-5 · workflow.py runs stay pi-free until its headless claude-code stage route lands · NEVER Opus/Fable fan-outs, forks or the Claude Workflow tool |
| protocol | doc:council-loop "The loop" · goal:g7.16.1 · messaging: SendMessage by session name only (no send.py, no rooms) until the bundles land |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main · gen 8 · meter 0.44 |
| skills | agi-merge-pass (§2 verdicts) · agi-workflow · agi-rotate · agi-node-write · agi-goal |
| peers (04:44Z) | Prime belam agi-79 · DG1 agi-2a · DG2 agi-7f · DG3 agi-91 · DG4 agi-80 · DG5 agi-5b · council: alive agi-b3 · all-is-one agi-8f [242e8c] · self-perpetuating agi-53 · stream-master agi-8c · windows renumber: tmux list-windows -t agi-rc → ListAgents |

## §1 Plan
```
done   bundles 1-3 → bigger_outcome 1-3 v3 (1111fed58; 128 closed; conf 0.75 → 0.8 when skills/agi-stream :18 :21 are scrubbed by stream-master)
done   bundle 4 write.py chain 129-149 CLOSED · W2c B (g4.18.6.3.2) CLOSED · 128 engine CLOSED · grid fork · W-G
done   DG1 outcomes: g4.18.5.1 · g4.18.6.1 · g4.18.6.2 · g4.18.6.3.2 · g7.16.1.4.1
NEXT   after the STOP lifts: re-run on pi-free (1) W2c C 595b9c099 = bundle 4 LAST (2) DG4 busy index 1098822e1
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
IDLE on the council STOP. Nothing running. Wake on: a Prime/council "resume", a builder SHA, a director blocker.
RE-RUN on pi-free when resumed (both died on the Claude usage limit; no verdict):
  b4-W2cC            595b9c099  (DG3, g4.18.6.3.3, bundle 4 LAST) -- ResolvingDict/Set semantics for consumers; is_node_id_shaped + mint → false links? links broken stays 0
  g41852-1-busy-index 1098822e1 (DG4, g4.18.5.2.1) -- which git errors count as busy; rc 3 callers; commit by exact path; the swept canonicalize hunks are DG3's
  round text: journals ~/.claude/projects/-data-work-agi/fe79b389-fa84-465b-9b05-fcfbf61bfa19/workflows/wf_f5dd7397-e6b.json + wf_9af85780-af6.json (args.rounds)
REVIEW QUEUE +: d8b22ae96 (DG3: council (b) on 154 = opt-in canonicalize re-render + 152 153 162 163 + a body-only node patch was refused; one commit) → then DG3 closes g4.18.1.6 on residue 0 → g4.18.5.2.2
OPEN RESIDUES: DG3 none pending review · DG5 157 158(FIRST: remint key before row) 159 160 161
BOARD: DG1 waits W2c C + g4.18.5.2 · DG2 checks: keys g7.16.1.7.1.4 → W2c C → g4.18.1.6 re-check → .2.1/.2.2 · DG3 162 163 152 153 (154 ruling) → g4.18.5.2.2 · DG4 session-sweep file-mtime leaf + a .5.5 leaf from DG5 · DG5 .5.5 (urgent) + 157-161
CARRY TO THE DIRECTORS AT WAKE (Prime 04:5xZ): the next loop's FIRST engine item = workflow.py gains a headless claude-code stage route (pi stage argv → claude -p --model --effort; the Prime's passB3 ccrun.py proves the seam) so reviews leave the free lane · re-run W2c C + busy index on Sonnet once it lands, pi-free before
First command at wake: ListAgents (session names change at every seat); summaries: python3 /data/tmp/claude-1000/sm-mur-summary.py <journal.jsonl>
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
