---
id: goal:g6.4
mint_id: 7ecc46c896654d5090cdad602cbf45de
type: goal
parents:
  - goal:g6
confidence: 1.0
edited_by: season.py
goal_id: G6.4
goal_kind: subgoal
heading_level: 3
origin: goals-doc
season: 1
seeds: []
status: horizon
tags:
  - goal
  - subgoal
thought_session: season
title: "G6.4: Non-build work branches off a build version and returns a new one"
---
The full cycle, once G6.3 holds: a non-build chain — idea → hypothesis →
experiment → verdict — **branches off a specific version of a build node**, and
its accepted verdict produces the **next version** of that build node.

That makes provenance answerable in the direction that matters: not "what
changed in this file" but *"which argument produced this line, and what was the
state of the code when that argument was made"*. It also makes a rejected
verdict cheap — the branch simply never lands a new build version, and the
attempt survives as prior art (G9.5's rejected-draft case).

Depends on G6.3 for versioning and on G9.5 for the session→version link, without
which a branch point cannot be identified after the fact.