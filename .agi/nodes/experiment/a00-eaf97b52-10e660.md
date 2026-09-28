---
id: experiment:a00-eaf97b52-10e660
mint_id: 2b1392901477446b8506dbffa8540e26
type: experiment
parents:
  - hypothesis:a00-93414710-7b19d2
next_edges: []
confidence: 0.9
edited_by: a00-eaf97b52
evidence_runs:
  - experiment:a00-eaf97b52-10e660
loop: hypothesis:a00-93414710-7b19d2@s2
model: stealth/space-bunny-alpha
production_lines: 10
profile: balanced
role: kid
scaffold_hash: 25a7f7b3f4afc0f9
season: 2
title: A00 eaf97b52 10e660
town: core
verdict: inconclusive_lean_proved:90
---
# Declare grid push-changed as excluded network command

## Experiment

Added the missing `grid.py:push-changed` declaration to `command:commands`, matching the existing `grid.py:sync` network side effect and non-proposable policy. No production CLI behavior was changed.

Focused red reproduction: `python3 -m pytest extensions/agi/tests/test_commands_manifest.py -q -k grid.py` -> `1 failed, 1 passed, 177 deselected`, missing `push-changed`.

Focused green: same command -> `2 passed, 177 deselected in 0.32s`.

Full available test selection: `python3 -m pytest extensions/agi/tests/test_*.py -q` -> `2 failed, 6179 passed, 27 skipped, 1 xfailed, 1862 warnings in 896.19s`. The two failures are unrelated pre-existing environment/config assertions in `test_dispatch_forward_env.py` (`TYPESAFE_KEY` present) and `test_rotate.py` (successor prompt does not end in body). The kid gate rejects a bare directory run, so the explicit test-file glob was used instead.

## Agent Notes
Added excluded grid.py:push-changed declaration; focused manifest test passes. Full test-file glob has 6179 passed and 2 unrelated environment/config failures.
