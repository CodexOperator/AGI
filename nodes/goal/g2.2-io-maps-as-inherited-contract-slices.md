---
confidence: 1.0
goal_id: G2.2
goal_kind: subgoal
id: "goal:g2.2"
origin: goals-doc
parents:
  - goal:g2
seeds: []
status: horizon
tags:
  - goal
  - subgoal
title: "G2.2: IO maps as inherited contract slices"
type: goal
---

Every node declares required inputs and promised outputs, each with a how/why,
a performance note and a security note; the maps re-derive when neighbours
change. Blocked on G2.1 — an IO map needs a code-level node to hang off.
