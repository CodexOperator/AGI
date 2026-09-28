---
id: goal:g7.33.18.2
mint_id: 0d397c449f39432495e94032f47dcd30
type: goal
parents:
  - goal:g7.33.18
next_edges: []
confidence: 0.7
edited_by: director-engine
goal_id: G7.33.18.2
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: 35b9a6a1d03c73a6
season: 2
seeds: []
spawn_check: unverified
spawn_check_reason: schema 'goal' is discriminated on 'goal_kind', which this node does not set
status: active
tags:
  - local-maxxing
  - engine
title: "G7.33.18.2: ONE idempotent installer -- dry-run by default, sized from the box's MemTotal/swap, every before-value recorded and restored on failure (assigned: director-engine)"
town: core
---
# goal:g7.33.18.2

# goal:g7.33.18.2

WORLD-AFTER: ONE idempotent installer renders goal:g7.33.18.1's templates sized by goal:g7.33.18's SIZING from the box's own MemTotal/swap, and installs them: DRY-RUN BY DEFAULT (prints the plan: path, before-value, after-value), records every before-value, restores them all on any failure, needs sudo only for the system pieces, and a second run changes nothing.

ACCEPTANCE: in a tmp-root fixture (never the live box): dry-run writes nothing; a real run against the tmp root writes every piece; a second run is a no-op; an injected failure mid-install restores every before-value byte-for-byte; the sizing rows reproduce local-town's measured numbers from its MemTotal/swap.
