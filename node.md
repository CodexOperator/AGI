---
id: goal:g7.32.6.4
mint_id: 9aa347111f744e03ae5e27b79064ddae
type: goal
parents:
  - goal:g7.32.6
next_edges: []
confidence: 0.85
edited_by: director-helper
goal_id: G7.32.6.4
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: 9ce7feca9dbf2b0b
season: 2
spawn_gate: bypassed
status: complete
tags:
  - goal
  - subgoal
  - engine
  - messaging
thought_session: helper-nopi-stopline13-20260928
title: "G7.32.6.4: Nudge fires only from sync on unread local-post dms"
town: core
---
<!-- BODY:BEGIN -->
# goal:g7.32.6.4

## Why this exists

**Parent `goal:g7.32.6`.** Owner design line for the post-branch send redesign: nudge = the box sync; fires only from sync, on unread dm for a post local to this box (`AGI_BOX`). Quiet blocks unless `[red]`.

## Target end-state

- Contract library on tip encodes the owner residue for this leaf.
- Falsifiers GREEN independently; production send.py/crons wiring is director-engine follow-on.

## Invariants

- Sibling slices under `goal:g7.32.6` own their own falsifiers — do not widen this leaf.
- Does **not** open `goal:g7.31.6` / `goal:g7.32.5` (board parked).
- NO pi under OWNER FULL STOP.

## Falsifier

1. `from_sync=False` never nudges.
2. foreign box / already-read refuse.
3. quiet blocks; `[red]` overrides quiet.

## Out of scope

- Other `goal:g7.32.6.*` siblings.
- Parked `goal:g7.32.5` / `goal:g7.31.6`.

## Agent Notes

Assigned to **director-helper** under OWNER FULL STOP (NO pi). Contract-first; engine wires production later.

NO-PI stopline13: dm_nudge_gate.py + test_dm_nudge_gate 4/4; sync-only local unread; quiet/[red].

<!-- THOUGHT: season3 rollover: complete goal not carried into s3; builds reparented to umbrella. -->
