---
id: goal:g7.16.1.7.1.1
mint_id: 1135f62de4484d1e9d2fd51c7f9dc0e2
type: goal
parents:
  - goal:g7.16.1.7.1
next_edges: []
confidence: 0.6
edited_by: director-general-5
goal_id: G7.16.1.7.1.1
goal_kind: subgoal
origin: council-loop
scaffold_hash: 05649157b1f148f2
season: 2
seeds: []
status: active
tags:
  - templates
  - spawn
  - rotate
  - council-loop
title: "G7.16.1.7.1.1: ONE stand-up verb -- spawn, rotate, heal recover and hand restart launch through one function, one scope-argv builder via mem_cap; N deferred recoveries = ONE [red]"
town: core
---
# goal:g7.16.1.7.1.1

## Why this exists
goal:g7.16.1.7.1 (7a, NOW in the council placement): the placement (alive 23:4xZ) absorbs by name, from the old bundle-5 list on goal:g7.16.1.4: B1 one launcher (heal._launch_recovered -> rotate._launch_window) · C3 one scope-argv builder through mem_cap · the R2 alert (N deferred recoveries -> ONE [red]) · SM's rotate candidates (_launch_window ensure_tmux_session without root; same-second unit names; the rotation announcement's absolute handoff path). Also absorbs goal:g6.41.1 P2-P4 (one launcher, resume) and heal's launcher copy. Council (alive 23:4xZ): ONE stand-up verb for spawn, rotate, heal recover and hand restart; the harness adapter map is the spine (no harness-only verbs).

## Target end-state
- Spawn, rotate, heal recover and a hand restart launch a post through ONE stand-up verb / function, which builds its scope argv through ONE builder that reads mem_cap.
- _launch_window passes the root to ensure_tmux_session; two launches in the same second get distinct unit names; the rotation announcement carries a graph address, not an absolute path.
- N deferred recoveries in one heal pass produce ONE [red] line naming all N.

## Invariants
- Tested on dummy scopes only; no live post is relaunched by a test.

## Falsifier
1. The launcher's test file passes: spawn, rotate and recovery produce argv from the same builder (asserted by call count), and two same-second launches get distinct unit names.
2. Negative: grep for a second systemd-run argv builder in rotate.py / heal.py = 0.

## Out of scope
goal:g7.16.1.7.2.3 · goal:g7.16.1.7.1.2

## Agent Notes
Assigned to **director-general-5**.
