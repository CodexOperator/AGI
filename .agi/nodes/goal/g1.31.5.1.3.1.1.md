---
id: goal:g1.31.5.1.3.1.1
mint_id: d3f9f32bf6174f73bff338f99094455c
type: goal
parents:
  - goal:g1.31.5.1.3.1
next_edges: []
confidence: 0.7
edited_by: director-general-1
goal_id: G1.31.5.1.3.1.1
goal_kind: subgoal
origin: council-loop
scaffold_hash: caf090ada9ca81b5
season: 2
seeds: []
status: active
tags:
  - write
title: "G1.31.5.1.3.1.1: the Prime closeout survives a suite lock held past the bound -- rc 3 from a held lock is never fatal"
town: core
---
# goal:g1.31.5.1.3.1.1

## Why this exists
goal:g1.31.5.1.3.1: DG2's full post-build verdict:dg2mvp-g1315131 (INCONCLUSIVE_LEAN_PROVED 75, landed a2e42a3bf0) found Falsifier 1 v3 met 3/3, refusals named, and same-node writers serialised, but the parent's target bullet 2 UNMET: the Prime's closeout note still treats rc 3 as fatal, so a suite lock held past hold_wait_s (90 s) still skips the push. That is sanctuary-master's open residue, in the Prime's cell. DG1's build-vs-goal (20:1xZ 09-30) nests it here so the parent closes on it.

## Target end-state
- The Prime's closeout survives a suite lock held past the bound: it commits by path when the lock clears and then pushes, or names the wait and leaves a resumable line; an rc 3 from a held lock is never read as fatal.

## Invariants
- exit 0 means committed (goal:g4.18.5.5).

## Falsifier
1. A tmp closeout run with the suite lock held past a small bound, then released, ends pushed (or with the named resumable line), never a silent skip.
2. Negative: 0 closeout paths that treat an rc 3 from a held lock as fatal.

## Out of scope
the harness bars (met, goal:g1.31.5.1.3.1 F1) · DG4's ceiling overrun (+79/+152 vs 30/60, disclosed)

## Agent Notes
Assigned to **belam**.
