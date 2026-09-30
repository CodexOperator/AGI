---
id: goal:g7.16.1.7.1.3.3
mint_id: 4db9eb254c4c4a84b26db96f76697cfa
type: goal
parents:
  - goal:g7.16.1.7.1.3
next_edges: []
edited_by: director-general-5
goal_id: G7.16.1.7.1.3.3
goal_kind: subgoal
scaffold_hash: 9b36caae057efcdc
season: 2
status: horizon
title: "G7.16.1.7.1.3.3: the pi-free / pi-local aliases retire"
town: core
---
# goal:g7.16.1.7.1.3.3

## Why this exists
goal:g7.16.1.7.1.3: its end-state says the old ids resolve as aliases "for one season" and then retire; goal:g7.16.1.7.1.3.2 introduces the aliases.

## Target end-state
- No harness id pi-free / pi-local is written anywhere (config, briefs, skills, role docs); the template's `aliases` cell is empty and then removed.

## Invariants
- Retiring an alias never changes which row a live route resolves.

## Falsifier
1. grep -rn 'pi-free\|pi-local' extensions/ skills/ .agi/config.json .agi/nodes/.geometry = 0 outside retired nodes and git history.
2. Negative: adapters.harness_block(cfg, "pi-free") raises the unknown-harness error by name.

## Out of scope
goal:g7.16.1.7.1.3.1 · goal:g7.16.1.7.1.3.2

## Agent Notes
Assigned to **director-general-5**.
