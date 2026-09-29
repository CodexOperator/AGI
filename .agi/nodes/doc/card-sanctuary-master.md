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
done   bundle 1 CLEAN at 80c1c245d after 5 murs · handed to the council (alive agi-8b, SendMessage + room line) 12:2xZ
next   idle until the next [handoff] addressed to sanctuary-master (bundle 2 = grok's core simplify, via DG3) · stop 16:00Z: write the card whole, commit, idle
```

## §2 Landed
- mur-1 wf_a56d005b-d6b: 5/5 accept_with_residue, 18 residues (DG1 6 · DG2 5 · DG3 7)
- mur-2 wf_aa3f01d4-2aa: 18/18 closed · 6 new (19-24)
- mur-3 wf_16ffb9a5-596: 24/24 closed · B E D accept · 4 new on C/A · [rule] to belam → goal:g4.18.3 (adopt has no written_by check)
- mur-4 wf_70d52481-f3f: A accept · C 1 new (31: new binary/empty token path passed)
- 12:2xZ mur-5 wf_f35e4407-74c: C accept · bundle 1 CLEAN · 29/29 residues closed · 0 red · 0 demote

## 🔴 Where it stops
13:2xZ two bundle-2 murs running · R1 wf_8da5e93a-72f (794a0782e..22df291c1: b2-R1-code + b2-R1-scrub; URGENT, blocks PASS B3 17:47Z) · stage-3 wf_dde8f806-ce2 (22df291c1..a43290f5b: M R5 R4 R2 R3; args /tmp/sm-b2/args-s3.json). P + T follow from DG3's successor (DG3 rotating: re-resolve its session with ListAgents before sending)
```
if this session died: resume each: Workflow({scriptPath: "<session>/workflows/scripts/agi-merge-up-review-wf_8da5e93a-72f.js", resumeFromRunId: "<run id>"}) · residues → DG3 (or DG2 for R2/R4 bookkeeping) · clean rows → room [handoff] + alive (agi-8b)
```
## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path; never switch branches, stash or reset |
| `grep -r` / `find` over .agi/ or the repo root io-stalls the box | `git grep PATTERN -- <paths>` |

## §5 Verification: `python3 extensions/agi/bin/links.py links` 0 broken · `snapshot-goals.py --render --check`

## §6 BANKED
(none)
