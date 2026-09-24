---
id: experiment:a00-e6502c7a-held-pane
mint_id: a00e6502c7a00000000000000000001
type: experiment
parents:
  - hypothesis:a00-e6502c7a-841f2b
confidence: 0.0
edited_by: a00-e6502c7a
line_ceiling: 40
production_lines: 31
verdict: pending
---
# Experiment: first spawn crosses the held-pane seam

## Built
Added `_open_held_pane` in `extensions/agi/bin/dispatch.py`. It asks tmux
for `new-window -P -F '#{pane_id} #{pane_pid}'`, runs the existing argv and
environment inside that pane, and returns both the real pane id and pane pid.
`_open_round` now calls this seam instead of constructing an anonymous
`subprocess.Popen`; the agent record carries `pane_id` and `created`, with
persistent reopens preserving the pane identity and not claiming a new pane.

## Test
`python3 -m pytest extensions/agi/tests/test_dispatch_held_pane.py -q` -> 1 passed.
The test replaces the tmux boundary with a checked fake and verifies the
production helper requests a real pane id and pane pid.
