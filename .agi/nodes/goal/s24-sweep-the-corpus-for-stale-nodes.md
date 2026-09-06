---
id: goal:s24
mint_id: 92c99c4d207c402f87dfea8507136976
type: goal
parents:
  - goal:g15
confidence: 0.8
edited_by: director
goal_id: S24
goal_kind: short-term
heading_level: 2
origin: goals-doc
seeds: []
status: horizon
tags:
  - goal
  - root
  - short-term
thought_session: agi-master-2026-09-06
title: "S24: Sweep the corpus for stale nodes: orphan @v2s and filler chain extensions"
---
**The owner's ask, 2026-09-02, alongside the goal sweep: the same pass the
goals just got, applied to the nodes.** A goal sweep classifies 41 declarations;
this classifies 861 nodes. Two populations are named as suspects, and both are
known to exist rather than guessed at:

1. **Standalone `@v2` nodes.** `goal:g6.3` retired the `@v2` convention — a
   version is a grid commit, not a second file — and the five `@v2` nodes it
   left behind are deprecated but still resolve as chain head. `HANDOFF.md`
   records the trap: *"a `@v2` node is the publish head, not the v1 node"*.
   Any `@v2` that is no longer anything's head is residue.
2. **Chain-extension fillers attached to other fillers.** This corpus already
   had 9 chains x 2000 hops of shortcut cycles carrying no signal, purged under
   `goal:g6.2`/`goal:s15`. The metric that rewarded them is gone
   (`goal:g3`), but nothing has since asked whether smaller instances of the
   same shape survived — a hop whose only parent is another hop, with no
   evidence at either end.

**Retire, never delete** — `status: deprecated` into `.agi/nodes/deprecated/`.
The reason is mechanical: a node's grid ref outlives its file, so deleting
decouples the durable structure instead of shrinking it. **Verify
`active_node_count` + `deprecated_node_count` never drops.**

**Gated on `goal:s23`.** Retiring nodes in bulk before deprecation suppresses
injection would move the clutter rather than remove it — the map would carry
every swept node exactly as it carries `build:TODO.md` today.

## Falsifier

Every node the pass retires is one a named rule already condemns — an orphaned
`@v2`, or a hop with no evidence and no non-hop parent. State the rule that
caught it per node. **A node retired because it "looks stale" is the failure
case**, and the count moving is not the result: this project has already
watched a sweep that undid no work move the primary metric by 0.038, which is
why `goal:g5` had to be revised before this could safely run at all.