---
id: goal:g7.26
mint_id: 6058821da96c417e949b9115e01eb35d
type: goal
parents:
  - goal:g7
next_edges: []
confidence: 0.9
edited_by: belam
goal_id: G7.26
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: 527f96977cacb583
season: 2
seeds: []
status: active
tags:
  - goal
  - subgoal
thought_session: g1-g7-rewrite-2026-09-19
title: "G7.26: Post briefs are self-sufficient custom instructions (spawn injects brief/worktree/pin/key; after-rotate dump)"
town: core
---
# goal:g7.26

## Why this exists

Parent `goal:g17` (seat / post system). Owner 2026-09-19: post briefs must be self-sufficient custom instructions, not "reference these instructions + pile." Spawn must stand up worktree + pin + key + brief injection. After-rotate dump matters for pi (and later in-house websocket dataflow).

## Owner bank (verbatim, 2026-09-19)

> I was wonering if we could assign the direct briefs that every post gets to the custom instructions of each bot directly instead of saying 'reference these instructions' and then a bunch of other stuff. Those are supposed to be self-sufficient. If you feel they lack anything to be complete by all means modify them in-graph using your key through the write function. Everything is a node. Always. If there's a doc or config that is not a node, then it needs to be a node. If there's a script file with no node, that especially needs to be a node. We have an advanced verification script that takes 10-15 minutes per run that we run during each batch merge to core/season2/main. But this way when some bot uses the spawn function to stand up a post they automatically get a fresh worktree and correct pin and key assignment, as well as the correct brief is automatically added to that bot's individual instructions. We also have an after-rotate feature to dump some relevant data into a fresh rotation. This isn't as relevant for grok bots that auto-rotate, but super relevant for pi posts among others. Especially will be relevant once we bring all model calls in-house using raw websocket connections and we manage all pieces of the dataflow outside the actual inference matrix multiplications - for now.

## Target end-state

- Every post brief is the bot's custom instructions body (complete, self-sufficient).
- Gaps are fixed in-graph via `write.py` (not external doc drift).
- `spawn` for a post yields: fresh worktree, correct pin, correct key assignment, brief written into that bot's individual instructions.
- `after-rotate` dumps relevant session data into the fresh rotation (required for pi; optional/no-op-ok for auto-rotating grok-bot seats until in-house websocket dataflow).

## Invariants

- Briefs live as nodes; edits go through the unified write path.
- Spawn is the only sanctioned way to stand up a post with pin/key/worktree/brief.
- After-rotate is a graph-declared feature, not a harness side-effect.

## Falsifier

1. A newly spawned post's custom instructions equal the brief node body (byte-stable after normalize), with no "see also / reference these" stub.
2. Spawn without a brief node fails closed.
3. After-rotate on a pi post leaves a dump artifact reachable from the new rotation's graph context; on grok-bot auto-rotate it is either applied or explicitly skipped with a recorded reason.

## Related

- Cross-cut: `goal:g4.20` (everything is a node), `goal:g7.11` (batch verify on merge-up), `goal:g1.18` (graph-native handoffs).
# goal:g7.26
