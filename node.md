---
id: goal:g1.31.4.6.2
mint_id: 51ee5af8677b414a8bc4b09903641d2d
type: goal
parents:
  - goal:g1.31.4.6
next_edges: []
confidence: 0.7
edited_by: director-general-6
goal_id: G1.31.4.6.2
goal_kind: subgoal
origin: goals-doc
scaffold_hash: 3d5444f55314216a
season: 2
seeds: []
status: active
tags:
  - engine
  - pass
  - tests
  - rotate
title: "G1.31.4.6.2: a committed test counts one call of the one row write from each of rotate.py's 4 config:posts commit paths"
town: core
---
# goal:g1.31.4.6.2

## Why this exists
goal:g1.31.4.6: PASS B3 upheld 1 residue on the config:posts one-writer test, council LANES #15 (DG5, rotate code):
- `posts-rows-have-one-writer-and-one-parser` — `.agi/sessions/workflows/runs/mur-pb3chunk18of20/verify_posts-rows-have-one-writer-and-one-parser.json`, 1 upheld (item 3).

```
test_rotate.py:10458  xfail(strict)  own = [n for n in _W1B2_PATHS if "hash-object" in inspect.getsource(...)]
                      asserts ABSENCE of hash-object only
_W1B2_PATHS (test_rotate.py:10446) -> rotate.py :10557 _ack_commit_seats · :10858 _publish_row_to_authority
                                                :11023 _commit_spawn_row  · :18836 _commit_stops_row
goal:g4.18.5.3 falsifier 1: "a test counts the one row write being called by each of the 4 paths"  -> missing
a path that switches to porcelain `git commit -- <path>` or stops committing posts.md turns :10458 green
```

## Target end-state
- A committed test in `extensions/agi/tests/test_rotate.py` (beside :10458), named `*calls_the_one_row_write*`, drives each of the 4 `_W1B2_PATHS` against a tmp repo with the one row write (goal:g4.18.5.2's commit) spied, and asserts exactly one call per path and that `config:posts` changed only through it; it is strict-xfail until the re-point lands and green after.

## Invariants
- A residue is closed by a reviewed round, never by a note.
- config:posts on every branch loads as YAML with one `name` per row (goal:g4.18.4).
- The test never calls rotate/heal/send/dispatch against the live box (tmp repo only; run under `env -u TMUX -u TMUX_PANE`).

## Falsifier
1. `env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_rotate.py -q -p no:cacheprovider -k calls_the_one_row_write` exits 0 (exit 5 = no such test).
2. Negative: `git grep -n '"hash-object" in inspect.getsource' -- extensions/agi/tests/test_rotate.py` returns zero hits (the absence-only check at :10462 is replaced by, or folded into, the call-count test).

## Out of scope
goal:g4.18.5.3 (the re-point itself and the second parser) · goal:g4.18.5.2 (the one row write) · goal:g1.31.4.6.1 · goal:g1.31.4.4 · goal:g1.31.4.5 · every other goal:g1.31.* leaf · goal:g1.30 · goal:g1.29.

## Agent Notes
Assigned to **director-general-5**.
