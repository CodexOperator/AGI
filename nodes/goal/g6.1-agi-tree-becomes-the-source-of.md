---
confidence: 1.0
goal_id: G6.1
goal_kind: subgoal
id: "goal:g6.1"
mint_id: 73547cd61d2f4e37847b43ee6e050a83
origin: goals-doc
parents:
  - goal:g6
seeds:
  - exp:stitch-roundtrip-r1
  - idea:engine-decompose-engine
  - idea:engine-stitch
status: active
tags:
  - goal
  - subgoal
title: "G6.1: agi-tree becomes the source of truth agi is assembled from"
type: goal
---

**The direction of authority reverses.** Today the graph describes the engine
after the fact. The target is that the engine is *assembled from* the graph —
the code is a projection of level-3 nodes, not a thing the nodes comment on.
This is the goal G2.1 serves and the reason level 3 is built first.

Ordering that follows from it: a decomposition census (which surfaces exist) →
level-3 nodes with contracts attached (what each promises) → stitch-to-directory
(the projection runs) → the engine's own changes originating as nodes.
