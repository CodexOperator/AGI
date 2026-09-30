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

## §0 State (03:14Z 09-30, date -u) — gen 8 · run 26 RUNNING (DG4 cold homing); meter ~0.37; write.py chain CLEAN; 148 149 with DG3; 144-147 with DG3; 144-147 with DG3; NEW LOOP (owner 23:5xZ, doc:council-loop "The loop"); STOP ~04:00Z 09-30
| | |
|---|---|
| post | sanctuary-master: ALSO the directors' centralized BOARD COORDINATOR (owner 03:0xZ 09-30, verbatim: \"And make sure the directors still know to do coordination through Sanctuary Master. Like DG1 is waiting in SM to know when they can continue. And that's perfect that's exactly the setup I want as SM acts as a centralized board coordinator while the council answers mid-work questions and clarifications.\"): sequencing, when to continue, board placement = me · rulings, mid-work questions = the council · never the Prime. And the bundle reviewer, standard mur on claude-code at Opus 5.5 high (owner 09-29 authorizes the Workflow tool for this review, over skill agi-workflow's pi-only rule, in this mode) |
| protocol | doc:council-loop "The loop" · goal:g7.16.1 |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main · gen 8 · meter 0.28 at 02:56Z |
| skills | agi-merge-pass (§2 verdict rules) · agi-workflow · agi-send · agi-rotate · agi-post · agi-node-write |
| peers | 02:5xZ (SendMessage names): Prime belam agi-79 · DG3 agi-91 [87eb1e] · DG4 agi-80 · DG5 agi-5b · others: tmux list-windows -t agi-rc → ListAgents |
| duty | bundle arrives AFTER the directors' inner loops ─► mur through my lens (vision:sanctuary) ─► residues to the directors ─► nothing left ─► I write the BIGGER_OUTCOME ([bigger_outcome].md: parents outcome|verdict, 1-4) ─► hand to the council |
| now | run 26 wf_84774171-117 (5a257979b g7.16.1.5.3.2 cold homing) → on accept route ONE heal restart to the Prime · bundle 4 waits on W2c C only · g4.18.1.6 residues 150-155 with DG3 |

## §1 Plan
```
done   bundles 1-3 CLEAN → DG1 outcomes → bigger_outcome:council-bundles-1-3-one-source-fail-closed (4ae3324b2) → council
       v2 08fc9e701: council false green 128 (home gate misses /data/<user>) → row + Judgment corrected, confidence 0.8 → 0.65
done   bundle 4 re-mur runs 5-14 (below) · spawn-gate bypass found (SM probe run 10) + closed eeccfbaa1
NEXT   re-mur each fix SHA (one round per commit): 131 · 132 · 128 engine
       done: bigger_outcome 1-3 v3 (0.75); → 0.8 when skills/agi-stream :18 :21 are scrubbed (stream-master)
       bundle 4 CLEAN → [ready] to DG1 (agi-0c) → its outcome(s) → next bigger_outcome (bundle 4, lens vision:sanctuary) → council
       .6 / .7 bundles (DG3 machinery · DG4 callers · DG5 spawn) as delivered; g7.16.1.6 review carries 108's requirement
```

## §2 Landed (bundle 4, all CC opus, 0 agent errors)
- run 5 wf_884739ac-f61: closed 91 92 96 97 · opened 106 107
- run 6 wf_40b19c77-7f2: closed 98 99 100 102 103 104 106 107 + L2a(a) · opened 108-111
- run 7 wf_7c3c15ad-a10: W1a corrective → 112-115 (113 = SM lens over the refuter: a closed goal's end-state regressed behind a green falsifier)
- run 8 wf_35fe675a-d5b: L2a(b) → 116 (closed by hand 481ecfde6) · 393992bbf hand-accepted
- run 9 wf_e2af26ea-3a7: closed 109 111 112 113 · opened 117 118 120 121 (+119)
- run 10 wf_a494f517-453: W2b.1 → 122 + the create --set parents probe
- run 11 wf_2ec2e1c6-d2c: W2b.2 → 119 closed · 123 124
- run 12 wf_928ddd3b-1f1: closed N2 N3 117 121 120a · opened 125 126 127
- run 13 wf_35753f5e-852: closed 118 122 + the spawn-gate bypass · opened 129
- run 15 wf_b5c775ea-e89: closed 129 130 (ONE judge, structural) + W2c A 27c454526 + 4a96d8bd0 · opened 131 132
- run 16 wf_1d7d51dd-720: closed 131 132 + probe (e77d0515a) + W2c B1 (d3f1d80c0) · opened 133 134 (e77) 135 136 (B1) · 4a420102e by hand
- run 25 wf_bcdbb290-f95: g4.18.1.6 a6102199b → 150 (scaffold_hash PROTECTED bypass) 151 (pre-submit gates blind to translated rows) 152 (2 THOUGHTs) 153 (traceback) 154 (not byte-exact; format hunks discarded) 155 cand (ring-fields signs untranslated)
- by hand: grid fork 6ec1f046c ACCEPT (red parent / green commit; test_grid 147p) → g4.18.6.3.2 ready (DG1 told; DG2 #2)
- by hand 03:08Z: 148+149 f0768720f + 6e21d9655 (g4.18.1.6 route refusal) ACCEPT (new tests red on parent, green on commit) → write.py chain 129-149 CLOSED
- run 24 wf_f800b604-eac: 144 b1f0e415f+033d75454 ACCEPT · 145-147 4538ed382 → 148 (000 dest: the check's own read = traceback) 149 (0200 dest: stamp then raise) · fix = os.access(R_OK|W_OK)
- run 23 wf_e3879214-a8b: 128 engine b0bc1699f (DG4) ACCEPT clean → 128 CLOSED · bigger_outcome 1-3 v3: home row + Judgment restored, conf 0.65 → 0.75 (0.8 when the stream literals are scrubbed)
- run 22 wf_67b2c3c8-b01: 140 b514b6d47 accept → 144 (empty body_patch - + verb dropped, code-read) · 142+143 eb91a95aa → 145 (2nd-writer blind to shared payload_bytes) 146 (read-only dest stamps then raises) 147 (unreadable src = traceback) · 141 51c664397 by hand
- run 21 wf_ba35a1b8-2ef: 138 8964a7c62 ACCEPT clean (one _HEAD + one _END; 0/5310 rows change) · notes: brief.py:2520 level3.py:267 links.py:391 own closers → DG2 fork
- run 20 wf_2e792c7e-029: 139 74f03f003 (empty `patch -` refused) → opened 142 (empty patch RESULT → data None → ValueError after the stamp, :2583) 143 (payload src/dest existence judged after the stamp)
- run 19 wf_e2faecc7-e15: 136 9a39d55fa ACCEPT clean · 135 3b61f9f73 → opened 141 (test_sm135 asserts twins equal, not == [0, 0]: a both-twin :790 bug or :805 `pass` stays green)
- run 18 wf_4a1d4109-831: 133 854aceb35 + 134 688d86d6f → opened 138 (END tail) 139 (empty patch - half-writes, PRIORITY) 140 (empty payload - + verb dropped)
- run 17 wf_c52bee27-302 (stopped at the hold, resumed): B2 7e1bed5b8 ACCEPT clean · B3 9c069f7dc opened 137 (plan_reid unwired + undisclosed)
- run 14 wf_4c7e5e27-052: closed 123 124 125 126 127 · opened 130
- by hand: 99 105 108 (ruling 29f5fdbfb, rc 0 kept → commit_node contract in g7.16.1.6) 114 116 101 (g4.19 horizon) · 113 falsifier (68611cef9) · g7.16.1.4.1 F1(files)+F2 clean
- 120c RULED by DG3 (grep index reads lines; YAML validity = schema/verify) — accepted

## 🔴 Where it stops
```
DONE runs 16 17 18 · 137 09a8397e4 ACCEPTED by hand (THOUGHT closes the site list; plan_reid exempt by contract identity.py:290-292, no caller; note: node stamped edited_by belam, written by DG3)
RUNNING run 26 wf_84774171-117 (task w7dckc8o7): g716153-2-cold-homing 5a257979b (DG4) -- byte loss / rmtree through link = DEMOTE; accept → SendMessage the Prime agi-79: ONE heal restart for b3b0024db + 4c6972981 + 5a257979b, falsifier: one pass homes N>=1 with tmpfs + engine shmem flat +/-20 MiB
BUNDLE 4 REMAINDER: W2c C (g4.18.6.3.3, DG3) only → review → full [ready] to DG1 → DG1 outcomes → my bundle-4 bigger_outcome → council
QUEUES SET (board):
  DG1 agi-2a: outcomes written g4.18.5.1 (556131169) g4.18.6.1 (0eef20bd9) · ready: g4.18.6.2 (council ruling pending on body refs) g4.18.6.3.2 · g4.18.5.2 waits on .2.1 + .2.2 builds
  DG2 agi-7f: (1) g4.18.1.6 MVP pass, HOLD verdict until 150/151 land (2) grid fork 6ec1f046c (3) W2c C · later .5.3.2, g4.18.5.2.1/.2.2
  DG3 agi-91: (1) 150+151(+155) (2) W2c C (3) 152 153 154 (4) g4.18.5.2.2 -- NOT write.py _commit_write (DG4's)
  DG4 agi-80: (1) cold homing DONE 5a257979b (in run 26) (2) g7.16.1.4.1.2 (W-G's last leaf) (3) g4.18.5.2.1 index.lock bounded retry (owns _commit_write)
  DG5 agi-5b: (1) .5.4 shmem cause (2) .5.5 RAM-disk budget line (Prime-assigned, urgent: engine cap 3G stopgap) (3) .1.4 keys
NEXT: one mur round per fix SHA as DG3 sends them (SendMessage; DG3 = agi-8f [e68acb], two agi-8f → always the ref) · then bundle 4 CLEAN → [ready] to DG1
MESSAGING until bundles land (owner verbatim): "use internal messaging only for everything and full guarantee until bundles land. Use the town bundles and goal nodes to coordinate context among the council and directors." → SendMessage; NO send.py, NO rooms · Prime = agi-79 (gen 20)
4a420102e test pin: accepted by hand (still asserts rc 2; only the refusal's words moved)
DG3 finding → belam (node owner): hypothesis:l2w6-telemetry-rollup has a scalar next_edges; its schema wants a list
open elsewhere: _marker_bad_line + brief.py:2520 / level3.py:267 / links.py:391 closers → DG2 one-definition fork · model-store path literals = ONE findings row (alive ruling; room directors)
At wake / on each run notification: python3 /data/tmp/claude-1000/sm-mur-summary.py <transcript dir>/journal.jsonl → residues to DG3
Round args shape: ~/.claude/projects/-data-work-agi/9e9e57f4-*/workflows/wf_b5c775ea-e89.json (run 15) · Workflow name agi-merge-up-review
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
