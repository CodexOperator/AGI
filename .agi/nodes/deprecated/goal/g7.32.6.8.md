---
id: goal:g7.32.6.8
mint_id: b73463a2a6fe4a1e93fd36c25c76bb35
type: goal
parents:
  - goal:g7.32.6
next_edges: []
confidence: 0.85
edited_by: director-helper
goal_id: G7.32.6.8
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: 47655e1fcb0d11af
season: 2
spawn_gate: bypassed
status: complete
tags:
  - engine
  - messaging
  - crons
thought_session: helper-nopi-stopline14-20260928
title: "G7.32.6.8: crons.py dm_sync KNOWN_JOB wired to interval cell"
town: core
---
<!-- BODY:BEGIN -->
# goal:g7.32.6.8

## Why this exists

**Parent `goal:g7.32.6`.** Production crons residue: `crons.py` must know `dm_sync` as a KNOWN_JOB and schedule `send.py dm-sync` using `values.dm.sync_interval_min` (via dm_engine) when the job omits every_mins.

## Target end-state

- `dm_sync` in `KNOWN_JOBS`.
- Renderer emits `python3 send.py dm-sync` on the interval cell when enabled.
- Cadence stays **disabled** in live geometry until Belam/DE flips it (no surprise live tick).

## Invariants

- Does **not** open `goal:g7.31.6` / `goal:g7.32.5`.
- Does not enable crons.md dm_sync without Belam.
- NO pi under OWNER FULL STOP.

## Falsifier

1. `crons.py` source carries `dm_sync` in KNOWN_JOBS and imports/uses `dm_engine` for the interval fallback.
2. `dm_engine.sync_schedule_expr` honors `values.dm.sync_interval_min` in [1,3].

## Out of scope

- Live crontab apply / geometry enable.
- Parked g7.32.5 / g7.31.6.

## Agent Notes

Assigned to **director-helper** under OWNER FULL STOP (NO pi).

NO-PI stopline14: dm_sync in KNOWN_JOBS; renderer uses dm_engine.sync_interval_min fallback; cadence not enabled in geometry (Belam/DE)

<!-- THOUGHT: season3 rollover: complete goal not carried into s3; builds reparented to umbrella. -->
