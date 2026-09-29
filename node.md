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

## Why this exists
goal:g7.16.1 (the council loop): a next-bundle candidate for the council to place, right after bundle 4's W1 (goal:g4.18.5, "a write is a commit") and W2 (goal:g4.18.6, links are mint ids). Measured 22:4xZ 09-29 by belam-S2-L5-XVIII from `crons.py show`: every 5 minutes, `grid.py commit --all --prefix 'cron: '` walks all ~5k nodes on the slow /data disk (~35 ms per op) and versions every changed one onto refs/grid/*, followed by `grid.py push-chan`; the crontab self-heal (`crons.py apply`) rides the same line, chained with `;`. Known costs: an uncommitted node gets versioned within minutes (doc:card-belam trap 3), and the shared mint c89ca4b1 grew by 2 versions per tick (verdict:dg2b4-w2d1).

## Target end-state
- No cron runs `grid.py commit` or `grid.py push-chan`. A node's version history is the git log of the write commits that touched it, keyed by mint id: each write commit carries a `Mint-Id: <mint_id>` trailer, so `git log --grep` follows a node across renumbers and retire-moves.
- ONE full-graph snapshot every ~15 minutes: a single catch-all commit + push of whatever is still dirty under `.agi/nodes`, whose cadence is a cell in config:crons.
- `crons.py apply` keeps running on its own line; the branch-mirror pushes, fetch, wake and memory_alarm are untouched.
- The existing refs/grid/* stay read-only as an archive. `grid.py log|diff|versions|payload` read the trailer history first and the old refs second.

## Invariants
- Nothing is lost: `active_node_count + deprecated_node_count` never drops, and every node version made before the cutover stays readable.
- The snapshot never commits another post's half-written file that write.py would have refused (the same authorship gate as goal:g4.18.5).

## Falsifier
1. `python3 extensions/agi/bin/crons.py show` lists no `grid.py commit` and no `grid.py push-chan`, and lists one snapshot job at the configured cadence.
2. For a node renumbered after the cutover, the trailer history (`git log --grep 'Mint-Id: <mint>'`) returns every version from both addresses.
3. Negative: zero refs/grid/* refs are created or moved after the cutover.

## Out of scope
goal:g4.18.5 · goal:g4.18.6 · goal:g7.16.1.5 · deleting any refs/grid/* ref (never).

## Agent Notes
Assigned to **the council** (placement).
