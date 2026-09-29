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

## §0 State (11:3xZ 09-29)
| | |
|---|---|
| post | sanctuary-master |
| stage | the bundle reviewer — standard mur on claude-code at Opus 5.5 high (owner 09-29 authorizes the Workflow tool for this review, over skill agi-workflow's pi-only rule, in this mode) |
| protocol | doc:council-loop (read it first) · goal:g7.16.1 (the owner's words) |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main · claude-code Opus 5.5 high · seated 10:3xZ 09-29 by belam · session agi-4f (@10) |
| skills | agi-merge-pass (§2 verdict rules) · agi-workflow · agi-send · agi-rotate · agi-post |
| bundle 1 | goal:g7.16.1.1 · range d6cfe7749..f70fa415a · 5 rounds B E C D A · DG1 agi-f8 @7 · DG2 agi-63 @8 · DG3 agi-8f @9 |

## §1 Plan
```
done   mur-1 wf_a56d005b-d6b: 5/5 accept_with_residue, 18 residues → chain → fixed at eae790aea · mur-2 wf_aa3f01d4-2aa: 18/18 CLOSED + 6 new (19-24) → DG1 (agi-f8)
next   DG3's re-handoff → mur-3 over eae790aea..<tip> on the 6 items only (rows B E C D A; table /tmp/sm-b1/residues2.md) → clean → alive (agi-8b) + room + ONE board numbers line
```

## §2 Landed
- mur-1 bundle 1: 18 residues (DG1 6 · DG2 5 · DG3 7), 0 red, 0 demote
- 11:5xZ mur-2: 18/18 closed · 6 new: 19 B claim (3) names links.py (DG1) · 20 E row text on g7.16.1.1:36 (DG1) · 21 staged branch unpinned (DG2) · 22 added_lines drops path headers (DG3) · 23 stale contracts bin-node-writer + bin-snapshot-goals (DG3) · 24 owed command lacks git add (DG3)

## 🔴 Where it stops
12:0xZ mur-3 wf_16ffb9a5-596 running over eae790aea..30684908b on rows 19-24 only (args /tmp/sm-b1/args3.json)
```
if this session died: Workflow({scriptPath: "<session>/workflows/scripts/agi-merge-up-review-wf_16ffb9a5-596.js", resumeFromRunId: "wf_16ffb9a5-596"}) · clean → SendMessage alive (agi-8b) + room line + ONE board numbers line
```
## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path; never switch branches, stash or reset |
| `grep -r` / `find` over .agi/ or the repo root io-stalls the box | `git grep PATTERN -- <paths>` |

## §5 Verification: `python3 extensions/agi/bin/links.py links` 0 broken · `snapshot-goals.py --render --check`

## §6 BANKED
(none)
