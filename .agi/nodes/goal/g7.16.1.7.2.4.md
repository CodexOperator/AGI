---
id: goal:g7.16.1.7.2.4
mint_id: 1333d33886874f31b0a7b7ddf7b859a9
type: goal
parents:
  - goal:g7.16.1.7.2
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G7.16.1.7.2.4
goal_kind: subgoal
origin: council-loop
scaffold_hash: f774d01fcfa822cf
season: 2
seeds: []
status: horizon
tags:
  - templates
  - spawn
  - rotate
  - council-loop
title: "G7.16.1.7.2.4: ONE post row holds the live role -- session id, pid, pane id, plus mint-id links (never copies) to its renderer and harness config"
town: core
---
# goal:g7.16.1.7.2.4

## Why this exists
goal:g7.16.1.7: the owner, verbatim there: "Ideally the post holds everything for that role: session id, pid, tmux pane id, renderer nested inside it but actually a mint id link: harness config (includes model type)." Measured 23:3xZ 09-29 by director-general-5 (council-loop room [measure] line): 6 sources and 5 resolver functions answer one question -- which harness/model/effort/settings a post runs on. config:posts carries 27 rows x 5 copied cells (harness, model, effort, settings, session_kind) = 135 cells, only 9 distinct combos.

## Target end-state
- A config:posts row holds live cells (session_id, pid, pane, generation, keys) plus link cells (mint ids) to its post template, harness template row and renderer; the 5 copied cells are gone.
- The row shape is posted in room directors before any writer depends on it.

## Invariants
- Every live row resolves through the walk to a full (harness, model, effort, settings); links resolve (links.py broken = 0).

## Falsifier
1. The walk resolves every live config:posts row, every live row carries a pane cell (config:posts holds only a window today), and links.py links reports 0 broken.
2. Negative: zero config:posts rows carry a model or effort cell.

## Out of scope
goal:g7.16.1.7.2.5 · goal:g7.16.1.7.1.4 · rotate.py commit sites (W1c, room directors)

## Agent Notes
Assigned to **director-general-5**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-1 08:4xZ 09-30, routed by sanctuary-master from self-perpetuating's council coverage review of goal:g7.16.1.7: the target already names a pane cell, but no falsifier checked it and config:posts holds only a window today; Falsifier 1 now requires a pane cell on every live row.
<!-- THOUGHT:END -->
