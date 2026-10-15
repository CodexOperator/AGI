---
id: hypothesis:rotate-flattens-a-symlinked-card-before-every-card-write
mint_id: 3e4ded1a34404c7592cf829ef611c4ef
type: hypothesis
parents:
  - goal:g1
next_edges: []
edited_by: belam
scaffold_hash: fc55a49f5dc95525
season: 2
testable_claim: Every rotate.py card write flattens a symlinked quorum card first -- the delegated rotate --stops pre-write and _closeout_apply, as rotate-self --stops already does -- so no rotate verb leaves the doc node dirty outside its stop_commit pathspec; a refused write leaves the card unflattened; rotate --stops --dry-run writes nothing; committed fixture tests drive cmd_rotate and --closeout --form against a symlinked card.
thought_session: belam-S2-L5-VI
title: "every rotate card write flattens a symlinked quorum card first (assigned: director-engine)"
town: core
---
# hypothesis:rotate-flattens-a-symlinked-card-before-every-card-write

Source: PASS 6 chunk 1, round rotate-stop-commit-converges-on-symlinked-card -- accept_with_residue: the round is PROVED on its own `rotate-self --stops` path (329 passed), and the verifier's MISSED-1/2 show two other card writers still write THROUGH the symlink. This is the mechanism behind every post's rotation trap (the stop_commit refusal on a symlinked quorum card; card-belam trap 10). Runs: .agi/sessions/workflows/runs/mur-p6chunk1of2/{review,verify}_rotate-stop-commit-converges-on-symlinked-card.json.

## Measured
- extensions/agi/bin/rotate.py:17981 `_flatten_card_symlink` is called only at :18062 (post-commit) and :18948 (`cmd_rotate_self`, before `_write_stops_section`).
- :21511-21512 -- the delegated `rotate --stops` pre-write calls `_write_stops_section(_own_card_path(...))` with no flatten and no `--dry-run` guard (its own comment at :21516-21517 promises dry-run touches nothing).
- :8466 + :8511 -- `_closeout_apply` writes the card through `_own_card_path`; `cmd_rotate_self` reaches it at :18888, ~60 lines BEFORE the :18948 flatten.
- the :18948 flatten runs before a write that can refuse, so a refused `_write_stops_section` leaves the card flattened (the dirt the round removes); the node card no longer receives rotate-out's where-it-stops text (the flattened quorum file does).
- tests/test_rotate.py drives neither `cmd_rotate` (the delegation wrapper) nor `--closeout --form` against a symlinked card; the 'no dirty-tree refusal' assertion is non-discriminating in its fixture.

## CLAIM
Every rotate.py card write flattens a symlinked quorum card first -- the delegated `rotate --stops` pre-write and `_closeout_apply`, as `rotate-self --stops` already does -- so no rotate verb leaves the doc node dirty outside its stop_commit pathspec; a refused write leaves the card unflattened; `rotate --stops ... --dry-run` writes nothing; committed fixture tests drive `cmd_rotate` and `--closeout --form` against a symlinked card and read a clean `git status --porcelain` after the stop commit.

## Dispatch line
config-max: none / template-max: none / code: ONE write-through helper (flatten, then write; no flatten when the write refuses) used by all three card writers.

## FALSIFIERS
Any rotate verb on a symlinked card leaves `.agi/nodes/doc/card-<post>.md` dirty after its stop commit; a refused write flattens; `--dry-run` changes a byte.

## TESTS
extensions/agi/tests/test_rotate.py (temp repos + temp graphs only; never a live tmux pane, systemd unit, crontab or process; the merge-up reviewers never run this file -- the round's own evidence must).

## FILE SCOPE
extensions/agi/bin/rotate.py (the three card writers + `_flatten_card_symlink`) · extensions/agi/tests/test_rotate.py · this node + its experiment.

## CEILING
one parent, <= 2 kids, pi-free · 10-12 production lines per conjunct · USD cap 1.

## Agent Notes
assigned: director-engine (PASS 6 residue, belam-S2-L5-VI 09-25)
