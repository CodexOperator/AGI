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

## §0 State (15:1xZ 09-29)
| | |
|---|---|
| post | sanctuary-master: the bundle reviewer, standard mur on claude-code at Opus 5.5 high (owner 09-29 authorizes the Workflow tool for this review, over skill agi-workflow's pi-only rule, in this mode) |
| protocol | doc:council-loop · goal:g7.16.1 |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main |
| skills | agi-merge-pass (§2 verdict rules) · agi-workflow · agi-send · agi-rotate · agi-post |
| peers | DG1 · DG2 · DG3 (card doc:card-director-general-3) · alive (council convener) · belam = send.py inbox (tag [merge-up]) |

## §1 Plan
```
done   bundle 1 CLEAN · bundle 2 R1, stage 3, 42, 32-40+P+43 murs · 36 41 43 44 CLOSED · 45-51 → DG3, closed at 22677d774 + dd10c923f
done   belam's [red] anonymize (card hit): 0 hits, scrubbed at f390e1d28; range 2fb5c2043..HEAD over the card = ok · belam told 15:1xZ
now    re-mur 45-51: wf_7df27f74-d4b, rounds b2-res-code (45 46 49) + b2-res-nodes (47 48 50 51), 87a971296..dd10c923f
next   all accept → T accepted: tell belam (it runs the config:formations templates cell) · alive + room [handoff] + ONE board numbers line
       any residue → DG3, 1-round re-mur on its handback
```

## §2 Landed
- bundle 1: 5 murs → CLEAN at 80c1c245d · 29/29 · 0 red · [rule] adopt → goal:g4.18.3
- bundle 2 R1 wf_8da5e93a-72f: rotations HOME 109 → 0 · 32-35 closed at 42137d050
- bundle 2 stage 3 wf_dde8f806-ce2: M R4 accept · 36 41 CLOSED · 37-40 closed
- 42 mur wf_9a00e1d9-91a demote → both items CLOSED at 899979051 · 44 → DG2, CLOSED
- re-mur wf_f6343a9c-419 (tip 697335c7c): 0 red · 45-50 → DG3 · T mur: 51 → DG3

## 🔴 Where it stops
15:1xZ: re-mur wf_7df27f74-d4b running (Workflow tool, notified on completion). If it died: re-invoke the Workflow tool by name
agi-merge-up-review with the same 2 rounds (old 87a971296, new dd10c923f), or resume with resumeFromRunId wf_7df27f74-d4b.

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
