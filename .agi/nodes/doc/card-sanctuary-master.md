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

## §0 State (15:3xZ 09-29)
| | |
|---|---|
| post | sanctuary-master: the bundle reviewer, standard mur on claude-code at Opus 5.5 high (owner 09-29 authorizes the Workflow tool for this review, over skill agi-workflow's pi-only rule, in this mode) |
| protocol | doc:council-loop · goal:g7.16.1 |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main |
| skills | agi-merge-pass (§2 verdict rules) · agi-workflow · agi-send · agi-rotate · agi-post |
| peers | DG1 · DG2 · DG3 (card doc:card-director-general-3) · alive (council convener) · belam = send.py inbox (tag [merge-up]) |

## §1 Plan
```
done   bundle 1 CLEAN · bundle 2 R1, stage 3, 42, 32-40+P+43 murs · 36 41 43 44 CLOSED · 45-51 closed at 22677d774 + dd10c923f
done   belam's [red] anonymize (card hit): 0 hits since f390e1d28 · belam told
done   re-mur wf_7df27f74-d4b: accept_with_residue x2 · 0 red · T accepted → belam (formations cell) · 52-54 → DG3 (agi-aa) + room line
next   DG3's 52-54 handback → a 1-round re-mur (files: verification.py, test_formation_readback.py, write.py + its test,
       experiment:a00-6cb8a731-232b62, mvp:dg3-p-park-tag) · clean → alive + room [handoff] + ONE board numbers line
```

## §2 Landed
- bundle 1: 5 murs → CLEAN at 80c1c245d · 29/29 · 0 red · [rule] adopt → goal:g4.18.3
- bundle 2 R1 wf_8da5e93a-72f: rotations HOME 109 → 0 · 32-35 closed at 42137d050
- bundle 2 stage 3 wf_dde8f806-ce2: M R4 accept · 36 41 CLOSED · 37-40 closed
- 42 mur wf_9a00e1d9-91a demote → both items CLOSED at 899979051 · 44 → DG2, CLOSED
- re-mur wf_f6343a9c-419 (tip 697335c7c): 0 red · 45-50 → DG3 · T mur: 51 → DG3
- re-mur wf_7df27f74-d4b (87a971296..dd10c923f): 45-51 closed (47 half) · 52 re.M mark regex · 53 experiment :87-88 placeholders · 54 unpark hook prints on REJECTED → DG3

## 🔴 Where it stops
15:3xZ: idle, waiting on DG3's handback of 52-54 (send.py inbox or SendMessage). At the handback: Workflow tool, name
agi-merge-up-review, 1 round, old = dd10c923f, new = DG3's tip, focus = 52 53 54 + the 3 optional notes.

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path; never switch branches, stash or reset |
| `grep -r` / `find` over .agi/ or the repo root io-stalls the box | `git grep PATTERN -- <paths>` |
| rotate flattens the quorum card | re-link: `ln -sfn ../../nodes/doc/card-sanctuary-master.md .agi/sessions/quorum/sanctuary-master.md` |
| a home path in a card or dm | write `<home>`; check: `anonymize.py check --text "$(cat <card>)"` |

## §5 Verification: `python3 extensions/agi/bin/links.py links` 0 broken · `snapshot-goals.py --render --check`

## §6 BANKED
(none)
