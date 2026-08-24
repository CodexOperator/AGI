---
confidence: 1.0
goal_id: G2
goal_kind: long-term
id: "goal:g2"
origin: goals-doc
seeds:
  - exp:zoom-numeric-axis-r1
  - goal:g2.1
  - goal:g2.2
  - goal:g2.3
  - goal:g2.4
  - goal:g2.5
  - idea:engine-embeddings
  - idea:engine-zoom
status: active
tags:
  - goal
  - root
title: "G2: Adjustable zoom with contracts that survive the trip"
type: goal
---

One graph readable at five grains, where level 3 is **actual code nodes that
stitch into a runnable directory layout** — the property that makes the graph an
executable artifact rather than a description of one. Build level 3 first and
treat the others as projections around it.

**Invariant:** one node at level N ⇔ a collection at level N+1, and back.

🔴 **Already falsified for the free-form implementation, and the number is
known:** 0.441 overall claim recall against a 0.90 bar, 12 agents over 6
complete round trips. Loss is category-structured, not uniform — prose survives
at 0.792, structured frontmatter recalls **0.000** (0/24, zero variance). Node
identity is destroyed outright, and it is not a capacity problem: the children
were longer than the parents.

**Design consequence:** zoom is a lossy transform, not a view. To behave like a
view, contract-bearing parts must not pass through a model at all — the harness
attaches inherited frontmatter and contract slices mechanically, and only prose
round-trips. Ground truth and scoring rule are preserved at
`agi/context/refs/zoom-roundtrip-ground-truth/` so the follow-up A/B stays cheap.

Owns: **L1** (the 1..5 axis), **L2** (live IO maps as inherited contract slices).
