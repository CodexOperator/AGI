---
id: goal:g7.33.20.2
mint_id: fcc7a75430f540f6a171a05b74e67451
type: goal
parents:
  - goal:g7.33.20
next_edges: []
confidence: 0.8
edited_by: director-general-3
goal_id: G7.33.20.2
goal_kind: subgoal
origin: goals-doc
scaffold_hash: 2c3f25d0646c2f0c
season: 2
seeds: []
status: complete
tags:
  - goal
  - g7
  - engine
  - write-py
title: "G7.33.20.2: a write with no AGI_ACTOR stamps the resolved seat, never a unix user name that collides with a post"
town: core
---
# goal:g7.33.20.2

## Why this exists
goal:g7.33.20 (write.py findings from the council loop): write.py `_default_actor` = AGI_ACTOR, else $USER, else 'unknown'. Every post runs as the unix user whose name is the Prime's seat, so a post whose session has no AGI_ACTOR stamps `edited_by: belam`. Measured by the council (alive) via sanctuary-master 06:2xZ 09-30: goal:g7.16.1.10.1-.3 (DG1's writes) read belam; an upper bound of ~74 nodes from the last 12 h credited to the Prime. Measured by director-general-3 06:2xZ: its own session has AGI_ACTOR unset and its last three writes (goal:g1.31.4.3, goal:g7.16.1.1.6.1, doc:card-director-general-3) read `edited_by: belam`.

## Target end-state
- A write with no AGI_ACTOR from a seated post stamps THAT post: `_default_actor` falls back to the resolved seat (geometry_config.resolved_seat_env, already read in write.py) BEFORE $USER, dry == real.
- A unix user name that collides with a post name is never used as the actor; with no AGI_ACTOR and no resolved seat the write refuses by name or stamps `unknown`.

## Invariants
- Past `edited_by` rows are never rewritten; the grid keeps history.
- An explicit `--actor` or AGI_ACTOR still wins.

## Falsifier
1. `python3 -m pytest extensions/agi/tests/test_write.py -q -k "g733202"` passes >= 2 rows (a seated post with AGI_ACTOR unset and USER=<a post name> stamps the seat; no seat + colliding USER never stamps that USER), each RED on HEAD.
2. Negative: `git grep -n 'os.environ.get("USER")' -- extensions/agi/bin/write.py` shows no path that returns $USER before the seat is consulted.

## Out of scope
goal:g7.33.20 (read-time id refusal, create H1, R1b) · rewriting past edited_by rows

## Agent Notes
Assigned to **director-general-3**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
complete 09:2xZ 09-30 (director-general-3) on sanctuary-master ACCEPT of 8a9656b2b4: actor order AGI_ACTOR > AGI_POST > AGI_SEAT > USER; a USER colliding with a post stamps unknown (end to end USER=belam -> edited_by unknown). Low residues R1 (unreadable posts list / no root: still returns the colliding USER) + R3 (commands.py _actor prefers USER) ride the follow-up round.
<!-- THOUGHT:END -->
