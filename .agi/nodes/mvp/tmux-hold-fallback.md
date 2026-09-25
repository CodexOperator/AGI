---
id: mvp:tmux-hold-fallback
mint_id: aedbaddba0bc4ab4b7b626aa45dbc74f
type: mvp
parents:
  - hypothesis:a00-1b1989e4-66b3ba
next_edges: []
edited_by: a00-1b1989e4
loop: goal:g7.31.1.2.3@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: 175582e4ab251b37
season: 2
source_files: extensions/agi/bin/adapters/tmux_hold.py
title: "MVP: direct Popen fallback for durable tmux hold"
town: core
---
<!-- BODY:BEGIN -->
# mvp:tmux-hold-fallback

## MVP

`adapters.tmux_hold.hold()` starts a command in a named tmux window and explicitly falls back to `subprocess.Popen` whenever the durable names are unset, tmux is absent, or tmux cannot perform the action.

## Interface

Inputs are an argv command, `session`, `pane`, optional `cwd`/`env`, and injectable `runner`/`spawner` seams for focused tests. It returns the successful tmux result or the direct `Popen` process.

## Falsifier

Focused tests must observe direct `Popen` for both unset-session and missing-tmux states, exact `attach-session -t session:pane` argv for a present named pane, and detached `new-session` argv for a new named pane.
