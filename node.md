---
id: goal:g13.3
mint_id: a125ad25c35e4648a0b8fb1d2eb9a9c1
type: goal
parents:
  - goal:g4
next_edges: []
confidence: 0.9
edited_by: belam
goal_id: G13.3
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: cd5cf0bffb792d08
season: 2
seeds: []
status: active
tags:
  - goal
  - subgoal
thought_session: g1-g7-rewrite-2026-09-19
title: "G13.3: Everything is a node — docs, configs, and especially scripts without nodes must gain them"
town: core
---
# goal:g13.3

## Why this exists

Parent `goal:g13` (one read/write path). Owner 2026-09-19: everything is a node — docs, configs, and especially scripts without nodes must gain them. Ties to spawn injecting briefs and in-graph brief edits.

## Owner bank (verbatim excerpt, 2026-09-19 — full text also on goal:g17.15)

> Everything is a node. Always. If there's a doc or config that is not a node, then it needs to be a node. If there's a script file with no node, that especially needs to be a node. … when some bot uses the spawn function to stand up a post they automatically get a fresh worktree and correct pin and key assignment, as well as the correct brief is automatically added to that bot's individual instructions.

## Target end-state

- Every operational doc, config, and script under the engine/graph tree has a corresponding node (or is explicitly listed as non-graph ephemeral with a gate).
- Scripts without nodes are treated as defects found by scan, not style nits.
- Brief/doc edits that change agent behavior go through `write.py`, not side-channel file edits.

## Invariants

- One read/write path remains the only sanctioned mutation of operational content.
- A script that affects dispatch/workflow/spawn/send without a node fails the batch verify gate (`goal:g7.11`).

## Falsifier

1. A scan lists every `extensions/agi/bin/*.py` (and declared config/doc paths) with either a node id or an explicit `ephemeral:` exemption.
2. Editing a brief node via `write.py` changes the next spawn's injected instructions without a second out-of-band copy step.
3. Adding a new script without a node fails the 10–15m advanced verification run used on merge to `core/season2/main`.

## Related

- `goal:g17.15`, `goal:s35` (schemas are nodes), `goal:g7.11`.
# goal:g13.3
