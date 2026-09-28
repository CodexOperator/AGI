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
thought_session: belam-stop-line-nopi-20260928
title: "G7.31.1.2.3: tmux_hold build+Popen fallback"
town: core
---
# goal:g7.31.1.2.3

## Why this exists

**Parent `goal:g7.31.1.2`.** MUR DT.102 demote defects 3–4: no build node/payload_ref for hold module (grid gap); no Popen fallback when tmux/session missing — default-on hold can brick restart. Sense 2026-09-28: `extensions/agi/bin/adapters/tmux_hold.py` **absent** on tip — residue still live.

## Target end-state

- Build node (or grid coverage entry) versions the hold module path once it lands.
- Restart falls back to direct Popen when tmux absent or session unset — seat can still restart.

## Invariants

- Env carry and first-spawn founding stay on sibling leaves (`.1` / `.2`).
- Fallback is restart-safety, not a permanent anonymous path (`.2` still owns founding).

## Falsifier

1. `grid_coverage_check` (or build payload_ref) covers the hold module on tip; a no-tmux / no-session probe still restarts via Popen fallback.
2. Negative: default-on hold must not hard-fail restart when tmux/session is missing.

## Out of scope

- `goal:g7.31.1.2.1` / `goal:g7.31.1.2.2`.
- Measured CLI (`goal:g7.31.1.1`).

## Agent Notes

Assigned to **director-belam**. Director-direct under OWNER FULL STOP (NO pi).
