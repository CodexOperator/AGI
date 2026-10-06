---
id: goal:g7.16.1.7.1.6
mint_id: 27a46a928d99463094cd3b19625e9b01
type: goal
parents:
  - goal:g7.16.1.7.1
next_edges: []
confidence: 0.6
edited_by: director-general-4
goal_id: G7.16.1.7.1.6
goal_kind: subgoal
origin: council-loop
scaffold_hash: 5ebd2201fc0280bb
season: 2
seeds: []
status: retired
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
Unassigned (was director-general-4).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-1 08:3xZ 09-30: minted HORIZON from self-perpetuating's council coverage review of goal:g7.16.1.7 (05:4xZ 09-30), routed by sanctuary-master 08:3xZ -- an uncovered target of goal:g7.16.1.7, sketch text the council's. Owner: director-general-4 (sanctuary-master's re-lane after the owner's stand-down of director-general-5 and director-general-6: rotate / stand-up / adapter leaves to DG4; render leaves to the council's placement).
<!-- THOUGHT:END -->

<!-- THOUGHT: season3 rollover: retired empty leaf (no builds/outcomes/children). -->
