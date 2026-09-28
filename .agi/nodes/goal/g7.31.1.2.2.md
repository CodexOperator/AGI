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
thought_session: belam-stop-line-nopi-20260928
title: "G7.31.1.2.2: first-spawn founds named held pane"
town: core
---
# goal:g7.31.1.2.2

## Why this exists

**Parent `goal:g7.31.1.2`.** MUR DT.102 demote defect 2: invariant "one named pane per seat / no anonymous fire-and-forget" unmet on **first spawn** — hold only on restart; `dispatch._open_round` still direct `Popen`.

## Target end-state

- First spawn founds the named held pane (`tmux_hold.start` or equivalent) — not only restart.
- Production path does not stamp `created=true` fabrication on the first restart after anonymous Popen.

## Invariants

- Env-on-hold-restart is OOS (`goal:g7.31.1.2.1`).
- Build coverage / Popen fallback is OOS (`goal:g7.31.1.2.3`).
- One named pane per seat; no parallel anonymous Popen then "upgrade".

## Falsifier

1. First-spawn under production `_open_round` uses the hold/start seam; probe shows stable pane_id across kill -9 without out-of-band `tmux_hold.start()`.
2. Negative: zero production first-spawn paths that only `subprocess.Popen` with no hold/start.

## Out of scope

- `goal:g7.31.1.2.1` child_env on held restart.
- `goal:g7.31.1.2.3` grid coverage + no-tmux fallback.
- Persistent dispatch mode umbrella (`goal:g7.28`, helper seat).

## Agent Notes

Assigned to **director-belam**. Director-direct under OWNER FULL STOP (NO pi).
