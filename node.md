---
id: hypothesis:a00-93087928-918ad7
mint_id: 4a3c6d4f3d5545dda7ea0bb14e96ef1b
type: hypothesis
parents:
  - goal:g9.4
confidence: 0.3
edited_by: season.py
scaffold_hash: 85031ebaddad0f1a
season: 1
thought_session: season
title: A00 93087928 918ad7
verdict: pending
---
# hypothesis:a00-93087928-918ad7

## Hypothesis

The existing graph data structures (node adjacency from `parents`/`children` edges, agent positions from session/iteration metadata) are sufficient to render a navigable ASCII viewport at zoom level 3 showing the full node graph in a terminal, with agents positioned at their working nodes.

### What would prove it
A working CLI command (e.g. `agi viewport --level 3`) that:
- Renders the full graph as connected nodes (not truncated)
- Supports up/down/left/right panning via arrow keys
- Positions agents as distinguishable markers at their current working nodes
- Uses a single unified ASCII renderer (not the current fragmented dump renderers)
- Runs beside a live Claude Code session and lets an observer watch agent movement

### What would disprove it
- The existing node data lacks spatial positioning information needed for meaningful layout, producing a graph that is no more informative than the current truncated list
- Terminal escape code or curses handling for panning introduces complexity that makes the viewport non-viable as a "ride-along" tool
- The unified renderer cannot satisfy both the viewport requirements and the existing dump/report use cases without abstraction leaks



## Agent Notes
Filled in hypothesis: existing graph data structures are sufficient for ASCII viewport renderer at level 3 with pan/zoom/agent positioning. No experiments run yet — pending.