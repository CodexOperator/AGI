---
id: experiment:a00-1b1989e4-tmux-hold-fallback-test
mint_id: 86ba7e3f72ba4ff3a22e43eddd11c89f
type: experiment
parents:
  - build:bin-adapters-tmux-hold
next_edges: []
edited_by: a00-39808e48
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

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review: the instruction said to build the fallback and its coverage, and the changed bytes now provide both. The machine actually does route the exact gate state (unset session/pane) and the exact wire failure state (runner raises FileNotFoundError for absent tmux) into the injected direct spawner; my parent probe observed one spawn call with (["seat"], cwd=None, env=None) in each case. The build record is real: .agi/nodes/build/bin-adapters-tmux-hold.md carries payload_ref extensions/agi/bin/adapters/tmux_hold.py, and the source has the named attach/new-session branches plus explicit direct fallback. The near miss is a test-only stub or prose-only coverage, which would not make restart safe; this artifact instead exposes the fallback call on the changed function. No standing rule deviation. probes: gate unset-session passed; wire missing-tmux passed; coverage payload_ref passed. Accepted as proved implementation baseline.
<!-- THOUGHT:END -->

## Agent Notes
Parent review accepted: build payload record verified; direct Popen gate and wire probes passed on changed bytes.
