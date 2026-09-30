---
id: goal:g7.16.1.5.5
mint_id: b1534257b7fc451ca397e9e2769120e7
type: goal
parents:
  - goal:g7.16.1.5
next_edges: []
confidence: 0.8
edited_by: alive
goal_id: G7.16.1.5.5
goal_kind: subgoal
origin: goals-doc
scaffold_hash: 2e46b4ca6b4f1b51
season: 2
seeds: []
status: horizon
tags:
  - memory
  - config-guard
  - council-loop
title: "G7.16.1.5.5: the memory budget has ONE home -- config:guard holds every memory number, boxkit and the applied units read it, the tmpfs caps count inside it"
town: core
---
# goal:g7.16.1.5.5

## OWNER 2026-09-29 22:2xZ, verbatim (Prime pane; also on goal:g7.16.1.5)
"Also maybe raise the OOM kill limit from 50% to around 85%. And allow Claude sessions a bit more leeway to hog some memory individually if needed."

## Why this exists
goal:g7.16.1.5 target B (the memory budget has ONE home): the council's placement check of .5's leaves (alive, 02:2xZ 09-30) found B with no leaf; belam asked the council writer to mint it, unassigned. Measured 02:2xZ 09-30 by alive: the budget has TWO homes that disagree -- config:guard carries GUARD_OOMD_LIMIT (the owner's 85, option b, set 22:4xZ 09-29) and GUARD_USER_HIGH_PCT, while config:boxkit carries its own USER_OOM_PCT 50, user_high_ratio 0.9, AGI_OOM_PCT 40, OOMD_PRESSURE_PCT 60 and the agi/work slice ratios. A third disagreement, measured 02:5xZ: config:guard GUARD_ENGINE_MAX_local_town = 1G (belam, after heal's reaper was oomd-killed twice at the old 384M high) while config:boxkit still carries ENGINE_HIGH 384M / ENGINE_MAX 512M. The RAM disk is charged to the WRONG line (belam, measured 03:06Z 09-30): tmpfs pages are charged to their first writer and reparented to the slice when a unit exits, so engine units (heal, alarms, sanctuary-watch) writing into MAIN-on-tmpfs pile shmem onto agi-engine.slice (792M = shmem 700 · file 702 · anon 78 MiB; the RAM disk 1095M at 02:31Z -> 1520M at 03:06Z; box Shmem 1,036 MiB); no reclaim frees shmem (swap only), so the slice throttles and oomd killed sanctuary-watch x3 + the reaper x1 after 02:58; stopgap GUARD_ENGINE_MAX 512M -> 1G -> 2G.

## Target end-state
- ONE home: config:guard, keyed by box class, holds every memory number -- user OOM %, agi.slice %, oomd pressure %, watchdog %, MemoryHigh, the slice ratios and a Claude session's own high/max (raised for the owner's "leeway", never unbounded).
- config:boxkit and every applied unit READ those cells; boxkit carries no memory number of its own.
- The tmpfs caps (goal:g7.16.1.5.1, goal:g7.16.1.5.4) count INSIDE the budget as the RAM disk's OWN line (its size cell in config:guard), never charged to whichever slice first wrote a page: engine units writing into MAIN-on-tmpfs leave agi-engine.slice carrying their own anon + file only, and GUARD_ENGINE_MAX returns from the 2G stopgap to a value derived from that; a launch holds on memory_alarm WARN/ALARM like every other launch.

## Invariants
- A memory number has exactly one writer; a second home is a FAIL, never a default.
- The kill line and P6 (config post_scope.live) are one judgement: the owner's 85 % stands with every post in its own scope.

## Falsifier
1. Every memory number in config:guard == the property applied on the box (systemctl show on the user slice, agi.slice, a post scope).
2. While the RAM disk fills, agi-engine.slice shmem stays near 0 (memory.stat) and no engine unit is oomd-killed for pages it only wrote to tmpfs; GUARD_ENGINE_MAX reads its derived value, not the stopgap.
3. Negative: `git grep -nE 'OOM_PCT|_high_ratio|_max_ratio' -- .agi/config.json` returns 0 numeric values outside a read of config:guard.

## Out of scope
goal:g7.16.1.5.1 · goal:g7.16.1.5.4 (the tmpfs mounts) · goal:g6.41.1 (P6, post scopes) · worktree cleanup (the owner's first priority).

## Agent Notes
UNASSIGNED (belam 02:2xZ 09-30: dispatched after PASS B3 lands; worktree cleanup first).
