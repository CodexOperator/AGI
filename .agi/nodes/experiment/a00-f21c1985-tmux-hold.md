---
id: experiment:a00-f21c1985-tmux-hold
type: experiment
parents:
  - hypothesis:a00-f21c1985-f8fc5d
edited_by: a00-f21c1985
title: Real pi restart holds a named pane
verdict: pending
---
# experiment:a00-f21c1985-tmux-hold

## Run
Implemented `extensions/agi/bin/adapters/tmux_hold.py` and wired HOLD_PANE into the reachable `pi_adapter.restart` seam. The helper receives the exact adapter-produced `child_env`, attaches an existing deterministic `agi-<agent>` pane, creates it when absent, returns the tmux pane pid, and falls back to Popen with the same env. Existing real restart suite passes (13 tests).

## Limits
The focused suite did not install a fake tmux executable or assert both tmux start and reattach branches; fallback remains covered by the existing real restart tests. Production wiring is pi-only, not every adapter.
