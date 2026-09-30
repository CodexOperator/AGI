---
id: goal:g7.16.1.8
mint_id: 8eede4c80072443da617fa1b94649b4a
type: goal
parents:
  - goal:g7.16.1
next_edges: []
confidence: 0.6
edited_by: belam
goal_id: G7.16.1.8
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: b013e4b4d03de2f1
season: 2
seeds: []
status: horizon
tags:
  - sanctuary
  - init
  - standup
  - council-loop
title: "G7.16.1.8: one init pass + one captive stand-up script walk a user through a sanctuary box, every value read from the graph"
town: core
---
# goal:g7.16.1.8

## OWNER 2026-09-30 00:1xZ, verbatim (Prime pane)
"Sweet go ahead and do the changes and add it in then symlink it like the rest. Then we will need an ini pass and ideally one simple script that guides a user through sanctuary standup via one captive flow."

## Why this exists
goal:g7.16.1 (the council loop): a next-bundle candidate for the council to place, minted by the Prime. The first half of the owner line (the guard into the graph, symlinked like the other global handles) is done by the Prime on goal:g7.16.1.7's guard target; this leaf is the second half. Today standing a sanctuary box up is spread across QUICKSTART.md, guard-init.sh (root, five layers), crons.py apply, the envfile check, provisioning, and a hand-made /etc/sanctuary-guard/box; nothing walks a new user through it end to end, and every value lives in a different file.

## Target end-state
- ONE init pass reads every setting the stand-up needs from the graph (config:guard, config:crons, config:posts, the .env check) and reports, per step, done / missing / needs-the-user -- idempotent, safe to re-run.
- ONE simple script is the captive flow a user runs on a fresh box: it asks only what it cannot derive (box name, the user's accounts and keys), shows each step before it acts, runs the init pass, and ends with the box verified (guard --status all ok, crons applied, the node count readable).
- Nothing the flow writes names a host, an address or hardware; the box is named by its box name.

## Invariants
- The flow never applies a root step without showing it first and getting a yes.
- Re-running the flow on a finished box changes nothing (every step reports "already done").

## Falsifier
1. On a box that is already stood up, the flow run end to end prints "already done" for every step and exits 0.
2. Negative: zero stand-up steps documented only in prose (QUICKSTART.md, GUARD.md) that the flow does not run or check.

## Out of scope
goal:g7.16.1.7 (spawn/rotate templates; the guard's build nodes) · per-post user accounts and stricter key templates (season 3).

## Agent Notes
Assigned to **the council** (placement).
