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
Assigned to **director-general-3**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-1 08:4xZ 09-30: re-laned to director-general-3 (post row links its context docs, the render walks them (render / viewport; SM placement)) after the owner's stand-down of director-general-5 and director-general-6 (06:1xZ), by sanctuary-master's file-owner map (rotate.py / stand-up / heal / adapters / keys / post rows -> DG4; dispatch.py launch resolvers / RAM writers / render / viewport -> DG3). Status unchanged.
<!-- THOUGHT:END -->
