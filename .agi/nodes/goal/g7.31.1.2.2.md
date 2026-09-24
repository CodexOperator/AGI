---
id: goal:g7.31.1.2.2
mint_id: 484c58581bc443ebae27f77a0f9737be
type: goal
parents:
  - goal:g7.31.1.2
next_edges: []
edited_by: director-belam
goal_kind: subgoal
location: source_root
scaffold_hash: 2c12960c256d611a
season: 2
spawn_check: unverified
spawn_check_reason: schema 'goal' is discriminated on 'goal_kind', which this node does not set
status: active
thought_session: belam-or-key-ladder-fix-20260923
title: "G7.31.1.2.2: first-spawn founds named held pane"
town: core
---
# goal:g7.31.1.2.2

## Why this exists

**Parent `goal:g7.31.1.2`.** MUR DT.102 demote defect 2: goal invariant "one named pane per seat / no anonymous fire-and-forget" unmet on **first spawn** — hold only on restart; `dispatch._open_round` still direct `Popen`.

## Target end-state

- First spawn founds the named held pane (tmux_hold.start or equivalent) — not only restart.
- Production path does not stamp `created=true` fabrication on the first restart after anonymous Popen.

## Falsifier

1. First-spawn path under production `_open_round` uses the hold/start seam; probe shows stable pane_id across kill -9 without requiring an explicit out-of-band `tmux_hold.start()` in the experiment.
