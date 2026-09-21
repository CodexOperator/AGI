---
id: goal:g7.32.4
mint_id: fa84fa8452794bcd81dcf429c24021b6
type: goal
parents:
  - goal:g7.32
next_edges: []
confidence: 0.9
edited_by: belam
goal_id: G7.32.4
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: 3571375dfdc6e142
season: 2
seeds: []
status: active
tags:
  - goal
  - subgoal
  - send-router
thought_session: owner-ask-2026-09-21
title: "G7.32.4: send.py thin router — transport choose, never policy"
town: core
---
# goal:g7.32.4

## Why this exists

**Parent `goal:g7.32`.** Owner vision: **`send.py` thin router** — choose transport (native mesh / signed seat send / nudge bridge), never embed formation, rotation, or harness policy.

g7.31.3 lists `send` among five pane-facing routes; this child owns the **router thinness** contract for that route.

## Target end-state

```
 caller ──▶ send.py ──┬── native seat channel
                      ├── signed DM / board path
                      └── cross-harness nudge bridge
                 (no rotate / no dispatch / no argv build)
```

- One entrypoint; transports are plugins/tables, not if-harness soups.
- Wrap/peek column behavior (legacy g15.22 lineage) stays presentation, not policy.

## Invariants

- send.py imports no rotate/dispatch orchestration.
- Policy refusals (FORGED, ring, written_by) stay in their modules; send only surfaces them.
- Thin = LOC and coupling bounded; growth goes to transport modules.

## Falsifier

1. `send.py` (or its package `__init__`) has zero imports of `rotate` / `dispatch` orchestration symbols.
2. Adding a new transport is a new module + table row, not a new harness `if` in send.py.
3. Cross-harness nudge path from g7.32.2 lands through this router.

## Out of scope

- Magic-pane product UX (g7.32.2).
- Pane method surface (g7.32.3).
- Signature enforcement flips (separate g15 lineage).

## Agent Notes

**Extends:** `goal:g7.31.3` (send as a route). **Used by:** `goal:g7.32.2`. Session: `owner-ask-2026-09-21`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
standing body whole-replace owner-ask-2026-09-21
<!-- THOUGHT:END -->
