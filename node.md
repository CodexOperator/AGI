---
id: goal:g1.1
mint_id: de7aafc73c54435885fd02b96e92bcc6
type: goal
parents:
  - goal:g1
confidence: 1.0
edited_by: season.py
goal_id: G1.1
goal_kind: subgoal
heading_level: 3
origin: goals-doc
season: 1
seeds: []
status: horizon
tags:
  - goal
  - subgoal
thought_session: season
title: "G1.1: An agent should need only the graph to orient"
---
**Recon happens in the graph, not in the filesystem.** Today a kid arrives with
a rendered map and then reads files anyway, because the map cannot answer
follow-up questions. Every one of those reads is motion spent re-deriving
context the graph already holds.

What has to exist: an agent can **move** through the graph from where it was
dropped — step to a neighbour, pull a snapshot of an adjacent region, widen to
the enclosing map — without opening a source file and without a second spawn.
The level-3 nodes make this newly plausible: a node already carries
`payload_ref` and a derived contract, so "what does this module take and
promise" is answerable from the graph alone.

The measurable version, and the reason this is worth doing: kids dropped from
11–13 tool calls to 5–7 when the map was embedded in the prompt. The target is
the same curve applied to follow-up reads — an agent that navigates instead of
grepping. Falsifier: if agents given navigation still read the same number of
files, the graph is not carrying the context it claims to.

Shares its substrate with G9.4 — the viewport a human pans and the region an
agent requests are the same query at different resolutions. Build them as one
mechanism with two front-ends, not two renderers that drift.