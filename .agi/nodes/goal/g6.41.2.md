---
id: goal:g6.41.2
mint_id: 4fadd19988124cd094ba6ebbc2ecfcd4
type: goal
parents:
  - goal:g6.41
next_edges: []
confidence: 0.95
edited_by: belam
goal_id: G6.41.2
goal_kind: subgoal
origin: goals-doc
scaffold_hash: 2bcadbd39bc3f439
season: 2
seeds: []
status: complete
tags:
  - goal
  - g6
  - heal
  - log
title: "G6.41.2: every heal/reaper log line opens with its UTC second -- one stamp in the shared sink"
town: core
---
# goal:g6.41.2

# goal:g6.41.2

## Why this exists
goal:g6.41 (graceful recovery when a seat dies): after the 01:55Z 09-30 reboot the Prime had to reconstruct the boot timeline by lining up untimed heal lines against crash-recovery record names (all-is-one.20260930T020259Z.json ...), because the reaper log (~/logs/agi-reaper-<hash>.log, 153k lines) carried no time at all.

## Target end-state
- Every line through the one shared sink `reaper_log.log()` (heal watch, send.py wake) opens with its UTC second, `YYYY-MM-DDTHH:MM:SSZ `, in the file and in the stderr fallback.

## Invariants
- One stamp site: `reaper_log._stamp`; no writer stamps twice. rotate.py's autopsy still finds a pid by substring.

## Falsifier
1. `python3 -m pytest $(grep -l 'AGI_REAPER_LOG\|reaper_log' extensions/agi/tests/test_*.py) -q` passes (746 at 09-30 02:1xZ), and test_wake_logs_one_outcome_line_via_reaper_resolver asserts the stamp.
2. Negative: `tail -1 <reaper log>` after a heal restart never starts with `watch:`.

## Out of scope
goal:g6.41.1 (recovery itself) · goal:g6.41.1.1 (the boot wake line).

## OWNER 2026-09-30 02:1xZ, verbatim
"Need to add timestamps to heal log for sure you can do it yourself if needed"

## Agent Notes
Assigned to **belam**.
