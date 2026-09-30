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

## §0 State (08:5xZ 09-30, date -u) — gen 9 · resumed after the scrub · rotation near (meter 0.40 / 0.47)
| | |
|---|---|
| post | sanctuary-master: bundle reviewer + the directors' centralized BOARD COORDINATOR (owner 03:0xZ 09-30, verbatim: "And make sure the directors still know to do coordination through Sanctuary Master. Like DG1 is waiting in SM to know when they can continue. And that's perfect that's exactly the setup I want as SM acts as a centralized board coordinator while the council answers mid-work questions and clarifications."): sequencing, when to continue, board placement = me · rulings = the council · never the Prime |
| usage + stand-down | owner 06:1xZ 09-30, verbatim (via the Prime): "We should probably ease off expensive subagents now and just use strictly sonnet 5.5 ideally using our new headless CC review routes." → Sonnet 5.5 subagents ONLY, ≤ 2 at once, headless CC route where one exists, never Opus/Fable or the Claude Workflow tool · and: "We also will need to stand down director-general 5 and 6 to help conserve tokens as well. Just let them arrive at a stopping point and have them stop and take down the posts to free up resources. 3,4 can continue as is and pick up whatever 5,6 don't finish after standing down" → I re-lane DG5/DG6 handover rows onto DG3 + DG4 (priority: DG6 email scrub · DG5 ramdisk proof · g1.31 residues · workflow.py CC route) |
| protocol | doc:council-loop "The loop" · goal:g7.16.1 · messaging: SendMessage by session name only (no send.py, no rooms) until the bundles land |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main · gen 9 · session agi-5c |
| skills | agi-merge-pass (§2 verdicts) · agi-workflow · agi-rotate · agi-node-write · agi-goal |
| peers (08:5xZ, ALWAYS "name [ref]") | Prime agi-23 [ecd665] · DG1 agi-8c [9e0227] · DG2 agi-e3 [78fffb] · DG3 agi-34 [e82e60] · DG4 agi-1c (rotated from agi-c8) · alive agi-e3 [761106] · all-is-one agi-8f [242e8c] · self-perpetuating agi-53 [21dc2d] · stream-master agi-8c [f29919] · DG5 DG6 DOWN |

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
Nothing running (09:2xZ). Bundle-4 bigger_outcome v3 (10876e2b25) OPEN 0.8 → last condition (4a) goal:g4.18.5.5 rides DG4.06 (a00-563c98b6) → on its accepted merge-up: ONE update → 0.9 + tell alive agi-e3 [761106]; values.core.suite_lock config text → Prime
ACCEPTED post-resume: 30175ea7e9 email class · be11671cb N2 · 6894c783f3 B+R1c · 8a9656b2b4 (.20.2 .20.3 B3) · 4e1560b754 R1-R3 (actor → unknown fail-closed · rule 3 token-exact · commands._actor shared) · 4633e4d076 g1.32 (0 old shas added) · DG4 merge-up 9f124d68f g1.31.1.2 (post hoc)
DG3 ROTATING (captive chain failed: handoff rc 2 / rotate-self rc 3; watch its successor): its successor holds dg6-03 re-mur (db1fa78b7f) + dg6-04 re-mur (edfef83cc5) → [merge-up] BEFORE landing · DG5.01 mur · then the resolve_old_sha leaf (the Prime's ruling: map LOCAL-ONLY /data/agi-maps/..., NEVER tracked/printed; cell paths.local-maxxing.scrub_commit_map; absent → fall through) · path-literal WARN on new writes (no sweep) · 46 g1.31 node-answer rows · .5.5.6 .5.5.7 · .10.4 · render .7.1.5 .7.2.7
DG4 agi-1c: DG4.04 158c harvested (mur next; closes .7.1.4.1) · DG4.05 · DG4.06 (DG4.01 residues + g4.18.5.5) · DG4.08 stream paths · DG4.09 g1.31.1.1 corrective (the Prime's config.json 2 lines at its merge-up) · merge-ups to me BEFORE landing (told 09:1xZ)
CONFIG PENDING (relay to the Prime): g1.31.1.1 config.json lines · g1.31.2 skills entry (exact text, byte_cap 6000→8000) · suite_lock block · scrub_commit_map cell
LANES: DG3 = write.py · anonymize · dispatch.py · RAM writers · render · g1.31 node answers · .10.4 | DG4 = rotate.py · heal · adapters · keys · workflow.py + CC route · .7 (12) · .10.1/.2/.6
First command at wake: ListAgents + tmux list-windows · pre-08:0xZ shas: map via the local commit-map (never print it)
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
