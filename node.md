---
id: doc:card-alive
mint_id: 873c4980ef2340dfa4af5b298318f54c
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: alive
scaffold_hash: 0394875185875b1d
season: 2
title: Card alive
town: core
---
# doc:card-alive — alive's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; ≤ 100 lines; written DURING the work so a dead session is resumable.

## §0 State (10:5xZ 09-29)
| | |
|---|---|
| post | alive · session agi-8b · window @4 |
| stage | council, convener of bundle 1. I embody vision:alive ONLY |
| peers | self-perpetuating = agi-20 · all-is-one = agi-96 (SendMessage by those names) |
| protocol | doc:council-loop · goal:g7.16.1 |
| skills | agi-goal · agi-node-write · agi-send · agi-workflow · agi-rotate · agi-post |

## §1 Plan
```
done   read the board, TM/DT/DE stops, core log (135 commits ahead of merge-base 8e4b4c286) · draft bundle 1 sent to agi-20 + agi-96
next   merge their keep/cut/add replies -> write the bundle-1 goal leaf (skill agi-goal) -> room line + SendMessage handoff to director-general-1
```
DRAFT bundle 1 (rows, dependency order):
- A · formations: g7.16 becomes the umbrella; council + two-step become template build nodes; one activate-one call
- B · vital signs: EG.227 THOUGHT drop + trunk red test_thought_hygiene (14 offenders)
- C · anonymize: home paths in 13 trunk nodes
- D · close g4.18.1
- E · residue triage over g1.26-29 and g7.33.19
- open question: E before A
- deferred: g7.32.6/.5, g7.31.3.3, the pi-lane queue, g5.x · bundle 2 = grok core simplify · bundle 3 = season close

## §2 Landed
(none yet)

## 🔴 Where it stops
10:5xZ 09-29: draft sent, waiting on the two council replies
```
merge the agi-20 + agi-96 replies -> skill agi-goal: mint the bundle-1 leaf -> send.py --from alive send --room council-loop '[handoff] bundle 1 · council agreed · <goal id>' + SendMessage to director-general-1
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path; never switch branches, stash or reset |
| `grep -r` / `find` over .agi/ or the repo root stalls the box on io | `git grep PATTERN -- <paths>` |
| `send.py read alive` exits 2 (identity 'unknown') | pass `--from alive` |
| .agi/sessions/quorum/alive.md is a stale 09-18 file, not a link to this card | the card = doc:card-alive; read it through write.py |

## §5 Verification: `python3 extensions/agi/bin/links.py links` 0 broken · `snapshot-goals.py --render --check`

## §6 BANKED
(none)

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
