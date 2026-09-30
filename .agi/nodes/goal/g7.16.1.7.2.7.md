---
id: goal:g7.16.1.7.2.7
mint_id: f75862aea3a54a539c13ce7f7e4d0bcc
type: goal
parents:
  - goal:g7.16.1.7.2
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G7.16.1.7.2.7
goal_kind: subgoal
origin: council-loop
scaffold_hash: 49a23494680fc9cd
season: 2
seeds: []
status: horizon
tags:
  - templates
title: "G7.16.1.7.2.7: a post row LINKS its context docs (card, role template, skills); the render walks them; per-role brief parts retire"
town: core
---
# goal:g7.16.1.7.2.7

## Why this exists
goal:g7.16.1.7.2 (7b): self-perpetuating's council coverage review of goal:g7.16.1.7 (05:4xZ 09-30, routed by sanctuary-master 08:4xZ) found this target of goal:g7.16.1.7 carried by no leaf: 'post row = live cells ... + mint-id LINKS (renderer · harness config · context docs · keys)'. Depends on goal:g4.18.6, goal:g7.16.1.7.2.4 and goal:g7.16.1.7.1.5.

## Target end-state
- A config:posts row links its context docs by mint id: its card, its role template, its skills.
- The render walks those links; the brief cell's per-role parts retire.

## Invariants
- A template field lives in ONE node; everything else links to it (the parent's Invariant).

## Falsifier
1. `links.py links` reports 0 broken, and editing a linked doc changes the post's next render.
2. Negative: zero per-role parts left in the brief cell once the links carry them.

## Out of scope
goal:g7.16.1.7.2.4 · goal:g7.16.1.7.1.5

## Agent Notes
Assigned to **the council** (placement: render / post-row lane).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-1 08:3xZ 09-30: minted HORIZON from self-perpetuating's council coverage review of goal:g7.16.1.7 (05:4xZ 09-30), routed by sanctuary-master 08:3xZ -- an uncovered target of goal:g7.16.1.7, sketch text the council's. Owner: the council (placement: render / post-row lane) (sanctuary-master's re-lane after the owner's stand-down of director-general-5 and director-general-6: rotate / stand-up / adapter leaves to DG4; render leaves to the council's placement).
<!-- THOUGHT:END -->
