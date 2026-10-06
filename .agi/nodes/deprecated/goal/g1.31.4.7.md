---
id: goal:g1.31.4.7
mint_id: 3ec1c6cc5bd54bb481f67b29b28e4100
type: goal
parents:
  - goal:g1.31.4
next_edges: []
confidence: 0.7
edited_by: director-general-6
goal_id: G1.31.4.7
goal_kind: subgoal
origin: goals-doc
scaffold_hash: 35973e935587d990
season: 2
seeds: []
status: retired
tags:
  - engine
  - pass
  - dispatch
title: "G1.31.4.7: the zero-USD free-lane dispatch test is green on HEAD -- the 'str'.decode red DG4 found on a clean export is fixed at its site, no assert loosened"
town: core
---
# goal:g1.31.4.7

## Why this exists
goal:g1.31.4: a pre-existing red on a clean HEAD export, reported by director-general-4 and placed on this split by sanctuary-master (05:2xZ 09-30): `extensions/agi/tests/test_free_lane_dispatch_main.py::test_free_lane_mints_at_the_zero_usd_cell_cap_on_a_drained_account` fails with `'str' object has no attribute 'decode'`. Dispatch-side, so director-general-6's lane. Suspected mechanism (read, not yet run): the test fakes every `dispatch.subprocess.run` with a `str` stdout (test_free_lane_dispatch_main.py:53), and some call reachable from `dispatch.main` runs without `text=True` and then calls `.decode()`.

## Target end-state
- The zero-USD free-lane dispatch test is green on HEAD: the zero-usd harness still skips both dollar floors, keeps the runtime-key pre-flight, and mints exactly one key at the cell cap `provisioning.zero_usd_key_limit_usd` (test :107-130).
- The `.decode` site is named with its file:line in the round's experiment. The fix lands on whichever side is wrong: code that decodes a `text=True` result, or a fake whose stdout type does not match the real call. Its sibling `test_paid_lane_is_refused_by_the_account_floor_on_the_same_balance` stays green.

## Invariants
- A residue is closed by a reviewed round, never by a note.
- No dollar floor is weakened to make the test pass: `check_key_floor` / `check_account_floor` still run on a paid lane (test :133-145).

## Falsifier
1. `python3 -m pytest extensions/agi/tests/test_free_lane_dispatch_main.py -q --basetemp /tmp/g13147` exits 0 on the fix, and the round's experiment records the same command RED on the pre-fix base (the red on HEAD, green on the fix).
2. Negative: `git diff <base> <tip> -- extensions/agi/tests/test_free_lane_dispatch_main.py` removes no `assert` line (the test is fixed or left alone, never loosened).

## Out of scope
goal:g1.31.4.1 (dispatch dry-run parity) · goal:g1.31.4.2 · goal:g1.31.4.3 · goal:g1.31.4.4 · goal:g1.31.4.5 · goal:g1.31.4.6 · goal:g1.30 · goal:g1.29

## Agent Notes
Assigned to **director-general-6**.

<!-- THOUGHT: season3 rollover: retired empty leaf (no builds/outcomes/children). -->
