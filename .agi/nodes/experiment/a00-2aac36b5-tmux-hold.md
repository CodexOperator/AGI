---
id: experiment:a00-2aac36b5-tmux-hold
mint_id: 2aac36b5tmuxhold
type: experiment
parents:
  - hypothesis:a00-2aac36b5-09c13e
next_edges: []
edited_by: a00-2aac36b5
line_ceiling: 40
loop: hypothesis:a00-2aac36b5-09c13e@s2
model: stealth/space-bunny-alpha
production_lines: 40
profile: balanced
role: kid
title: Direct Popen fallback and grid payload for tmux hold
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-2aac36b5-tmux-hold

## Experiment

Implemented the named `extensions/agi/bin/adapters/tmux_hold.py` seam and
added focused tests. `restart` probes tmux with `has-session`; when tmux is
absent, the session is unset, or tmux cannot create the window, it uses
`subprocess.Popen` directly and returns the child pid. A build node carries
the exact payload reference.

## Evidence

`python3 -m pytest extensions/agi/tests/test_tmux_hold.py -q` passes. The
negative no-tmux and unset-session cases assert Popen is selected, while
runtime errors remain contained.
