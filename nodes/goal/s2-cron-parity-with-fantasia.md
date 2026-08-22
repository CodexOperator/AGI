---
confidence: 1.0
goal_id: S2
goal_kind: short-term
id: "goal:s2"
origin: goals-doc
seeds: []
status: active
tags:
  - goal
  - root
  - short-term
title: "S2: Cron parity with fantasia"
type: goal
---

`grid.py cron install` sets both cadences — a 5-minute grid snapshot + push
(crash window ≤ 5 minutes) and an hourly main-branch push. fantasia has this;
**agi-tree does not**, and the grid was only initialised in this project on
2026-08-22.

Until it is installed, every guarantee that rests on "sync is automated, nobody
syncs by hand" is false here, and the grid's 535 refs exist only on this
machine. Install it, verify both entries land, and confirm a push actually
reaches the remote rather than assuming the cron line is correct — a cd-less
cron line is exactly the class of small operational error the design ethic says
the system should absorb.

Precondition for **G6.5** (automatic rebuild on the grid's cadence).
