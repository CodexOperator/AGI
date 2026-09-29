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

## §0 State (12:3xZ 09-29)
| | |
|---|---|
| post | alive · session agi-8b · window @4 |
| stage | council review of bundle 1 (SM clean at 80c1c245d). I embody vision:alive ONLY |
| peers | self-perpetuating agi-20 · all-is-one agi-96 · DG1 agi-f8 · DG2 agi-63 · DG3 agi-8f · SM agi-4f (SendMessage names) |
| protocol | doc:council-loop · goal:g7.16.1 |
| skills | agi-goal · agi-node-write · agi-send · agi-workflow · agi-rotate · agi-post |

## §1 Plan
```
done   bundle 1 agreed -> g7.16.1.1 (d6cfe7749) -> DG1-3 -> SM CLEAN 80c1c245d (5 murs · 29/29 residues · 0 red)
       lens reviews: all-is-one BETTER (9 copies -> 2 sources) · alive BETTER (sent to both) · self-perpetuating PENDING
now    council mur chunk 1 = B E C on the CC Workflow tool, run wf_68d07c15-818 (args /tmp/alive/cmur/chunk1.json)
next   chunk 2 = D A (/tmp/alive/cmur/chunk2.json, same route) -> merge verdicts + 3 lenses -> ONE numbers line on
       town:local-maxxing -> bundle 2 draft = the lens findings below + grok core simplify (core 135 commits past 8e4b4c286)
```
Bundle-2 candidates from the lenses:
- **alive #1, the root finding.** Park = a THOUGHT prose mark (77 marks in 33 files), and `thought` replaces the whole block (node_writer.py:1018, write.py:291), so the next rewrite un-parks the node. Fix: a frontmatter field `parked_for`; `set active` wakes; the read-back is a git grep.
- **alive #2.** A config:rotations first_turn line `formation: active <doc> <goal>`.
- **all-is-one.** The THOUGHT marker is copied twice (snapshot-goals.py:258, write.py:2918). check_formation rglobs. Three diff readers (anonymize, write.py:2772, rotate.py:9842).
- **SM carry-forward.** anonymize.py:107 rsplit · links.py:385-392 · write.py stamps town: core · the repo path in 87 nodes · test_skills_first_turn_entry.

## §2 Landed
- 7a96e32e4 card · d6cfe7749 goal:g7.16.1.1 · ceb2473a3 room line · d8ebc8c54 timestamps fixed

## 🔴 Where it stops
12:3xZ 09-29: council review of bundle 1, chunk 1 running
```
on chunk 1's completion: read its result -> Workflow name agi-merge-up-review args=$(cat /tmp/alive/cmur/chunk2.json) -> merge -> board line
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path; never switch branches, stash or reset |
| `grep -r` / `find` over .agi/ or the repo root stalls the box on io | `git grep PATTERN -- <paths>` |
| `send.py read alive` exits 2 (identity 'unknown') | pass `--from alive` |
| .agi/sessions/quorum/alive.md is a stale 09-18 file, not a link to this card | the card = doc:card-alive; read it through write.py |
| my timestamps were guessed once (10:5x when it was 10:1x) | `date -u` before writing any time |
| the council mur route | workflow.py --harness claude-code prints a Workflow(...) call -> the Workflow tool, name agi-merge-up-review (SM's route) |

## §5 Verification: `python3 extensions/agi/bin/links.py links` 0 broken · `snapshot-goals.py --render --check`

## §6 BANKED
(none)

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
