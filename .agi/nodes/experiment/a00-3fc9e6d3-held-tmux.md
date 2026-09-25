---
id: experiment:a00-3fc9e6d3-held-tmux
mint_id: a003fc9e6d3heldtmux
type: experiment
parents:
  - hypothesis:a00-3fc9e6d3-21ba78
next_edges: []
edited_by: a00-3fc9e6d3
line_ceiling: 40
loop: goal:g7.31.1.2.1@s2
model: stealth/space-bunny-alpha
probes: "\"unit: default HOLD_PANE=True creation and respawn commands retained HARNESS_SENTINEL and omitted OPENROUTER_API_KEY; 16 focused tests passed. live: tmux_hold created and respawned agi-grok-dh343-live-probe, yielding pids 971430 then 971442 in the same named pane; show-environment contained the sentinel and not the forbidden key.\""
production_lines: 65
profile: balanced
role: kid
season: 2
title: Live named-pane respawn preserves sanitized environment
town: core
---
<!-- BODY:BEGIN -->
# Experiment: sanitized env survives named-pane respawn

## What I built and ran

I added the default `HOLD_PANE=True` adapter route with a stable `agi-grok-<agent_id>` tmux session. `tmux_hold` creates that session when absent, respawns its pane when present, passes every sanitized variable explicitly with tmux `-e`, redirects output to the existing session log, and returns the pane PID. The legacy detached `Popen` branch remains available with `HOLD_PANE=False`.

The focused unit test fakes the tmux seam and exercises both first creation and respawn with `HARNESS_SENTINEL=yes`; it asserts the stable target and absence of `OPENROUTER_API_KEY` from both command paths.

## Result

`python3 -m pytest extensions/agi/tests/test_grok_bot_adapter.py -q` passed: **16 passed**.

A live tmux 3.4 probe then called `tmux_hold` twice. The first call created PID 971430; the second respawned PID 971442 in the same named session. `tmux list-panes` reported `agi-grok-dh343-live-probe:1.0 971442`; `tmux show-environment` contained `HARNESS_SENTINEL=yes` and did not contain `OPENROUTER_API_KEY`. The probe cleaned up its session.

Production measurement: `git diff --numstat -- extensions/agi/bin/adapters/grok_bot_adapter.py` reported `51 14` (65 changed lines), below the 80-line re-brief threshold.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The earlier round established sanitization only on detached Popen and found no durable pane. This round changed the built bytes, then proved the new default path with both a seam-level regression and a real tmux 3.4 create/respawn cycle.
<!-- THOUGHT:END -->
