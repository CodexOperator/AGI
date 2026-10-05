---
id: goal:g7.16.1.11.11.2
mint_id: 61c6f5d89a28462897cad192b280526b
type: goal
key: 664244b07d7040d2
parents:
  - goal:g7.16.1.11.11
next_edges: []
confidence: 0.6
edited_by: director-thought-2
goal_id: G7.16.1.11.11.2
goal_kind: subgoal
origin: goal
season: 2
seeds:
  - goal:g7.16.1.11.11
  - hypothesis:aa1-v4-wake-still-shells-send-py
status: active
tags:
  - council
  - aa1
  - mail
  - g7.16.1.11.11
title: "G7.16.1.11.11.2: AA1 box KEEP as THE mail path; send.py MOVE never git rm; g1.40 FOLDS (flock SCRAP)"
town: core
---
# goal:g7.16.1.11.11.2

## Why this exists
goal:g7.16.1.11.11 (AA1 boxes): SM [coord] 20:48Z 10-05 placed this nested leaf from hypothesis:aio-w-and-mail-one-living-path (AIO, trunk 703e7ad58). Parent already has AA1.M (goal:g7.16.1.11.11.1). AIO CLAIM v1 had send.py KEEP-until-move + g1.40 flock. Owner 20:42Z (SM [coord] 20:56Z) superseded: send.py MOVE never git rm; AA1 box is THE mail; g1.40 FOLDS (refs no RMW, flock SCRAP).

## Target end-state
- `box` KEEP (AA1 THE mail). No new mail primitive beside it.
- send.py MOVE (deprecate+move, never `git rm`) — owner 20:42Z; not KEEP-until-last-old-setup-moves.
- A v4 post writes no `.agi/sessions/inbox`. Delivery is refs/box + refs/held.
- g1.40 FOLDS: refs have no RMW, so flock SCRAP. Do not copy `_foreign_memo_lock` onto inbox.
- Host acts stay Prime GO, not this bundle.

## Invariants
- Forward-only refs (parent AA1). No flag day.
- Nothing is deleted. 0 B in the zygote.
- No implement on this mint (SM: No implement yourself).

## Falsifier
1. `wc -c` of the box script stays the AA1 cap on the trunk AND `git grep -n 'sessions/inbox' --` the box script + v4 agi-run wake line prints 0.
2. Negative: a v4 post's `box send` / `box read` path never opens send.py; `git grep -l send.py --` the v4 agi-run wake line prints 0.

## Out of scope
goal:g7.16.1.11.15.1 (PHASE W) · goal:g7.16.1.11.11.1 (AA1.M already placed) · host acts · agi-infer · season.py rollover --apply · g1.40 flock (SCRAP)

## Agent Notes
Assigned to **director-thought-2**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-thought-2 21:39Z 10-05 (date -u): owner IMPLEMENT NOW named DT2. Nested hypothesis:aa1-v4-wake-still-shells-send-py -> experiment:dt2-aa1-wake-send-py-1005 -> verdict PROVED: box 2005 inbox-free; agi-run wake still shells send.py. Did not MOVE send.py. Did not git rm. Did not push.
<!-- THOUGHT:END -->
