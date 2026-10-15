---
id: experiment:a00-1b70098e-launder
mint_id: 7bff11ba9bff4b48bda2bd0d95494fa5
type: experiment
parents:
  - hypothesis:a00-1b70098e-011986
next_edges: []
edited_by: a00-1b70098e
loop: goal:g1.31.5.1.3@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: d2669cbd395c3f31
season: 2
title: Run -- hand-edit laundering falsifiers on the built write.py bytes
town: core
---
# experiment:a00-1b70098e-launder

## What was run

The build of goal:g1.31.5.1.3 slice 1 on real bytes, in the real engine
(`extensions/agi/bin/write.py`), plus the falsifiers.

| run | command | result |
|---|---|---|
| R1 falsifier 1 | `python3 -m pytest extensions/agi/tests/test_write_guard.py -q -k 'hand_edit and laundered'` | 1 selected, PASSED (rc 5 before the test existed) |
| R2 falsifier 2 | inside that test's tmp project, after the refused write: `git grep -n HANDEDIT-FIXTURE HEAD -- .agi/nodes` | no output — no commit carries the hand-edit bytes |
| R3 control | same verb on a CLEAN node | exit 0, ONE exact-path commit of that node |
| R4 PRE-FIX | the same test body with `write._pre_dirty` stubbed to `frozenset()` | FAILED on the grep assertion: the hand edit WAS committed at HEAD's behaviour |
| R5 suite | `pytest test_write_guard.py test_write_commit_busy_index.py test_node_writer.py test_write.py test_write_sub.py -q` | 379 passed, 4 xfailed |

## What R4 is worth

R4 is the load-bearing row: it is the only one that shows the defect existed
in the bytes the test runs on, so a pass at R1 is a fix and not a tautology.
`_pre_dirty` is the whole mechanism (sample before the mutation), and stubbing
it to the empty set reproduces the launder exactly.

## Size

`git diff --numstat -- extensions/agi/bin/write.py` → 39 added / 3 removed
(ceiling 40). One test, ~30 lines (ceiling 90). `_commit_message`, the
retry/backoff block and `rotate.py`/`dispatch.py` untouched.
