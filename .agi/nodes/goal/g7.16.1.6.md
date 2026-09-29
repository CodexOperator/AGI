---
id: goal:g7.16.1.6
mint_id: 383535579260452a90b125e1efe446f6
type: goal
parents:
  - goal:g7.16.1
next_edges: []
confidence: 0.6
edited_by: belam
goal_id: G7.16.1.6
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: 4eeffc40c1f641b8
season: 2
seeds: []
status: horizon
tags:
  - grid
  - crons
  - council-loop
title: "G7.16.1.6: no grid crons -- every write is a mint-keyed commit, plus one full-graph snapshot every ~15 min"
town: core
---
# goal:g7.16.1.6

## OWNER 2026-09-29 22:4xZ, verbatim (Prime pane)
"Also can't we eliminate grid crons if every write is a node commit?  Then the only snapshot is a full graph snapshot every 15 mins or so. No more grid crons at all"

## OWNER 2026-09-29 23:0xZ, verbatim (Prime pane) -- the shape, supersedes the Prime's trailer design below
"So my idea was that the write node commit would still go into the grid. It's still there for per-node history as that's still valid and needed in the future if we do updates patches reworks etc. but we commit ONLY to the grid ref and the specific grid ref that belongs or is created for that node. So all node writes ARE grid commits, but only on individual nodes. Even less storage and memory bloat than the grid commit skip dupes thing. So no need for grid cron, but still a need for the grid as a commit target for individual node writes. The overall snapshot stays as you described. Does that make sense?"
## Why this exists
goal:g7.16.1 (the council loop): a next-bundle candidate for the council to place, right after bundle 4's W1 (goal:g4.18.5, "a write is a commit") and W2 (goal:g4.18.6, links are mint ids). Measured 22:4xZ 09-29 by belam-S2-L5-XVIII from `crons.py show`: every 5 minutes, `grid.py commit --all --prefix 'cron: '` walks all ~5k nodes on the slow /data disk (~35 ms per op) and versions every changed one onto refs/grid/*, followed by `grid.py push-chan`; the crontab self-heal (`crons.py apply`) rides the same line, chained with `;`. Known costs: an uncommitted node gets versioned within minutes (doc:card-belam trap 3), and the shared mint c89ca4b1 grew by 2 versions per tick (verdict:dg2b4-w2d1).

## Target end-state
- Every node write IS one grid commit onto that node's OWN ref (refs/grid/<mint>, created on first write): plumbing only (hash-object -> mktree -> commit-tree -p <ref tip> -> update-ref with the old tip as a compare-and-swap), so a write never touches the branch, MAIN's index or HEAD, and never waits on verify-suite.lock. History stays keyed by mint id, so it survives renumbers and retire-moves with no trailer. No cron runs `grid.py commit`. This AMENDS goal:g4.18.5's target ("a write IS a git commit"): the commit target is the node's grid ref, not the branch (W1b, 14cf86000, commits on the branch by exact path today).
- ONE full-graph snapshot every ~15 minutes: a single catch-all commit + push of whatever is still dirty under `.agi/nodes`, whose cadence is a cell in config:crons.
- `crons.py apply` keeps running on its own line; the branch-mirror pushes, fetch, wake and memory_alarm are untouched.
- The existing refs/grid/* histories simply continue: the first write after the cutover parents onto the ref's current tip. The ~15-min snapshot is the branch's only node writer and the push point for other boxes; grid refs push with it.

## Invariants
- Nothing is lost: `active_node_count + deprecated_node_count` never drops, and every node version made before the cutover stays readable.
- The snapshot never commits another post's half-written file that write.py would have refused (the same authorship gate as goal:g4.18.5).

## Falsifier
1. `python3 extensions/agi/bin/crons.py show` lists no `grid.py commit` and no `grid.py push-chan`, and lists one snapshot job at the configured cadence.
2. For a node renumbered after the cutover, `git log refs/grid/<mint>` returns every version from both addresses, and one write moves exactly one ref (refs/grid/<mint>) and no branch.
3. Negative: zero branch commits made by a single node write after the cutover (the ~15-min snapshot is the only branch writer for nodes), and zero refs/grid/* refs deleted.

## Out of scope
goal:g4.18.5 · goal:g4.18.6 · goal:g7.16.1.5 · deleting any refs/grid/* ref (never).

## Agent Notes
Assigned to **the council** (placement).
