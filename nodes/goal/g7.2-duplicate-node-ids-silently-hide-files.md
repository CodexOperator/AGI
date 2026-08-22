---
confidence: 1.0
goal_id: G7.2
goal_kind: subgoal
id: "goal:g7.2"
origin: goals-doc
parents:
  - goal:g7
seeds: []
status: active
tags:
  - goal
  - subgoal
title: "G7.2: Duplicate node ids silently hide files on disk"
type: goal
---

Found 2026-08-22 by the G9.1 dashboard on its first run, which is the argument
for G9 in miniature: **17 node ids are declared by two files each.** The loader
keeps one and drops the other, so 17 files sit on disk fully invisible to every
tool that reads this graph — the renderer, the metrics, the chain finder, and
the dashboard itself.

The dropped file is frequently the *larger* one: `app-purpose:graph-core` keeps
a 276-byte file and hides a 575-byte one; `bigger-outcome:graph-core-r1` keeps
315 bytes and hides 1,217. This is not a cosmetic duplicate — it is content
loss that has already happened and that nothing reported.

Fix: id uniqueness must be checked at load and at write. A second file claiming
a live id is an error, not a silent preference for whichever sorts first.
**Do not resolve the existing 17 by deleting either side** — merge or re-id
them deliberately, the G7 rule.
