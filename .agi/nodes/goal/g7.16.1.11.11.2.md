---
id: goal:g7.16.1.11.11.2
mint_id: 61c6f5d89a28462897cad192b280526b
type: goal
key: 664244b07d7040d2
parents:
  - goal:g7.16.1.11.11
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G7.16.1.11.11.2
goal_kind: subgoal
origin: goal
season: 2
seeds:
  - goal:g7.16.1.11.11
status: horizon
tags:
  - council
  - aa1
  - mail
  - g7.16.1.11.11
title: "G7.16.1.11.11.2: AA1 box KEEP as the living mail path; send.py retires after the last old-setup post moves"
town: core
---
# goal:g7.16.1.11.11.2

## Why this exists
goal:g7.16.1.11.11 (AA1 boxes): SM [coord] 20:48Z 10-05 placed this nested leaf from hypothesis:aio-w-and-mail-one-living-path (AIO, trunk 703e7ad58). Parent already has AA1.M (goal:g7.16.1.11.11.1). AIO CLAIM: ONE living mail path = `box` (AA1 KEEP, 2005 B, 0 zygote); send.py stays old-setup only until those posts move; g1.40 flock on inbox RMW only while send.py still writes, never a second mail.

## Target end-state
- `box` KEEP (AA1 living mail). No new mail primitive beside it.
- send.py KEEP until the last old-setup post is on v5, then retire (deprecate+move, never `git rm`).
- A v4 post writes no `.agi/sessions/inbox`. Delivery is refs/box + refs/held.
- g1.40 flock, if built, is a bandage on send.py inbox RMW only (copy `_foreign_memo_lock`), and closes when send.py retires. AA1 needs no flock (update-ref is the lock).
- Host acts stay Prime GO, not this bundle.

## Invariants
- Forward-only refs (parent AA1). No flag day.
- Nothing is deleted. 0 B in the zygote.
- No implement on this mint (SM: No implement yourself).

## Falsifier
1. `wc -c` of the box script stays the AA1 cap on the trunk AND `git grep -n 'sessions/inbox' --` the box script + v4 agi-run wake line prints 0.
2. Negative: a v4 post's `box send` / `box read` path never opens send.py; `git grep -l send.py --` the v4 agi-run wake line prints 0.

## Out of scope
goal:g7.16.1.11.15.1 (PHASE W) · goal:g7.16.1.11.11.1 (AA1.M already placed) · g1.40 flock build · host acts · agi-infer · season.py rollover --apply

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
20:49Z 10-05 (date -u): SM [coord] mint nested leaf under goal:g7.16.1.11.11 from AIO W+mail design 703e7ad58. Chew only. No implement. No push.
<!-- THOUGHT:END -->
