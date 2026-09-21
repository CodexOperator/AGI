---
id: goal:g7.34.1
mint_id: c1859c56a05d42bb93aa3c681ed2aced
type: goal
parents:
  - goal:g7.34
next_edges: []
confidence: 0.9
edited_by: belam
goal_id: G7.34.1
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: e78060098071b9a3
season: 2
seeds: []
status: horizon
tags:
  - goal
  - subgoal
  - trajectory
  - schema
  - parked
thought_session: belam-geom-traj-spine-2026-09-21
title: "G7.34.1: B1 [trajectory] schema + allowed parents/links"
town: core
---
<!-- BODY:BEGIN -->
# goal:g7.34.1

## Why
No [trajectory] schema yet; town bodies hold TEMP stand-ins. Need typed node with allowed parents/links so KG coordination is first-class.

## Target
`.agi/context/schemas/[trajectory].md` exists; spawn/parents/links rules documented; write.py create trajectory:* accepted; links.py resolves trajectory links.

## Invariants
- Schema declares allowed parents/links explicitly.
- Does not steal town ops fields (location/council/master).
- Parents-on-children remain goal nesting SoT.

## Falsifier
1. `test -f .agi/context/schemas/[trajectory].md` fails → not done.
2. write.py create trajectory:… refused without documented reason → not done.
3. links.py broken count >0 on a sample trajectory node → not done.

## Out of Scope
- Minting trajectory:core / :local-maxxing (g7.34.2).
- Geometry Pass-1 (g7.34.3+).
- Engine G7.33.5 duplicate work if already covered — prefer this spine id.

## Agent Notes
Parked **town:core**. Parent **goal:g7.34**. B1 only.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Belam 2026-09-21: mint parked unassigned on town:core; geometry/trajectory spine; no director assign; no impl yet
<!-- THOUGHT:END -->
