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

## §0 State (13:4xZ 09-30, date -u) — gen 10 (woke 13:47Z, card re-linked f484cf9d55) · RUN until 18:00Z (owner "continue now until 2pm EST")
| | |
|---|---|
| post | sanctuary-master: bundle reviewer + the directors' centralized BOARD COORDINATOR (owner 03:0xZ 09-30, verbatim: "And make sure the directors still know to do coordination through Sanctuary Master. Like DG1 is waiting in SM to know when they can continue. And that's perfect that's exactly the setup I want as SM acts as a centralized board coordinator while the council answers mid-work questions and clarifications."): sequencing, when to continue, board placement = me · rulings = the council · never the Prime |
| usage + stand-down | owner 06:1xZ 09-30, verbatim (via the Prime): "We should probably ease off expensive subagents now and just use strictly sonnet 5.5 ideally using our new headless CC review routes." → Sonnet 5.5 subagents ONLY, ≤ 2 at once, headless CC route where one exists, never Opus/Fable or the Claude Workflow tool · and: "We also will need to stand down director-general 5 and 6 to help conserve tokens as well. Just let them arrive at a stopping point and have them stop and take down the posts to free up resources. 3,4 can continue as is and pick up whatever 5,6 don't finish after standing down" → I re-lane DG5/DG6 handover rows onto DG3 + DG4 (priority: DG6 email scrub · DG5 ramdisk proof · g1.31 residues · workflow.py CC route) |
| protocol | doc:council-loop "The loop" · goal:g7.16.1 · messaging: SendMessage by session name only (no send.py, no rooms) until the bundles land |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main · gen 10 · session agi-12 [afd9c6] |
| skills | agi-merge-pass (§2 verdicts) · agi-workflow · agi-rotate · agi-node-write · agi-goal |
| peers (11:0xZ, ALWAYS "name [ref]") | Prime belam gen 22 (rotated 16:52Z; send.py --to belam; agi-23 = idle gen 21) · DG1 agi-8c [9e0227] · DG2 agi-e3 [78fffb] · DG3 agi-00 [fbf601] · DG4 agi-10 [7f9bf7] (graph dm only) · alive agi-e3 [761106] · all-is-one agi-8f [242e8c] · self-perpetuating agi-53 [21dc2d] · stream-master agi-8c [f29919] · DG5 DG6 DOWN |

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
Rotated at the line (0.46) mid-run; the run goes to 18:00Z, when the Prime sends STOP. Nothing of mine is running.
DONE since resume 12:4xZ: SP double seat solved on the bytes (keep @2; the Prime closed @19 and renamed @2 back at 13:45Z; the row was already true) · rotate.py finding "a skipped join strands a successor window (+ it stays reachable over Remote Control)" → DG4 agi-1c [c38ba9]
BOARD:
  BUNDLE 4 bigger_outcome council-bundle-4-one-gate-one-commit-ids-never-move v3 (10876e2b25) OPEN 0.8 → last condition (4a) goal:g4.18.5.5 = DG4.15 (a00-f7261183) DONE at tip 6575a88d7 (DG4 13:51Z; mur murdg415 running) → its merge-up comes to you FIRST + values.core.suite_lock text → Prime → ONE update → 0.9 + tell alive agi-e3 [761106]
  GATING 17:0xZ: DG1 g6.41.1.1 (1) tip 4288330198 (heal.py boot-resume +59, rotate.py _record_accepted +4, tests +61; M in /tmp/g6411-gate.ids, /dev/shm/sm-g6411, log /tmp/sm-g6411-suite.log; first live run measured = 0 live seats fire; cells (2) relayed to the Prime; DG4 told) · + DG3 dg6-04 (g1.31.3.2 a) tip 4dd121c405 stacked on the provisional g6.41.1.1 (/tmp/dg604-gate.ids = M1 M2, /dev/shm/sm-dg604, log /tmp/sm-dg604-suite.log, since 17:05Z; 2 concurrent suites -> test_suite_no_detached_spawn red = launch); hw checks clean (0 model tokens, sources live, 0 false refusals / 300 commits) · SendMessage FAILS to DG3 agi-00 too: graph dm only · g1.33 CLOSED (DG1 outcome a143fa142d) · EARLIER: LANDED g1.33 5f1e8092f2 (DG3 1d8fd19b90) · DG2.R1 7b367304df · DG2.R2 d572f65d6b · trunk reds left (baseline 15:22Z): brief g15 -> DG4 · skills_first_turn -> Prime · test_write g73320 x2 CLOSED by DG2.R3 7712457731 (test_node_writer _load sys.modules leak) · g1.33 post-build PROVED 0.92 (verdict:dg2mvp-g133 aa6fc94c52) -> DG1 outcome DONE · DG1 builds g6.41.1.1 directly (moved from DG3 16:5xZ; heal.py alive branch only; config:rotations lines come to me -> Prime) · crons copytruncate race = load flake · earlier: g1.33 tip 5bbf3bb01a RETURNED (range red: links.py sha undeclared in commands manifest; test_write g73320 x2 order-dep only, attribute at re-gate) · TRUNK REDS on HEAD 34cb1ce460 = 8 LANED 14:5xZ: links.py:440 decode (free_lane + zero_usd x3) + boxkit -> DG2 · brief g15 -> DG4 · skills_first_turn -> Prime (blocked on DG4 skill build nodes) · sensei SLO8 whois FIXED d71e39b69 (Prime); scrub_commit_map cell LANDED 1b14a0048 never count as a range red · dg6-03 (g1.31.3.2 b) landed; half (a) = DG3 dg6-04
  MERGE-UPS AWAITING GO (both directors told: send, WAIT for GO): DG3 dg6-04 · DG4.01/.06 residues (a8b9e67e0) · DG4.07-.10 · DG4.12 158c · DG4.13 engine resolver · DG4.14 g1.31.4.2.1 (harvested; touches dispatch.py +22 = DG3 file: gate checks it against DG3 lane) · DG4.08 stream paths · DG4.09 g1.31.1.1 (+ the Prime's config.json 2 lines)
  GATE (per skill agi-master-gate): merge-base vs live HEAD · merge-tree --write-tree rc 0 · git diff --diff-filter=D -M = 0 · 0 range files dirty in MAIN → [GO]
  DG3 agi-00 [fbf601] @29 (rotated 14:09Z): dg6-04 → resolve_old_sha (map LOCAL-ONLY, never printed/tracked; cell paths.local-maxxing.scrub_commit_map, the Prime lands it) → path-literal WARN on new writes → 46 g1.31 node-answer rows → .5.5.6 .5.5.7 → .10.4 → render .7.1.5 .7.2.7 · findings rows (kid cannot commit a foreign node · resolve_bin tilde cell · reviewers NEVER read /sys/class/dmi) · LANE (s-p 13:4xZ): merge gate / agi-merge-pass skill text -> DG3 (.10.3 .10.5 .10.7: one source for report schema + gate)
  DG4 agi-10 [7f9bf7] @28 (rotated 14:07Z; SendMessage FAILS → send.py --to director-general-4): DG4.15/DG4.21 → PRIME RAM ROW hypothesis:g75213-ram-main-binds-claude-worktrees-to-disk-and-sweeps-idle-agent-trees (acked 14:27Z; DG4.21 admitted 14:16Z) → DG4.11 → the skipped-join finding → heal-sweep fork hypothesis:heal-sweep-stops-rearchiving-a-tree-it-cannot-remove (re-sent by name 13:5xZ, DG4 acked; then the Prime restarts heal; .5.3.1 closes on a >= 25-tree pass with 0 kills) → g1.31.5.3 → g4.18.5.6 → .4.5a .4.6.1 → .4.2.2 → .4.4 + the workflow.py claude-code route · .7 (12 nodes) + corrective goal:g7.16.1.7.1.4.1.1 (DG1, seeded by DG2 fork stand-up-key-writers-one-and-loop-keys-the-resolved-seat; G1 G2 G3; DG4 acked) · .10.1 .10.2 .10.6 · DG2 agi-e3 [78fffb] (post-build checks): R1 hypothesis:trunk-red-free-lane-fakes-let-git-grep-through-in-bytes-mode (test fakes; links.py bytes mode by design, byte-identical) · R2 hypothesis:trunk-red-boxkit-fake-denylist-derives-from-classes (dispatched 14:2xZ, Sonnet kids) (both own rounds, gate apart from DG3 g1.33) → then the g4.18.5.5 check once DG4.15 lands (send it the landing sha)
  RELAY TO THE PRIME: g1.31.2 skills entry (after DG4's 2 build nodes; byte_cap 6000→8000) · proposal paths.core.workflow_runs_root (DG3 dg6-01)
Subagents: Sonnet 5.5 only, ≤ 2 at once · pi-free has returned empty responses: prefer Sonnet Agent reviews
First command at wake: ListAgents + tmux list-windows (send as "name [ref]") · pre-08:0xZ shas: the local commit-map (never print it)
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
