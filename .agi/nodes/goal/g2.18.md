---
id: goal:g2.18
mint_id: 230ab5972f244a6ca8a6c7dc7366999a
type: goal
parents:
  - goal:g2
confidence: 1.0
edited_by: belam
goal_id: G2.18
goal_kind: subgoal
heading_level: 3
origin: goals-doc
season: 1
seeds: []
status: horizon
tags:
  - goal
  - subgoal
thought_session: g1-g7-rewrite-2026-09-19
title: "G2.18: Pick a node, see its history; pick a version, see how it got there"
---
The viewport is only half of it. From any node on the web:
- **select the node → its version history**, straight off the git grid
  (`refs/grid/node/<id>`), which already records one version per change;
- **select a version → what produced it** — for a non-build node, the chat and
  reasoning that wrote it; for a build node, the code at that version and the
  chain that led to it.

The data mostly exists already and is unused: the grid holds per-node and
per-session refs, `grid.py log|diff|versions` can read them, and session drafts
are versioned under `refs/grid/session/*` — including drafts that were rejected.
**Rejected drafts are the interesting ones**, because they are the only record
of what the loop considered and declined.

Gap to close: nothing currently links a node version back to the *session* that
produced it. That link is what turns the grid from storage into history.

---
