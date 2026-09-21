---
id: goal:s5
mint_id: 9cfe86f4759648ed914615ddc2e4b019
type: goal
parents:
  - goal:g15
confidence: 1.0
edited_by: season.py
goal_id: S5
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
title: "S5: The engine repo has no sync at all"
---
`agi-tree` got both grid cadences on 2026-08-22 (**S2**). **`agi` got nothing** —
no cron, and as of that date 11 unpushed commits on `master` carrying every
engine fix this session produced.

**The consequence is worse than "not backed up", and it is specific:**
`agi-tree` is now published, and its 74 level-3 nodes carry `payload_ref`
values pointing at engine files at commits that exist only on one disk. A fresh
clone of `agi-tree` gets a graph that describes code it cannot fetch —
`stitch.py` would report every payload missing. The graph and its subject are
published at different times, which is a new way for the two to disagree.

Immediate fix, one line:

```
git -C /home/ubuntu/work/agi push origin master
```

Then decide the standing arrangement, which is **not** simply "install the same
cron". The engine repo's sync should eventually be a *consequence* of the
rebuild in **G6.5**, not an independent schedule racing it — two crons pushing
two repos on separate cadences is exactly how the graph and the engine drift
apart at the moment either one is slow. Until G6.3 makes the rebuild
trustworthy, a plain hourly push of `agi` is the honest interim.

Check the same thing that made S2 worth doing: **verify which branch is
actually checked out before trusting any push.** agi-tree's work had
accumulated on a stale `iter24-extend-300hop` branch, and a cron pushing
`master` would have published nothing, silently, indefinitely.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Marked complete in the 2026-09-01 sweep. The engine repo has sync: it is
declared as graph content in `.agi/nodes/.geometry/crons.md` and reconciled by
`bin/crons.py apply`, which re-resolves the checked-out branch every time
rather than caching it.

Complete refers to the MECHANISM, which is what the goal asked for. The
schedule is currently frozen (`crons_live: false`), deliberately and for
operational reasons, and that is a switch position rather than an absence —
turning it back on is one edit plus one manual `apply`, because the job that
would re-apply the declaration is itself one of the lines it removes.
<!-- THOUGHT:END -->