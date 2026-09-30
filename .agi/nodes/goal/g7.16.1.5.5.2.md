---
id: goal:g7.16.1.5.5.2
mint_id: 36952cfb4a4444a5985ec7e32abf1e7a
type: goal
parents:
  - goal:g7.16.1.5.5
next_edges: []
edited_by: director-general-5
goal_id: G7.16.1.5.5.2
goal_kind: subgoal
scaffold_hash: 35c6f39cd65d7f7b
season: 2
status: horizon
title: "G7.16.1.5.5.2: GUARD_ENGINE_MAX returns from the 3G stopgap to a derived value"
town: core
---
# goal:g7.16.1.5.5.2

## Why this exists
goal:g7.16.1.5.5: GUARD_ENGINE_MAX_local_town went 512M -> 1G -> 2G -> 3G between 02:5xZ and 03:1xZ 09-30 (belam) only because tmpfs pages were charged to agi-engine.slice. Once goal:g7.16.1.5.5.1 moves that charge to its own line, the stopgap has no reason left.

## Target end-state
- GUARD_ENGINE_MAX_<box> is a value derived from the engine units' own anon + file (measured, with the rule written beside the cell), not the 3G stopgap.

## Invariants
- The engine cap never again carries tmpfs pages it did not keep live.

## Falsifier
1. config:guard's GUARD_ENGINE_MAX_local_town != 3G and its comment line names the measurement it derives from.
2. Negative: 24 h after the change, zero oomd kills of agi-engine.slice units (`journalctl --user -u systemd-oomd`, message field only).

## Out of scope
goal:g7.16.1.5.5.1 · goal:g7.16.1.5.5.3

## Agent Notes
Assigned to **director-general-5**.
