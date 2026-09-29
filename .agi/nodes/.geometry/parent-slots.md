---
id: config:parent-slots
mint_id: 7c3e9a1b2d4f4058a6b8c0d1e2f30405
type: config
parents:
  - goal:g7.31.3.3
next_edges: []
edited_by: director-helper
season: 2
status: active
tags:
  - engine
  - spawn
  - geometry
title: "Committed parent-slot definitions under each post (g7.31.3.3.1)"
town: core
---
# config:parent-slots

## Why this exists

**Parent `goal:g7.31.3.3` / leaf `goal:g7.31.3.3.1`.** Owner design: concurrency×parallel
become the count of pre-set parent post slots under each post in `.geometry`.
This file holds the **committed slot definitions** only.

## Invariants

- Live occupancy is NOT stored here. Occupancy SoT is the local runtime file
  `.agi/sessions/parent-occupancy.json` (`goal:g7.31.3.3.2` / `parent_slots.occupy`).
- Forbidden as SoT on a committed slot row: occupied, occupant, occupied_by, pid,
  live, runtime, session_id, window.
- Slot ids are `parent-0` .. `parent-(N-1)` where N = spawn.concurrency × spawn.parallel
  (absent cells read as 1). Sample rows below seed the contract for stop-line posts.

## parent_slots

parent_slots:
  director-helper:
    - {"id": "parent-0", "kind": "parent"}
  director-engine:
    - {"id": "parent-0", "kind": "parent"}
  director-belam:
    - {"id": "parent-0", "kind": "parent"}
  director-thought:
    - {"id": "parent-0", "kind": "parent"}
  belam:
    - {"id": "parent-0", "kind": "parent"}

## Agent Notes

Landed NO-PI by director-helper 2026-09-28 (stopline11): defs-only geometry +
`extensions/agi/bin/parent_slots.py` reader; occupancy sibling owns the runtime file.
