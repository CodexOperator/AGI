---
confidence: 1.0
goal_id: G6.5
goal_kind: subgoal
id: "goal:g6.5"
origin: goals-doc
parents:
  - goal:g6
seeds: []
status: horizon
tags:
  - goal
  - subgoal
title: "G6.5: Rebuild agi from agi-tree automatically, on the grid's cron"
type: goal
---

The grid already syncs on two cadences (5-minute grid push, hourly branch push)
and `grid.py cron install` sets both. Add the rebuild to that schedule: when the
cron runs, re-derive the census, re-scan level 3, and run `stitch --verify`, so
drift between graph and engine is detected within one cadence instead of
whenever someone happens to look.

**Verify only, until G6.3 lands.** A cron that *writes* the engine from the
graph before the version layer is trusted is a data-loss defect waiting to
happen, and this project has already paid for that class twice. Report drift;
do not silently reconcile it.

Pairs with **S2** (cron parity with fantasia) — there is no point scheduling a
rebuild on a project whose basic sync cadence is not set up.
