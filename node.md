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
- The engine recognises exactly ONE project marker, `.agi/config.json`, through ONE resolver, `extensions/agi/bin/locations.py`. Measured 05:3xZ 09-30 (Opus refutation pass), the legacy names still resolve in SEVEN places, and each of them either drops the legacy names or calls locations.py:
  - `extensions/agi/bin/locations.py`: :72 the legacy marker names · :82 the prefixed names inside `.agi/` · :86 the `AUTORESEARCH_TREE_PROJECT_ROOT` env var · :162 `_descend` finding `*-tree/` directories
  - `write_guard.py:47` · `model_fence.py:36` · `lib/find-root.sh:48` · `driver.sh:147` · `grid_coverage_check.py:64` · `extensions/agi-bridge/index.ts:24` (CONFIG_NAMES)
- Strings only, updated in the same pass: `extensions/agi/bin/dashboard.py:31,124-125` (a docstring and an error message; it resolves through `metrics.config_path`) and CLAUDE.md's Layout line "(legacy agi-tree.config.json at the root still resolves)".
- The `.hermes` hits are NOT resolver fallbacks: they are `__main__` demo defaults (asciirender.py:243, graph_builder.py:2821, pi_tree_adapter.py:223, query_engine.py:180), a module constant that creates a directory at IMPORT (benchmark.py:30-32), a comment (chains.py:150), and a README (agi-bridge/README.md:33) documenting a fallback index.ts no longer has. The target for them: no directory is created at import, and no home-path demo default remains.

## Invariants
- Nothing is deleted on any host by this leaf: it only stops the engine from resolving the legacy names.
- After this leaf, `locations.py` IS the single resolver: every other place that needs the project root calls it.

## Falsifier
1. A test creates a scratch directory holding only a legacy marker, and EVERY resolver above (locations.find_project_root, write_guard, model_fence, find-root.sh, driver.sh's root step, grid_coverage_check, agi-bridge) refuses to treat it as a project.
2. Negative: `git grep -nE 'autoresearch-tree|agi-tree\.config\.json|AUTORESEARCH_TREE_PROJECT_ROOT' -- extensions CLAUDE.md ':!extensions/agi/tests'` prints 0 hits (test fixtures and history under .agi/nodes are not counted).
## Out of scope
goal:g1.6 (the bin/ rename) · host and GitHub housekeeping from s4 (C1-C5: archive autoresearch-tree, remove host directories), which is the owner's to do by hand.

## Agent Notes
Assigned to **the council** (placement).
