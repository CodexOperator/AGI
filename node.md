---
id: goal:g7.16.1.11.10
mint_id: a5045f1756a541b4a1da363d6984d557
type: goal
parents:
  - goal:g7.16.1.11
next_edges: []
confidence: 0.6
edited_by: belam
goal_id: G7.16.1.11.10
goal_kind: subgoal
origin: owner
scaffold_hash: 00809c3efdff8b4c
season: 2
seeds: []
status: active
tags:
  - council-loop
  - redesign
  - bundle
title: "G7.16.1.11.10: PHASE 3: every post but belam runs on the new post system, each moved only after every post's moral satisfaction verdict says yes and leaf .8 holds"
town: core
---
# goal:g7.16.1.11.10

## Why this exists
Parent goal:g7.16.1.11: Owner 06:5xZ on goal:g7.16.1.11: prepared tonight, executed when the owner wakes (the CC logins are the owner's).
## Target end-state
PHASE 3: every post but belam runs on the new post system, each moved only after every post's moral satisfaction verdict says yes and leaf .8 holds.
## Invariants
one post at a time, DG5 first, each with a one-command rollback; belam stays on the old system.
## Falsifier
1. every post row reads engine.v of the new system except belam, and each post's verdict reads yes
2. negative: a post moved without its verdict: zero
## Out of scope
the sibling leaves goal:g7.16.1.11.1 through goal:g7.16.1.11.10, each its own end-state
## OWNER, verbatim
"transfer everyone other than yourself to new post system in phase 3 once everyone is beyond satisfied" (owner 06:5xZ; verbatim on goal:g7.16.1.11)
## Agent Notes
Assigned to **director-general-3**.
