---
id: goal:g7.9
mint_id: 3c2c2f43062c4beabcf8fc694f561956
type: goal
parents:
  - goal:g7
confidence: 1.0
edited_by: season.py
goal_id: G7.9
goal_kind: subgoal
heading_level: 3
origin: goals-doc
season: 1
seeds: []
status: horizon
tags:
  - goal
  - subgoal
thought_session: season
title: "G7.9: A scan must not prune quietly, and `level3.py` is misnamed"
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

## A refused publish is not a no-op — observed 2026-08-27

`publish-engine.sh` gates in order and refuses late, but **step 1 already
mutated the graph**. During the `level3` -> `build` rename it refused at gate 3
("the graph disagrees with its own contracts") — correctly — after gate 1 had
run the *engine's* `level3.py`, which was still the pre-rename copy. That run
wrote **184 nodes into a freshly recreated `nodes/level3/`**, each with a
newly minted `mint_id`, none of them tracked, none of them wanted.

The 5-minute grid cron then committed all 184 to `refs/grid/node/*` before
anyone looked, so a refusal produced durable version history for nodes that
should never have existed. They were removed by hand; `node_count` went
970 -> 785, which is the correct number.

Nothing was lost and no ids collided — checked before deleting, because "the
scan recreated its own output under the old name" and "there are two nodes for
one file" are different situations and only the first is safe to `rm`. But the
property that failed is the one this goal is about: **a command that refuses
should leave nothing behind.** Re-deriving contracts is idempotent in ordinary
use, which is exactly why it was placed before the gates and exactly why the
one time it was not idempotent — mid-rename, with the engine and graph
disagreeing about a directory name — it went unnoticed until a node count was
read.

Asks, in addition to the prune guard above:

- **Gate before mutating.** Every refusal check that can run first should run
  first; contract re-derivation belongs after the graph and engine are known
  to agree, not before.
- **Or make the mutation reversible** — a scan that writes to a directory it
  did not previously own should say so, loudly, and that is the same warning
  the prune needs.