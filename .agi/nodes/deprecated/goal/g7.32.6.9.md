---
id: goal:g7.32.6.9
mint_id: 2de2058315ec4dc1b5216481c16cecab
type: goal
parents:
  - goal:g7.32.6
next_edges: []
confidence: 0.85
edited_by: director-helper
goal_id: G7.32.6.9
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: 4357081723872141
season: 2
spawn_gate: bypassed
status: complete
tags:
  - engine
  - messaging
  - nudge
thought_session: helper-nopi-stopline14-20260928
title: "G7.32.6.9: dm_engine nudge/read/sync-tick production composer"
town: core
---
<!-- BODY:BEGIN -->
# goal:g7.32.6.9

## Why this exists

**Parent `goal:g7.32.6`.** Production nudge/read residue: `dm_engine.gate_nudge` + `plan_read` + `plan_sync_tick` compose the sync-only / local / quiet-[red] / read=true-to-sender contracts for engine callers.

## Target end-state

- `dm_engine.gate_nudge` / `plan_read` / `plan_sync_tick` on tip; unit falsifiers GREEN.
- `send.py dm-read-plan` and `dm-sync` exercise the composer on a production CLI path.

## Invariants

- Does **not** open `goal:g7.31.6` / `goal:g7.32.5`.
- Does not type live panes from dm-sync dry-plan.
- NO pi under OWNER FULL STOP.

## Falsifier

1. gate_nudge False without from_sync; quiet blocks unless [red].
2. plan_read destination = sender remote_head; read=True.
3. plan_sync_tick emits only gated unread locals.

## Out of scope

- Live pane typing from sync; write.py push (g4.18.1).
- Parked g7.32.5 / g7.31.6.

## Agent Notes

Assigned to **director-helper** under OWNER FULL STOP (NO pi).

NO-PI stopline14: gate_nudge + plan_read + plan_sync_tick on tip; dm-read-plan/dm-sync CLI exercise composer; no live pane type from dry-plan

<!-- THOUGHT: season3 rollover: complete goal not carried into s3; builds reparented to umbrella. -->
