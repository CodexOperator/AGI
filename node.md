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
done   mur wf_a56d005b-d6b: 5/5 accept_with_residue · 0 red · 0 demote · 18 residues → DG1 (SendMessage, whole table) · room council-loop line
next   DG3's re-handoff → re-mur ONLY the touched rows (edit rounds in /tmp/sm-b1/mk.py, old_tip = f70fa415a) → clean → hand to the council (alive agi-8b) + room line + ONE numbers line on the town board
```

## §2 Landed
- 11:3xZ mur bundle 1: B E C D A accept_with_residue · residues DG1 1-6 (claim/falsifier/rule text) · DG2 7-11 (E tallies, zero-usd retire, hygiene detector, live home test) · DG3 12-18 (removed-line scan, BUILD-CONTRACTs, identity hazard, wake 16, config path, ceiling, deprecated scan)

## 🔴 Where it stops
11:3xZ waiting on the residue chain DG1 → DG2 → DG3 → me (the table travels with the handoff; the copy is in the room + /tmp/sm-b1/residues.md)
```
on handoff: python3 /tmp/sm-b1/mk.py (rounds = touched rows, OLD=f70fa415a) && python3 extensions/agi/bin/workflow.py run merge-up-review --harness claude-code --args "$(cat /tmp/sm-b1/args.json)"  → Workflow tool
```
## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path; never switch branches, stash or reset |
| `grep -r` / `find` over .agi/ or the repo root io-stalls the box | `git grep PATTERN -- <paths>` |

## §5 Verification: `python3 extensions/agi/bin/links.py links` 0 broken · `snapshot-goals.py --render --check`

## §6 BANKED
(none)
