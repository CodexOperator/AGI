---
id: goal:g2
mint_id: bcbb7e64bb824b74876ad5db95c89969
type: goal
confidence: 1.0
edited_by: season.py
goal_id: G2
goal_kind: long-term
heading_level: 2
origin: goals-doc
season: 1
seeds:
  - exp:zoom-numeric-axis-r1
  - goal:g2.1
  - goal:g2.10
  - goal:g2.11
  - goal:g2.2
  - goal:g2.3
  - goal:g2.4
  - goal:g2.5
  - goal:g2.6
  - goal:g2.7
  - goal:g2.8
  - goal:g2.9
  - idea:engine-embeddings
  - idea:engine-zoom
status: horizon
tags:
  - goal
  - root
thought_session: season
title: "G2: Adjustable zoom with contracts that survive the trip"
---
One graph readable at five grains, where level 3 is **actual code nodes that
stitch into a runnable directory layout** — the property that makes the graph an
executable artifact rather than a description of one. Build level 3 first and
treat the others as projections around it.

**Invariant:** one node at level N ⇔ a collection at level N+1, and back.

**Two axes, not one — and conflating them is the mistake this goal keeps
making.** *Zoom* is **where you are standing**: far out shows supernode
groupings, base level shows build nodes, closer shows a node's version history,
closest shows the chat that produced a version. *LOD* is **how much detail is
drawn at wherever you stand**, dialled up or down independently. Every zoom
position has its own LOD range. Zoom is **G2.5**–**G2.7**; LOD is **G2.8**–**G2.9**.

⚠️ **`level3` as a node type is legacy stale wording, and the graph should carry
no zoom-level names at all.** A zoom level is a *view*, and baking a view's name
into the data was a category error: it froze one grain into the type system and
made the other grains unnameable. Zoom is now organised on two axes and neither
of them is a level number — coarser grains come from **tags and addresses**
(G2.5, G2.6), finer grains from **mint ids and the grid** (G2.7). A node is a
node. Retiring the name is **S11**; it is mechanical and touches ~180 files, so
it is sequenced deliberately rather than done in passing.

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