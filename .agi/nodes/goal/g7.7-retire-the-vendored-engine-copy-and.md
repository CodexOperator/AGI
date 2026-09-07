---
id: goal:g7.7
mint_id: 6b02b12853164a169b2ea71dd1748dc7
type: goal
parents:
  - goal:g7
confidence: 1.0
edited_by: season.py
goal_id: G7.7
goal_kind: subgoal
heading_level: 3
origin: goals-doc
season: 1
seeds: []
status: horizon
tags:
  - goal
  - subgoal
thought_session: season
title: "G7.7: Retire the vendored engine copy and the last loader path bug"
---
Two carried defects with one root: `agi-tree/src/` holds project-local copies of
`graph_core`, `chain_engine`, `renderers`, `schema_registry`, `embeddings` and
`environment_indexers`, and the documented override convention gives them
precedence over the engine's own. The project therefore runs on a stale copy
that predates `sqlite_backend.py` — which is how a snapshot came to crash
mid-corpus this session (H0g).

This is H0/H0b's defect class arriving through the `src/` door, and L9 states
the rule it breaks: **the engine must never be vendored.** Retire the directory
deliberately — the historical `exp-*.py` scripts import from it, so verify
before deleting. Absorbs **H0h** and **H5** (the R11 loader path-safety bug,
which lives in the same code).