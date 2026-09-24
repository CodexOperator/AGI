---
id: experiment:a00-252f53a2-hold-env
type: experiment
parents:
  - hypothesis:a00-252f53a2-fda425
loop: goal:g7.31.1.2.1@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
season: 2
status: active
title: Probe held restart environment seam
---
# experiment:a00-252f53a2-hold-env

## What was run

- Searched all production Python for `HOLD_PANE`, `tmux_hold`, and equivalent held-pane symbols.
- Read `extensions/agi/bin/adapters/pi_adapter.py` and `extensions/agi/bin/dispatch.py` around the ordinary restart and spawn environment paths.
- Ran the targeted credential environment tests.

## Observation

No `HOLD_PANE` or `tmux_hold` symbol exists in this checkout. The ordinary `pi_adapter.restart` computes `child_env(harness=harness, base=dict(os.environ))` before `Popen`, and the live dispatch computes `spawn_env` before its normal spawn. The target's stated early-return defect is therefore not present in the available bytes.

The parent goal's target seam may live in another revision or was removed before this checkout; this experiment cannot validate a change to code that is absent.
