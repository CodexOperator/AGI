---
id: goal:g7.16.1.7.1.3
mint_id: e6fff7ecc5104289ad08e7213c3c5085
type: goal
parents:
  - goal:g7.16.1.7.1
next_edges: []
confidence: 0.6
edited_by: director-general-5
goal_id: G7.16.1.7.1.3
goal_kind: subgoal
origin: council-loop
scaffold_hash: eba692bad43b5500
season: 2
seeds: []
status: horizon
tags:
  - templates
  - spawn
  - rotate
  - council-loop
title: "G7.16.1.7.1.3: ONE pi harness template -- JSON model rows (model, thinking, extendable settings), exactly one default marker; pi / pi-free / pi-local retired by name"
town: core
---
# goal:g7.16.1.7.1.3

## Why this exists
goal:g7.16.1.7.1 (7a, NOW in the council placement) under goal:g7.16.1.7: the owner, verbatim there: "No more templates for pi free vs pi local. Just standard pi template that lists all the different model + thinking level + extendable to other harness settings as rows containing jsons." Measured: .agi/config.json carries 3 pi blocks (pi, pi-free, pi-local) with adapter, bin and forward_env copied 3x, differing only in provider / models / thinking / zero_usd; spawn.harness and workflows.*.provider name pi-free. Absorbs by name goal:g4.20.1 (one harness source).

## Target end-state
- ONE pi harness template node: shared cells once (adapter, bin, forward_env); a rows list of JSON objects, one per usable model (model, provider, thinking, zero_usd, max_live, ... extendable), covering the internal aliases in use; exactly ONE row carries the default marker.
- A post or a route picks a row by name at stand-up or on the fly; no row name is a harness id.
- The old pi-free / pi-local / pi harness ids resolve (for one season) as aliases onto rows, each alias named in the template, then retire.

## Invariants
- Exactly one default row. A paid row is never the default (the free lane stays the default, goal:g4.20.1).

## Falsifier
1. The walk (goal:g7.16.1.7.2.1) resolves harness pi + no row -> the default row, and pi + row <name> -> that row, in its test file.
2. Negative: zero harness blocks named pi-free or pi-local remain in .agi/config.json (grep = 0) once the aliases retire.

## Out of scope
goal:g7.16.1.7.2.1 · goal:g7.16.1.7.2.3 · goal:g7.25 (third-party adapters)

## Agent Notes
Assigned to **director-general-5**.
