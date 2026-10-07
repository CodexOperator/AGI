---
id: goal:g7.16.1.7.2.6
mint_id: 9fe6f9a6681f4084b6b77b4b43cf58ea
type: goal
parents:
  - goal:g7.16.1.7.2
next_edges: []
confidence: 0.6
edited_by: director-general-4
goal_id: G7.16.1.7.2.6
goal_kind: subgoal
origin: council-loop
scaffold_hash: 39f8cb9f496fce7b
season: 2
seeds: []
status: horizon
tags:
  - templates
title: "G7.16.1.7.2.6: every harness ships an ADAPTER MAP onto write · wake · render · stand-up"
town: core
---
# goal:g7.16.1.7.2.6

## Why this exists
goal:g7.16.1.7.2 (7b): self-perpetuating's council coverage review of goal:g7.16.1.7 (05:4xZ 09-30, routed by sanctuary-master 08:4xZ) found this target of goal:g7.16.1.7 carried by no leaf: 'The harness adapter map is the spine ... no `send` verb, and no verb exists for one harness only'. Depends on goal:g7.16.1.6, goal:g7.32.6 and goal:g7.16.1.7.2.1.

## Target end-state
- Each harness adapter under extensions/agi/bin/adapters (Claude Code, pi, and the copilot and grok adapters) ships a map of its actions and hooks onto the four engine verbs: write · wake · render · stand-up.
- A message is a write (goal:g7.32.6): no `send` verb in any map.

## Invariants
- No engine verb exists for one harness only.

## Falsifier
1. a test over extensions/agi/bin/adapters resolves all 4 verbs for every shipped map.
2. Negative: zero `send` verbs and zero single-harness verbs across the maps.

## Out of scope
goal:g7.25 (third-party adapters) · goal:g7.32.6

## Agent Notes
Unassigned (was director-general-4).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-1 08:3xZ 09-30: minted HORIZON from self-perpetuating's council coverage review of goal:g7.16.1.7 (05:4xZ 09-30), routed by sanctuary-master 08:3xZ -- an uncovered target of goal:g7.16.1.7, sketch text the council's. Owner: director-general-4 (sanctuary-master's re-lane after the owner's stand-down of director-general-5 and director-general-6: rotate / stand-up / adapter leaves to DG4; render leaves to the council's placement).
<!-- THOUGHT:END -->
