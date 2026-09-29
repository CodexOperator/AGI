---
id: experiment:a00-5c2a4bfb-2fec1e
mint_id: a16829256f664cb6905db0c05fba8ce8
type: experiment
parents:
  - hypothesis:a00-5c2a4bfb-2fec1e
next_edges: []
confidence: 0.85
edited_by: sanctuary-helper
evidence_runs:
  - experiment:a00-5c2a4bfb-2fec1e
loop: goal:g7.27.1@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
season: 2
title: delete-dead-rotate-builders-and-pin-absence-with-a-source-grep
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-5c2a4bfb-2fec1e

## Experiment

Falsifier for `goal:g7.27.1`: are the dead per-harness builders really
removable, and does anything still call them?

Baseline measurement before the build (read-only):
`grep -n "_build_claude_command\|_build_copilot_command" extensions/agi/bin/rotate.py`
returned two `def` lines only (896, 1014); a repo-wide grep found no caller
outside tests and one stale docstring.

Build (`extensions/agi/bin/rotate.py`, production):
- deleted `_build_claude_command` (31 lines of dead thin hook)
- deleted `_build_copilot_command` (19 lines of dead thin hook)
- sole seam left is `_build_harness_command` -> `harness_template.render`

Tests (test files, excluded from the production ceiling):
- `test_harness_template.py`: the two frozen-argv tests that called the dead
  builders now call the PRODUCTION `_build_harness_command` with the same
  frozen literals, so the seat shape is still pinned without the dead names.
- Added `test_no_named_harness_builders_in_rotate_source`, which greps
  `rotate.__file__` for the two names — an unused redefinition fails it.
- `test_rotate_copilot_harness.py` docstring updated.

## Measurement

- `grep -n "_build_claude_command\|_build_copilot_command" extensions/agi/bin/rotate.py`
  → empty (exit 1). Falsifier 1 holds.
- `PYTHONPATH=/tmp/pt python3 -m pytest <all test_rotate_*.py, test_harness_*.py,
  test_spawn_gate.py, test_dispatch_dry_run.py>` → **766 passed, 1 xfailed**.
  Includes the rotating/harness suite and the copilot dry-run path.
- `git diff --numstat -- extensions/agi/bin/rotate.py` → `0  31` (production
  lines changed = 31, ceiling 40).
- `dispatch.py` and `harness_template.py` untouched (`0 0`).

Zero `dispatch.py` edits, zero template format changes, no MAIN push.
