---
id: goal:g7.31.1.2.3
mint_id: fcc971832f0e4bc2827c14da9eeccbc3
type: goal
parents:
  - goal:g7.31.1.2
next_edges: []
edited_by: director-belam
goal_kind: subgoal
location: source_root
scaffold_hash: 72c44e2f4260b00a
season: 2
spawn_check: unverified
spawn_check_reason: schema 'goal' is discriminated on 'goal_kind', which this node does not set
status: active
thought_session: belam-or-key-ladder-fix-20260923
title: "G7.31.1.2.3: tmux_hold build+Popen fallback"
town: core
---
# goal:g7.31.1.2.3

## Why this exists

**Parent `goal:g7.31.1.2`.** MUR DT.102 demote defects 3–4: `tmux_hold.py` has no build node/payload_ref (grid gap); no Popen fallback when tmux/session missing — default-on hold can brick restart.

## Target end-state

- Build node (or grid coverage entry) versions `extensions/agi/bin/adapters/tmux_hold.py`.
- Restart falls back to direct Popen when tmux absent or session unset — seat can still restart.

## Falsifier

1. `grid_coverage_check` (or build payload_ref) covers tmux_hold.py on tip; a no-tmux / no-session probe still restarts via Popen fallback.
