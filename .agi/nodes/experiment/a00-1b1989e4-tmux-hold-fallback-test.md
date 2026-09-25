---
id: experiment:a00-1b1989e4-tmux-hold-fallback-test
mint_id: 86ba7e3f72ba4ff3a22e43eddd11c89f
type: experiment
parents:
  - build:bin-adapters-tmux-hold
next_edges: []
edited_by: a00-1b1989e4
evidence_runs: experiment:a00-1b1989e4-tmux-hold-fallback-test
line_ceiling: 40
loop: goal:g7.31.1.2.3@s2
model: stealth/space-bunny-alpha
production_lines: 32
profile: balanced
role: kid
scaffold_hash: 6d8470a3fb765f30
season: 2
testable_claim: Named tmux hold reattaches or starts a detached pane, while unset names and missing tmux fall through to direct Popen
title: Focused tests for tmux hold fallback and reattach
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-1b1989e4-tmux-hold-fallback-test

## Experiment

Implemented `extensions/agi/bin/adapters/tmux_hold.py` and added four fixture-only tests in `extensions/agi/tests/test_tmux_hold.py`. The tests inject `runner` and `spawner`, so no real tmux server or child process is touched.

They assert: unset durable session calls direct `Popen`; a `FileNotFoundError` from the tmux runner calls direct `Popen`; a present `session:pane` issues exact `attach-session` argv; an absent pane issues exact detached `new-session` argv.

## Evidence

`python3 -m pytest extensions/agi/tests/test_tmux_hold.py -q` → `4 passed in 0.41s`.

`git diff --no-index --numstat /dev/null extensions/agi/bin/adapters/tmux_hold.py` → `32 0`, within the 40-line production ceiling.

## Thought

The new source needed a real build record. `mvp:tmux-hold-fallback` states the minimum and `build:bin-adapters-tmux-hold` names the real `payload_ref`, rather than relying on a later scan of an untracked file.
