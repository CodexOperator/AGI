---
id: goal:g7.16.1.7.2.3
mint_id: 5efe7a7c55dc4019af4bbd62e2bcf6c7
type: goal
parents:
  - goal:g7.16.1.7.2
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G7.16.1.7.2.3
goal_kind: subgoal
origin: council-loop
scaffold_hash: 0a3c21c8d61b269f
season: 2
seeds: []
status: horizon
tags:
  - templates
  - spawn
  - rotate
  - council-loop
title: "G7.16.1.7.2.3: ONE role resolver -- load_role, _resolve_seat_role, resolve_role_spec, resolve_seat_spec and ladder_role_row become calls into the walk; DEFAULT_CC_ROLES retired"
town: core
---
# goal:g7.16.1.7.2.3

## Why this exists
goal:g7.16.1.7.2 (7b, after goal:g7.16.1.6 + goal:g4.18.6): Measured 23:3xZ 09-29 by director-general-5 (council-loop room [measure] line): 6 sources and 5 resolver functions answer one question -- which harness/model/effort/settings a post runs on. The 5 resolvers are rotate.load_role (ladder > config.json > literals), rotate._resolve_seat_role (toml role_source ladder|row), dispatch.resolve_role_spec, dispatch.resolve_seat_spec and adapters.ladder_role_row. The ladder and the post rows drift (prime_director fable-5-1/max in the ladder vs opus-5-5/high on the belam row).

## Target end-state
- Every launch-time (harness, model, effort, settings) comes from the walk (goal:g7.16.1.7.2.1); the five functions are thin callers or gone.
- DEFAULT_CC_ROLES and its 9 literals are gone; an unresolvable role is refused by name, never defaulted to a hardcoded model.

## Invariants
- One answer per post: dispatch, rotate and heal return the same resolution for the same post.

## Falsifier
1. A parity test: for every live config:posts row, rotate, heal and dispatch resolve the same (harness, model, effort, settings).
2. Negative: grep DEFAULT_CC_ROLES in extensions/agi/bin = 0.

## Out of scope
goal:g7.16.1.7.1.1 · goal:g7.16.1.7.1.2

## Agent Notes
Assigned to **director-general-4**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-1 08:4xZ 09-30: re-laned to director-general-4 (one role resolver: 3 of 5 sites are rotate.py (load_role, _resolve_seat_role) and adapters (ladder_role_row); the 2 dispatch.py sites (resolve_role_spec, resolve_seat_spec) are DG3's file, coordinated with DG3) after the owner's stand-down of director-general-5 and director-general-6 (06:1xZ), by sanctuary-master's file-owner map (rotate.py / stand-up / heal / adapters / keys / post rows -> DG4; dispatch.py launch resolvers / RAM writers / render / viewport -> DG3). Status unchanged.
<!-- THOUGHT:END -->
