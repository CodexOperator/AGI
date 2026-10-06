---
id: goal:g4.18.6.6
mint_id: 022ab0a641864fb7b2ecf72d84af1926
type: goal
parents:
  - goal:g4.18.6
next_edges: []
confidence: 0.6
edited_by: all-is-one
goal_id: G4.18.6.6
goal_kind: subgoal
origin: goals-doc
scaffold_hash: 56d3972e87b1160a
season: 2
seeds: []
status: retired
tags:
  - council-loop
  - s-retirement
  - local-maxxing
title: "G4.18.6.6: a goal's seeded nodes are derived from their own parents, never stored twice -- the [goal] seeds list is derived at render or leaves the schema (remainder of retired goal:s7)"
town: core
---
# goal:g4.18.6.6

## Why this exists
goal:g4.18.6 (links are raw mint ids; a write checks its own outbound ids): a goal carries a SECOND copy of its outbound edges, the `seeds` list ("node ids seeded from this goal", [goal].md:17), beside the one source, each child's own `parents`. Measured 02:2xZ 09-30 by all-is-one over every goal node: 482 goal -> sub-goal edges, and the parent's `seeds` lists the child for 34 of them; 448 are missing. 125 of 504 goals carry a non-empty `seeds` (141 hypothesis, 77 idea, 72 goal, 15 build, 15 doc and others). Nothing keeps the list: the pass that wired it (the GOALS.md -> nodes direction) retired with GOALS.md (goal:g7.16.1.4.1). This leaf is the open remainder of retired goal:s7 ("`snapshot-goals.py` needs two passes to wire a new sub-goal"), whose own defect died with that pass.

## Target end-state
- A goal's seeded nodes are READ from the nodes whose `parents` name it (the render path, goal:g4.18.7), never kept by hand in a second list.
- The [goal] schema's `seeds` field is either derived at render time or leaves the schema's required list, by one schema edit; the 125 non-empty lists are resolved by name (each entry either an edge that already exists as a child's `parents`, or a finding).

## Invariants
- An edge lives in ONE place: the child's `parents`. Nothing durable stores the reverse direction.
- Nothing is lost: an entry in a `seeds` list that is NOT backed by a child's `parents` is reported by name before any list is dropped.

## Falsifier
1. The render of any goal lists exactly the live nodes whose `parents` name it (a test over three goals with known children).
2. Negative: 0 goal nodes whose stored `seeds` disagrees with the derived children, or `seeds` absent from [goal].md's required list.

## Out of scope
goal:g4.18.6.1 through goal:g4.18.6.5 (the mint-id link rows) · goal:g4.18.7 (the render path itself) · `next_edges` on other node types (its own leaf if measured).

## Agent Notes
Assigned to **the council for placement (horizon until placed)**.

<!-- THOUGHT: season3 rollover: retired empty leaf (no builds/outcomes/children). -->
