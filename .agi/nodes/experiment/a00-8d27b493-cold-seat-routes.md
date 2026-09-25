---
id: experiment:a00-8d27b493-cold-seat-routes
mint_id: 1a00c5a1d6b4e1c2a9f0d3b7e5c8a11
type: experiment
parents:
  - hypothesis:a00-8d27b493-f91586
next_edges: []
loop: goal:g7.31.3.1@s2
status: complete
title: "Cold seat brief names all five pane routes"
town: core
---
# experiment:a00-8d27b493-cold-seat-routes

## Hypothesis under test

A cold prime-director brief can expose the five pane-facing routes in one compact, contract-named block, without introducing a sixth special route.

## What changed

Added a `Pane-facing agent routes` section near the top of `extensions/agi/briefs/prime-director-successor.md`. It lists the exact contract names from `goal:g7.31.3`: `write`, `read`, `send`, `dispatch | workflow`, and `rotate | spawn`, with each engine seam and a rename rule.

## Proof

A direct read/grep of the changed brief shows all five numbered route names and their CLI seams. A small assertion over the file confirms `routes_present=True` and exactly five contract tokens. The existing brief's workflow rule still points at `workflow.py`, so the ONE-router invariant remains explicit.

## Result

The cold-seat surface now satisfies the parent's falsifier. The route block is documentation only; it does not add a parallel invoker or alter dispatch/rotate behaviour.
