---
id: goal:g7.31.3.3.4
mint_id: 43c0d95304294e3e8180b6cf4c5dacb7
type: goal
parents:
  - goal:g7.31.3.3
next_edges: []
confidence: 0.85
edited_by: director-belam
goal_id: G7.31.3.3.4
goal_kind: subgoal
heading_level: 6
origin: goals-doc
scaffold_hash: a1dbb64622876c75
season: 2
seeds: []
status: active
tags:
  - goal
  - subgoal
  - engine
  - spawn
  - rotate
thought_session: belam-stop-line-nopi-20260928
title: "G7.31.3.3.4: Refusal writes named row + one send-reply to requesting post"
town: core
---
# goal:g7.31.3.3.4

## Why this exists

**Parent `goal:g7.31.3.3`.** Owner addition: a refusal writes the row by name AND sends one reply to the requesting post via the send reply route (graph-found); cap one reply per failed request.

## Target end-state

- Refusal stamps the named row and triggers exactly one reply through the send reply route.
- Cap: one reply per failed request (no reply storms).

## Invariants

- Sibling slices under `goal:g7.31.3.3` own their own falsifiers — do not widen this leaf.
- Does not open `goal:g7.31.6` / `goal:g7.32.5` (board parked); stays under stop-line `g7.31.3`.

## Falsifier

1. Induced refusal: row updated by name + exactly one reply delivered to requesting post.
2. Negative: zero multi-reply storms for a single failed request.

## Out of scope

- Other `goal:g7.31.3.3.*` siblings.
- Messaging half of the same owner message (`goal:g7.32.5`, helper / parked).

## Agent Notes

Assigned to **director-belam**. Director-direct under OWNER FULL STOP (NO pi).
