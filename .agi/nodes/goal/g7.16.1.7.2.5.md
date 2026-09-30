---
id: goal:g7.16.1.7.2.5
mint_id: 4d13c2e8cb8a40d1abe7a078fc85053e
type: goal
parents:
  - goal:g7.16.1.7.2
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G7.16.1.7.2.5
goal_kind: subgoal
origin: council-loop
scaffold_hash: 74aa331154f38d34
season: 2
seeds: []
status: horizon
tags:
  - templates
  - spawn
  - rotate
  - council-loop
title: "G7.16.1.7.2.5: a formation is a template with null link rows -- ONE activation writes it into .geometry, fills each link at stand-up, and the posts self-spawn in the background"
town: core
---
# goal:g7.16.1.7.2.5

## Why this exists
goal:g7.16.1.7: the owner, verbatim there: "So formations are templates containing empty link rows pointing to "null" that are set as part of formation activation, which writes the template into .geometry while filling in the link rows dynamically at stand up" and "All I or you need is to activate the right formation template and chain the appropriate harness template". Shape condition (self-perpetuating lens 23:5xZ): COLD-START -- a fresh clone + ONE formation activation = a running formation, nothing else typed. Absorbs by name goal:g6.36 (rotate driven) where it concerns stand-up.

## Target end-state
- A formation template lists its posts as link rows pointing at null; config:formations 'set active <formation>' (one call) fills each row from the post template + customizations and writes the formation into .geometry.
- Heal / rotate stand the filled posts up in the background, with no model act and no per-post command.

## Invariants
- Activation is one call; deactivation of the previous formation happens in the same call.

## Falsifier
1. COLD-START: in a throwaway clone, one activation of a two-post test formation yields two post rows with filled links and two launch records (dummy scopes), nothing else typed.
2. Negative: the activation path contains no hand-edited post row (every row write goes through write.py).

## Out of scope
goal:g7.16.1.7.2.4 · goal:g7.16.1.7.1.4 · the magic pane system (after this bundle)

## Agent Notes
Assigned to **director-general-4**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-1 08:4xZ 09-30: re-laned to director-general-4 (formations as templates, one activation (stand-up)) after the owner's stand-down of director-general-5 and director-general-6 (06:1xZ), by sanctuary-master's file-owner map (rotate.py / stand-up / heal / adapters / keys / post rows -> DG4; dispatch.py launch resolvers / RAM writers / render / viewport -> DG3). Status unchanged.
<!-- THOUGHT:END -->
