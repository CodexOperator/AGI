---
id: goal:g7.28
mint_id: 07e7ba7f51034ec681ba3ab4438ac907
type: goal
parents:
  - goal:g7
next_edges: []
confidence: 0.9
edited_by: belam
goal_id: G7.28
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: 67e36e432b34d525
season: 2
seeds: []
status: horizon
tags:
  - goal
  - subgoal
  - dispatch
  - seat
  - persistent
thought_session: belam-horizon-4b-2026-09-21
title: "G7.28: Dispatch persistent mode for occupied seats"
town: core
---
# goal:g7.28

## Why this exists

**Parent `goal:g7` (Sanctuary / seat lineage).** `dispatch.py` today fires and forgets (kid/parent rounds). A **seat** needs the process held, watched, and restarted on death — work `rotate.py` currently re-implements around tmux panes and harness-specific argv. Owner ask 2026-09-19 (voice): give dispatch a **persistent** mode so rotate does not own process lifecycle.

## Target end-state

- `dispatch` gains a **persistent** mode: hold the process, watch it, restart on death (using the harness restart contract / template renderer from `goal:g7.27`).
- Persistent mode **registers the process as an occupied seat** (seat registry / posts row pin stays coherent).
- Rotate does not re-implement watch/restart once this lands.

## Invariants

- Fire-and-forget (kid/parent) behavior remains the default; persistent is opt-in and explicit.
- Restart goes through the same adapter/template seam as first spawn (no second argv path).
- Seat occupation is visible in the graph/config posts row, not only in tmux state.

## Falsifier

1. `dispatch … --persistent` (or equivalent named flag) keeps a seat process alive across a deliberate kill+restart without rotate rebuilding argv.
2. After start, the seat registry / posts row shows the seat occupied with the live pid/session pin.
3. Kid/parent non-persistent spawns are unchanged (regression dry-run).

## Out of scope

- Template authorship (`goal:g7.27`).
- Stripping rotate argv builders (`goal:g7.29`).
- Grok land (`goal:g7.30`).

## Agent Notes

Assigned to **director-helper**. Point director-belam stays on current batch — do not interrupt.
Depends on / pairs with `goal:g7.27` for restart argv source.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
horizon-pass not in-flight unclaimed on board
<!-- THOUGHT:END -->
