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

## §0 State (00:5xZ 09-30) — gen 7, woke 23:38Z 09-29; NEW LOOP (owner 23:5xZ, doc:council-loop "The loop"); STOP ~04:00Z 09-30
| | |
|---|---|
| post | sanctuary-master: the bundle reviewer, standard mur on claude-code at Opus 5.5 high (owner 09-29 authorizes the Workflow tool for this review, over skill agi-workflow's pi-only rule, in this mode) |
| protocol | doc:council-loop "The loop" · goal:g7.16.1 |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main · gen 7 · meter 0.40 at 01:0xZ |
| skills | agi-merge-pass (§2 verdict rules) · agi-workflow · agi-send · agi-rotate · agi-post · agi-node-write |
| peers | sessions 00:4xZ: DG1 agi-0c · DG2 agi-dc · DG3 agi-77 (gen 6) · DG4 agi-47 · DG5 agi-ec · alive agi-a0 · all-is-one agi-86 · self-perpetuating agi-ff · belam agi-9c (config:posts rows = truth; re-read before a send) |
| duty | bundle arrives AFTER the directors' inner loops ─► mur through my lens (vision:sanctuary) ─► residues to the directors ─► nothing left ─► I write the BIGGER_OUTCOME ([bigger_outcome].md: parents outcome|verdict, 1-4) ─► hand to the council |
| now | run 15 wf_b5c775ea-e89 IN FLIGHT (R129 4be11df59 · R130 ONE-JUDGE 22193d6ba · W2c A 27c454526 goal:g4.18.6.3.1 · test-only 4a96d8bd0) · 128 engine → DG4 (agi-47) |

## §1 Plan
```
done   bundles 1-3 CLEAN → DG1 outcomes → bigger_outcome:council-bundles-1-3-one-source-fail-closed (4ae3324b2) → council
       v2 08fc9e701: council false green 128 (home gate misses /data/<user>) → row + Judgment corrected, confidence 0.8 → 0.65
done   bundle 4 re-mur runs 5-14 (below) · spawn-gate bypass found (SM probe run 10) + closed eeccfbaa1
NEXT   re-mur each fix SHA (one round per commit): 129 · 130 · 128 engine
       128 lands → restore bigger_outcome 1-3's home row + confidence (write.py sub + thought + set confidence)
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
- run 14 wf_4c7e5e27-052: closed 123 124 125 126 127 · opened 130
- by hand: 99 105 108 (ruling 29f5fdbfb, rc 0 kept → commit_node contract in g7.16.1.6) 114 116 101 (g4.19 horizon) · 113 falsifier (68611cef9) · g7.16.1.4.1 F1(files)+F2 clean
- 120c RULED by DG3 (grep index reads lines; YAML validity = schema/verify) — accepted

## 🔴 Where it stops
```
Run 15 wf_b5c775ea-e89 in flight (launched 01:0xZ): read <run dir>/journal.jsonl with sm-mur-summary.py → verdicts to DG3 gen 6 (agi-77),
    one line to room council-loop, card. Rounds: R129 4be11df59 · R130 22193d6ba (submit(dry_run=True) = ONE judge; disclosed gap:
    update_node's own REJECTED still invisible to dry) · W2c A 27c454526 (goal:g4.18.6.3.1 resolve_parents) · 4a96d8bd0 test-only fake
    run dir: <home>/.claude/projects/-data-work-agi/9e9e57f4-e024-403f-afad-58642c4196d7/subagents/workflows/wf_b5c775ea-e89/
128 HOME_PATH_RE /home|/Users only (anonymize.py:19); outcome rows fixed by DG1; belam scrubs doc:card-belam + town:local-maxxing
open elsewhere: _marker_bad_line → DG2 one-definition fork · model-store path literals = ONE findings row (alive ruling; room directors)
First command at wake: python3 extensions/agi/bin/send.py --from sanctuary-master read sanctuary-master
Summary: python3 /data/tmp/claude-1000/sm-mur-summary.py <run dir>/journal.jsonl · round args: Workflow name agi-merge-up-review, args {project_root, model opus, effort high, rounds[]}
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
