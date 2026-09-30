---
id: goal:g4.21
mint_id: 018f992109df495fafbcdf2714c674e5
type: goal
parents:
  - goal:g4
next_edges: []
confidence: 0.7
edited_by: self-perpetuating
goal_id: G4.21
goal_kind: subgoal
origin: goals-doc
scaffold_hash: bba99061ff57acd7
season: 2
seeds: []
status: active
tags:
  - s-goal-retirement
  - from-s4
  - legacy
  - resolver
title: "G4.21: the engine resolves ONE project marker -- no autoresearch-tree / agi-tree legacy marker and no .hermes fallback, so a leftover legacy directory is never a live project (from goal:s4)"
town: core
---
# goal:g4.21

## OWNER 2026-09-30 01:2xZ, verbatim (relayed by alive gen 3, belam's post-reboot owner-task)
"All S goals should have been retired in favor of nested sub sub goals or whatever that fit under the umbrella goals."

## Why this exists
goal:g4 (elegance): goal:s4 ("retire the legacy directories and repos") was retired on the owner's line above. It was measured at 02:1xZ 09-30 (self-perpetuating, read-only survey). agi-tree was disarmed and archived, and C6 (tracked gitnexus skills) was untracked in 4b4a62288. The C1-C5 host and GitHub items cannot be seen from the repo. What stays open is on the ENGINE side: the resolvers still accept the legacy project markers, so a leftover legacy directory would still be picked up as a live project, which is the hazard agi-tree had. s4's own rule ("disarm first") applied from the engine side defuses that without deleting anything on any host.

## Target end-state
- The engine recognises exactly ONE project marker, `.agi/config.json`. `autoresearch-tree.config.json` (extensions/agi-bridge/index.ts:24, extensions/agi/bin/locations.py:72, bin/dashboard.py:31,125) and the root `agi-tree.config.json` no longer resolve.
- No home-directory `.hermes` fallback remains (extensions/agi/src/agi_algos: asciirender.py, benchmark.py, graph_builder.py, pi_tree_adapter.py, query_engine.py; chain_engine/chains.py; agi-bridge/README.md).
- CLAUDE.md's Layout line drops "(legacy agi-tree.config.json at the root still resolves)".

## Invariants
- Nothing is deleted on any host by this leaf: it only stops the engine from resolving the legacy names.
- `bin/locations.py` stays the single resolver.

## Falsifier
1. A test creates a scratch directory holding only a legacy marker, and `locations.find_project_root` from inside it does not return it.
2. Negative: `git grep -nE 'autoresearch-tree\.config\.json|agi-tree\.config\.json|\.hermes' -- extensions CLAUDE.md` prints 0 live code hits (history under .agi/nodes is not counted).

## Out of scope
goal:g1.6 (the bin/ rename) · host and GitHub housekeeping from s4 (C1-C5: archive autoresearch-tree, remove host directories), which is the owner's to do by hand.

## Agent Notes
Assigned to **the council** (placement).
