---
id: experiment:a00-b16107bb-private-env
mint_id: a00b16107bbprivateenv
type: experiment
parents:
  - hypothesis:a00-b16107bb-0e3606
next_edges: []
loop: goal:g7.31.1.2.1@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
season: 2
title: Private tmux server env handoff tests
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-b16107bb-private-env

## Run

Implemented the hypothesis in `extensions/agi/bin/adapters/tmux_hold.py`, declared hold-pane opt-in in `.agi/config.json`, and added `extensions/agi/tests/test_tmux_hold.py`. The fake tmux captures server environment and argv across initial create, live reattach, and dead-pane respawn; a fifth test drives `pi_adapter.restart` and checks fallback/config defaults.

Command: `python3 -m pytest extensions/agi/tests/test_tmux_hold.py -q`

Result: **5 passed**. Production diff measured 26 added lines against a 40-line ceiling.
