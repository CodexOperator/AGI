---
id: goal:g4.18.2.1
mint_id: 70fc9c0443ec43bc89f18b769187a114
type: goal
parents:
  - goal:g4.18.2
next_edges: []
confidence: 1.0
edited_by: alive
goal_id: G4.18.2.1
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: 38059e6af16cef9f
season: 2
seeds: []
status: active
tags:
  - goal
  - docs
  - subgoal
thought_session: g1-g7-rewrite-2026-09-19
title: "G4.18.2.1: the docs say what the tree does now -- one test fails on any retired name the docs still teach as live"
---
# goal:g4.18.2.1

## OWNER ask 2026-09-04, as carried verbatim on goal:s33 (goals-doc)
"Owner ask, 2026-09-04. After loop L1 (L1.08 to L1.11) the docs drifted: QUICKSTART.md still describes pre-L1 state (CC-only dispatch, iter-NNN numbering, kits, render-context), CLAUDE.md and skills/agi/SKILL.md carry rules for things that no longer exist or now exist (claude-code harness real, loop-scoped ids real, build-site cohort retired, evidence gate on the commit path, spawn.parallel semantics, workspace weekly budget). Commit to one sweep: every claim in QUICKSTART.md, CLAUDE.md, skills/agi/SKILL.md and HANDOFF.md section 5 is checked against the tree and corrected or deleted, with the commit citing what was stale. Falsifier: a test that greps the docs for retired names (render-context.py, payloads/, grid.py checkout as a live command, context/kits) and fails on any hit outside a sentence that marks it retired."

## OWNER 2026-09-30 00:5xZ, verbatim (relayed by belam to the council)
"All S goals should have been retired in favor of nested sub sub goals or whatever that fit under the umbrella goals."

## Why this exists
goal:g4.18.2 (skills for every engine flow + the doc trim): this is the doc trim's truth check, renumbered here from goal:s33 by the council (alive, 02:1xZ 09-30) on the owner line above. Measured 02:1xZ 09-30 by alive: QUICKSTART.md:108 still draws `render-context.py` as a live driver stage (retired L1.05: INJECTION.md is written by inject.py via briefing.py); the four retired names (render-context.py 4 · payloads/ 2 · grid.py checkout 4 · context/kits 2 hits across QUICKSTART.md, CLAUDE.md, skills/agi/SKILL.md) are mostly inside sentences that mark them retired, but no test tells the two apart; the sweep's hypotheses (hypothesis:a00-abd94427-d2294b, hypothesis:a01-49aa1742-c5a5d0) never produced the test.

## Target end-state
- ONE test reads the teaching docs (QUICKSTART.md, CLAUDE.md, skills/*/SKILL.md) and FAILS on any retired name that appears outside a sentence marking it retired; the retired-name list is ONE config cell, so the next retirement is a row, never a code change.
- Every claim the test flags is corrected or deleted in the commit that makes it green, the commit citing what was stale.
- Through vision:alive: the docs are the system's own account of itself, re-measured every run, so a successor never learns a retired path as live.

## Invariants
- A doc that names a retired thing says it is retired in the same sentence (CLAUDE.md's never-lines stay legal).
- The retired-name list has ONE home (a config cell); the test reads it.

## Falsifier
1. The test passes on the tree and fails when `render-context.py` is re-added to QUICKSTART.md as a live stage.
2. Negative: `git grep -n render-context.py -- QUICKSTART.md` returns only lines that mark it retired.

## Out of scope
goal:g4.18.2 (the skills themselves) · goal:g4.20 (every doc gains a node) · goal:s33 is RETIRED as an id (renumbered here), never reused.

## Agent Notes
Assigned to **the council** (placement; the build goes to the directors by their own split).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Renumbered goal:s33 -> goal:g4.18.2.1 (mint_id 70fc9c04 kept) by the council, alive writer, on the owner line "All S goals should have been retired in favor of nested sub sub goals or whatever that fit under the umbrella goals." Still open, measured against the bytes (QUICKSTART.md:108; no docs-truth test), so renumbered rather than retired: the node keeps its history and its two hypotheses. Parent moved goal:g6 -> goal:g4.18.2, the doc trim it belongs to. References re-pointed in the same commit: 2 hypothesis parents + their prose, 1 experiment line. The old body was one quoted owner ask in Agent Notes; it is now an OWNER section, verbatim, and the body follows the goal format. Prior THOUGHT ("Minted by the L1.08 director at the owner request; standalone because it spans every doc") is kept in the grid history.
<!-- THOUGHT:END -->
