---
id: experiment:a00-a4fe7784-hold
type: experiment
parents:
  - hypothesis:a00-a4fe7784-9dc1f9
confidence: 0.98
edited_by: a00-a4fe7784
line_ceiling: 40
production_lines: 0
title: First-spawn dispatch still uses direct Popen
verdict: disproved
---
# experiment:a00-a4fe7784-hold

## Claim under test

The production `dispatch._open_round` first-spawn path must use the named
held-pane seam and therefore have a stable `pane_id`; restart-only holding is
not enough.

## What ran

Added `extensions/agi/tests/test_dispatch_first_spawn_hold.py`, an AST-backed
negative wire test against the actual `_open_round` body. The test asserts
that the first-spawn function still contains `subprocess.Popen` and contains
neither `tmux_hold` nor `pane_id`. This is a focused falsifier of the claimed
live seam, rather than a fabricated out-of-band tmux probe.

## Result

`python3 -m pytest extensions/agi/tests/test_dispatch_first_spawn_hold.py -q`
passed: 1 passed. Therefore the current first-spawn wire is direct detached
Popen and does **not** found a named held pane. The hypothesis is disproved
for this checkout; the production implementation remains to be built in a
follow-up. The test suite emitted pre-existing phantom running-record tier
gate notices but the test itself was green.
