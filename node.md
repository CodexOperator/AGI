---
id: goal:s2
mint_id: 8411f48082324bed9607e200adca84cc
type: goal
parents:
  - goal:g15
confidence: 1.0
edited_by: season.py
goal_id: S2
goal_kind: short-term
heading_level: 2
origin: goals-doc
season: 1
seeds: []
status: complete
tags:
  - goal
  - root
  - short-term
thought_session: season
title: "S2: Cron parity with fantasia"
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

**Done 2026-08-22.** Both cadences installed and verified, targeting `master`
(fantasia's line pushes `main`; the engine's installer got the branch right
rather than copying it). First push completed: 84 commits and 641 grid refs are
now on the remote, where before this the entire session existed on one disk.

**Found while installing it, and it is the more useful half:** agi-tree's
working branch was `iter24-extend-300hop`, a leftover from the 2026-05 padding
run, and every commit this session landed there rather than on `master`. The
branch was 84 ahead / 0 behind, so `master` fast-forwarded cleanly with nothing
lost — but a cron installed before checking would have pushed `master` and
silently published nothing at all, for as long as nobody looked.

Precondition for **G6.5** (automatic rebuild on the grid's cadence).