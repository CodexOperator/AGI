---
id: goal:g7.16.1.5.5.3
mint_id: dfb8b9a7b5ee49728c2492d40051b79e
type: goal
parents:
  - goal:g7.16.1.5.5
next_edges: []
edited_by: director-general-5
goal_id: G7.16.1.5.5.3
goal_kind: subgoal
scaffold_hash: a1095f26cc0511e3
season: 2
status: horizon
title: "G7.16.1.5.5.3: every memory number has one home in config:guard"
town: core
---
# goal:g7.16.1.5.5.3

## Why this exists
goal:g7.16.1.5.5 target "ONE home": alive measured 02:2xZ 09-30 that the memory budget has two homes that disagree (config:guard vs config:boxkit), and the owner asked for Claude sessions to get "a bit more leeway" (verbatim on goal:g7.16.1.5.5).

## Target end-state
- Every memory number (user OOM %, agi.slice %, oomd pressure %, watchdog %, MemoryHigh, slice ratios, a Claude session's own high/max) is a config:guard cell keyed by box; config:boxkit and every applied unit read those cells.

## Invariants
- A memory number has exactly one writer.

## Falsifier
1. Every memory number in config:guard == the property applied on the box (systemctl show on user@, agi.slice, a post scope).
2. Negative: `git grep -nE 'OOM_PCT|_high_ratio|_max_ratio' -- .agi/config.json` returns 0 numeric values.

## Out of scope
goal:g7.16.1.5.5.1 · goal:g7.16.1.5.5.2 · goal:g6.41.1 (post scopes)

## Agent Notes
Assigned to **director-general-5**.
