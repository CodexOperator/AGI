---
confidence: 1.0
goal_id: G7.9
goal_kind: subgoal
heading_level: 3
id: "goal:g7.9"
mint_id: 3c2c2f43062c4beabcf8fc694f561956
order: 47
origin: goals-doc
parents:
  - goal:g7
seeds: []
status: active
tags:
  - goal
  - subgoal
title: "G7.9: A scan must not prune quietly, and `level3.py` is misnamed"
type: goal
---

Two changes to the same file, grouped because they touch the same lines and
the rename is the safer half.

**1. The prune must be loud and gated.** `bin/level3.py` deletes every node
whose `origin` it recognises but does not re-derive on that run, and reports
the count in a line that reads the same whether it pruned 0 or 185. That is
the H0/H0i failure mode with the safety catch still missing: the two
data-loss defects this project has already paid for were both a scan quietly
removing what it did not recognise. A prune should require an explicit flag,
announce every id it is about to drop, and refuse outright above a threshold
-- a scan that would delete most of its own output is reporting a bug, not
doing its job. **S11** flags this as the sharp edge of the `level3` rename;
this goal owns the guard itself, independent of any rename.

**2. `level3.py` is named after a zoom level, which is the category error
G2 and G10.2 both record.** The file is the entry point for the code-level
view of the graph -- the thing you load into at the start of a workflow --
so it should be named for that: `view.py`, `main.py` or similar. Sequence it
the way **S11** demands: teach the reader both names, migrate, then retire
the old name. Never the reverse.

Deliberately not over-specified -- the final name and the rest of this
update are being decided in a parallel session. What is fixed here is the
*property*: **no node disappears without something saying so first.**

Pairs with **S11**, **G7.5** (parse failures swallowed with zero signal) and
**G6.6**.
