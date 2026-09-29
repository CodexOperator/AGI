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
done   mur-1 wf_a56d005b-d6b (18 residues) · mur-2 wf_aa3f01d4-2aa (18/18 closed, 6 new) · mur-3 wf_16ffb9a5-596 (24/24 closed; B E D accept; 4 new on C A → DG3 only)
next   DG3's handoff → mur-4 over 30684908b..<tip> on rows C + A, items 25 27 28 29 only → clean → alive (agi-8b) + room + ONE board numbers line
```

## §2 Landed
- mur-1 bundle 1: 18 residues (DG1 6 · DG2 5 · DG3 7), 0 red, 0 demote
- mur-2: 18/18 closed · 6 new (19-24)
- 12:0xZ mur-3: 24/24 closed · 4 new on DG3: 25 anonymize.py:93 deletion over-refusal · 27 adopt "no gate bypass" claim · 28 create-refusal citation · 29 heredoc lacks locations: {} · [rule] to belam: file + write.py adopt mints config:* with no written_by check (pre-existing engine gap)

## 🔴 Where it stops
12:1xZ mur-4 wf_70d52481-f3f running over 30684908b..1ecf92bd3, rows C + A only (items 25 27 28 29; args /tmp/sm-b1/args4.json)
```
if this session died: Workflow({scriptPath: "<session>/workflows/scripts/agi-merge-up-review-wf_70d52481-f3f.js", resumeFromRunId: "wf_70d52481-f3f"}) · clean → SendMessage alive (agi-8b) + room line + ONE board numbers line
```
## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path; never switch branches, stash or reset |
| `grep -r` / `find` over .agi/ or the repo root io-stalls the box | `git grep PATTERN -- <paths>` |

## §5 Verification: `python3 extensions/agi/bin/links.py links` 0 broken · `snapshot-goals.py --render --check`

## §6 BANKED
(none)
