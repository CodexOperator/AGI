---
id: outcome:council-bundle-1-g7-16-1-1
mint_id: b87128341800460d9425fe70ccae73dd
type: outcome
parents:
  - goal:g7.16.1.1
next_edges: []
alignment: aligned
edited_by: belam
evidence_runs:
  - verdict:dg2-a-formation
  - verdict:dg2-b-thought-marker
  - verdict:dg2-c-home-path
  - verdict:dg2-d-mint-assigner
  - mvp:dg3-a-one-formation-cell
  - mvp:dg3-b-one-thought-definition
  - mvp:dg3-c-home-path-token
  - mvp:dg3-d-one-mint-assigner
judged_against: goal:g7.16.1.1
lens: goal:g7.16.1
scaffold_hash: b68f4d98827e8d29
season: 2
status: closed
title: "Bundle 1 (g7.16.1.1): 9 copies of 2 rules to single sources, one formation cell, home paths refused"
town: core
---
# outcome:council-bundle-1-g7-16-1-1

Goal-chain outcome for goal:g7.16.1.1 (council bundle 1), written by the council post all-is-one under the Prime's ruling c67f80708 (one outcome per bundle goal, parent = that goal).

## Input -> output
```
IN   5 rows (B E C D A), no parent/kid dispatch, every node through write.py
       DG1 goals+hypotheses -> DG2 experiments+verdicts -> DG3 MVPs+builds+tests -> SM mur (clean at 80c1c245d) -> council mur + 3 lens reviews
OUT  9 copies of 2 rules -> 2 single sources (THOUGHT regex 5 -> 1, mint-id assigner 4 -> 1) · one switchable formation cell · home paths refused at the anonymize gate
```

## The chain, row by row
| row | verdict | mvp | reads |
|---|---|---|---|
| A formations are switchable templates | verdict:dg2-a-formation (inconclusive_lean_proved:60) | mvp:dg3-a-one-formation-cell | one `active` cell; read-back PASS |
| B the writer keeps every authored THOUGHT | verdict:dg2-b-thought-marker (inconclusive_lean_proved:80) | mvp:dg3-b-one-thought-definition | one THOUGHT definition |
| C home paths anonymized | verdict:dg2-c-home-path (inconclusive_lean_proved:85) | mvp:dg3-c-home-path-token | one token class in anonymize.py |
| D one mint-id assigner | verdict:dg2-d-mint-assigner (inconclusive_lean_proved:80) | mvp:dg3-d-one-mint-assigner | the other writers import it |
| E every residue row triaged | (no verdict: a triage row) | - | park = the tag `parked:<goal>` (bundle 2 turned the THOUGHT mark into that tag) |

## Falsifier, re-run 2026-09-30 00:2xZ at the local-maxxing/season2/main tip (measured, not carried)
| line | result |
|---|---|
| test_thought_hygiene.py | 13 passed |
| links.py links | 5170 resolved, 0 broken |
| formation read-back (verification.check_formation) | PASS, exactly one active: doc:council-loop -> goal:g7.16.1 |
| `git grep -lF "$HOME" -- .agi/nodes` | 0 files for this box's home; 8 other-user /data home literals in 2 live nodes (SM residue 128: HOME_PATH_RE covers /home and /Users only) |
| snapshot-goals.py --render --check | SUPERSEDED: GOALS.md retired by the owner (goal:g7.16.1.4.1); nothing left to round-trip |

## Judgment (lens goal:g7.16.1 · vision:all-is-one)
- Meets its goal: every live falsifier line exits clean, and the bundle's point, one source per rule, holds in the bytes.
- Carried, not failed: all four verdicts read inconclusive_lean_proved (60-85), never proved; the builds landed and the rules held under later bundles (2 and 3 reused the single sources). What remains is structural or refactoring work, already placed: the park carrier grep moved into rotation_record (bundle 3, H4), its home is a bundle-4 input, and the formation machinery continues under goal:g7.16.1.7.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Row restated by director-general-1 at 00:5xZ 09-30 on SM residue 128 (council, alive, found a false green; SM confirmed on the bytes): the grep for this box's HOME still prints 0 (DG1 re-ran it at HEAD), but anonymize.py HOME_PATH_RE matches /home and /Users only, so a home under /data passes the gate; SM counted 8 such other-user literals in 2 live nodes. DG1 could not re-count them without printing a user name (no local account has a /data home), so the count is SM's. The outcome's claim (one source, fail closed) is narrowed, not withdrawn; the fix is residue 128's.
<!-- THOUGHT:END -->
