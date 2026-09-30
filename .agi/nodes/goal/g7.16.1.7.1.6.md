---
id: goal:g7.16.1.7.1.6
mint_id: 27a46a928d99463094cd3b19625e9b01
type: goal
parents:
  - goal:g7.16.1.7.1
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G7.16.1.7.1.6
goal_kind: subgoal
origin: council-loop
scaffold_hash: 5ebd2201fc0280bb
season: 2
seeds: []
status: horizon
tags:
  - templates
title: "G7.16.1.7.1.6: a stood-up post's first turn is a RENDER TOOL CALL whose result is the inline slice"
town: core
---
# goal:g7.16.1.7.1.6

## Why this exists
goal:g7.16.1.7.1 (7a): self-perpetuating's council coverage review of goal:g7.16.1.7 (05:4xZ 09-30, routed by sanctuary-master 08:4xZ) found this target of goal:g7.16.1.7 carried by no leaf: 'A stood-up post's first turn is a TOOL-CALL turn ... that slice IS the tool result'; this leaf carries goal:g7.16.1.7 Falsifier 2. Depends on goal:g7.16.1.7.1.5.

## Target end-state
- A stood-up post's first turn is a tool_use of the one render call; its tool result is the inline slice of the post's linked context docs (live card + active formation line).
- No launch path pastes the brief as a prompt or as hook text.

## Invariants
- The first-turn body is the render, byte for byte; never a copy that can drift.

## Falsifier
1. a dummy-harness stand-up yields a first turn that is a tool_use, and its result is byte-identical to `viewport.py --emit llm` (inline) for that post's links.
2. Negative: zero launch paths in rotate.py / heal.py paste the brief as prompt or hook text (the test enumerates them).

## Out of scope
goal:g7.16.1.7.1.5 · goal:g7.16.1.7.3 (the magic pane)

## Agent Notes
Assigned to **director-general-4**.
