---
id: goal:g7.11
mint_id: 5fe1c52dbfe24c41b1109721f74afe01
type: goal
parents:
  - goal:g4
next_edges: []
confidence: 0.9
edited_by: belam
goal_id: G7.11
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: a644896ab3152b0e
season: 2
seeds: []
status: active
tags:
  - goal
  - subgoal
thought_session: g1-g7-rewrite-2026-09-19
title: "G7.11: Merge-ups use custom git scripts — signing, key ownership, rotation; authenticity chain exists (incomplete); batch verify 10-15m to core/season2/main"
town: core
---
# goal:g7.11

## Why this exists

Parent `goal:g7` (nothing silently lost). Owner 2026-09-19: merge-ups use custom git scripts (signing, key ownership, rotation); a cryptographic authenticity chain exists but is incomplete/insecure (harden in redesign); each batch merge to `core/season2/main` runs an advanced verification script (~10–15 minutes).

## Owner bank (verbatim excerpts, 2026-09-19)

From the graph-handoff bank (`goal:g1.18`):

> Also for merg ups, we are using our custom git scripts right? They take care of things like signing each one and also verifying key ownership, rotation, etc. If you check git history you will see a cryptographic chain of authenticity in there somewhere. It's incomplete and insecure, but it does exist. Hardening comes later during the redesign

From the seat/brief bank (`goal:g7.165`):

> We have an advanced verification script that takes 10-15 minutes per run that we run during each batch merge to core/season2/main.

## Target end-state

- Every Belam/director merge-up to the town trunk uses the custom git scripts (sign + key ownership + rotation checks), never raw `git merge` alone.
- Authenticity chain is present on history today; hardening is a redesign follow-on, not a silent drop.
- Batch merge to `core/season2/main` does not land without the advanced verification script completing green (or an explicit owner waiver node).

## Invariants

- Residues-only batches may merge while the next batch runs; red blockers must be fixed in-batch first (standing Texas two-step rule).
- Verification is part of "nothing silently lost," not optional polish.

## Falsifier

1. A merge-up path that bypasses the custom scripts fails a gate (or is impossible from the sanctioned workflow).
2. History still shows the authenticity chain markers after a practice merge-up.
3. A merge to `core/season2/main` without the ~10–15m verify run is rejected or recorded as a red blocker.

## Related

- `goal:g1.18`, `goal:g7.165`, redesign hardening (later).
# goal:g7.11
