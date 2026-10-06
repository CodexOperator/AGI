---
id: goal:g7.16.1.7.2.1
mint_id: 442aec9983da4af7b058d3b8cc6a70b9
type: goal
parents:
  - goal:g7.16.1.7.2
next_edges: []
confidence: 0.6
edited_by: director-general-4
goal_id: G7.16.1.7.2.1
goal_kind: subgoal
origin: council-loop
scaffold_hash: c0b82d72326d799d
season: 2
seeds: []
status: retired
tags:
  - templates
  - spawn
  - rotate
  - council-loop
title: "G7.16.1.7.2.1: ONE link walk resolves a post's template chain -- formation -> post -> harness -> model, nearest wins, <= walk_max hops (a config cell), cycle-guarded"
town: core
---
# goal:g7.16.1.7.2.1

## Why this exists
goal:g7.16.1.7.2 (7b, after goal:g7.16.1.6 + goal:g4.18.6, council placement alive 23:4xZ) under goal:g7.16.1.7: its target end-state is nested, recursive, dynamically linked templates. Measured 23:3xZ 09-29 by director-general-5 (council-loop room [measure] line): 6 sources and 5 resolver functions answer one question -- which harness/model/effort/settings a post runs on. Everything else in the bundle reads THIS walk, so it comes first and touches no live path. Absorbs by name the old bundle-5 B4 (one config reader, goal:g7.16.1.4).

## Target end-state
- ONE read-only resolver module walks link rows (mint ids, goal:g4.18.6) from a formation template through a post template (+ its customizations) to a harness template to a model row, and returns one resolved mapping per post.
- Nearest wins (owner 23:3xZ point 1): post customizations over the harness template over the model default.
- The walk limit is a config cell (default 5, owner 23:3xZ point 2); a cycle or a walk past the limit returns ONE finding naming the whole chain (a simplify leaf or a [red]), never a silent error or a partial answer.
- An override equal to the value it inherits is REFUSED (council guard, alive 23:4xZ): a customization must change something.
- Every resolved field carries its source node (which template won), so a reader can say why a post runs what it runs.

## Invariants
- The walk never writes. A template field is read from ONE node; nothing is copied.

## Falsifier
1. The resolver's own test file passes: a 3-hop chain resolves with nearest-wins provenance; a 6-hop chain and a 2-node cycle each return one finding naming the chain.
2. Negative: the resolver module imports nothing from rotate.py, heal.py or dispatch.py (grep = 0).

## Out of scope
goal:g7.16.1.7.1.3 · goal:g7.16.1.7.2.2 · goal:g7.16.1.7.2.3 (callers are wired there)

## Agent Notes
Unassigned (was director-general-4).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-1 08:4xZ 09-30: re-laned to director-general-4 (the link walk resolves the stand-up template chain (rotate.py / adapters)) after the owner's stand-down of director-general-5 and director-general-6 (06:1xZ), by sanctuary-master's file-owner map (rotate.py / stand-up / heal / adapters / keys / post rows -> DG4; dispatch.py launch resolvers / RAM writers / render / viewport -> DG3). Status unchanged.
<!-- THOUGHT:END -->

<!-- THOUGHT: season3 rollover: retired empty leaf (no builds/outcomes/children). -->
