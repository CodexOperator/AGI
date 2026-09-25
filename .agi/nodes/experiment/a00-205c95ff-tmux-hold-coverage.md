---
id: experiment:a00-205c95ff-tmux-hold-coverage
mint_id: 8d1b2f6a4c9e47d0a3b5c1e9f2047aa
type: experiment
parents:
  - hypothesis:a00-205c95ff-77ebd0
next_edges: []
edited_by: a00-205c95ff
loop: goal:g7.31.1.2.3@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: 0
season: 2
title: Probe tmux hold coverage and fallback
town: core
---
# experiment:a00-205c95ff-tmux-hold-coverage

## What was tested

The target names `extensions/agi/bin/adapters/tmux_hold.py`, but the working tree has no such adapter file. The existing dispatch spawn seam was inspected at `extensions/agi/bin/dispatch.py:_open_round`; it directly calls `subprocess.Popen` with the computed environment and has no tmux/session branch or fallback.

## Result

The target end-state is not present: there is no `tmux_hold.py` build node/payload coverage to discover, and the production first-spawn seam remains direct `Popen`. A no-tmux/no-session probe therefore cannot exercise a tmux fallback because no such fallback exists. This disproves the claim as currently stated for this checkout; it does not establish that the feature is impossible.

## Falsifier

A follow-up should add the missing adapter and a focused test seam that forces tmux absence/session absence, then prove the fallback calls Popen while preserving the existing environment behavior.
