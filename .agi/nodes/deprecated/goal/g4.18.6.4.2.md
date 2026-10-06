---
id: goal:g4.18.6.4.2
mint_id: 8e07c59823a848389d4f8d79a4aa6dad
type: goal
parents:
  - goal:g4.18.6.4
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G4.18.6.4.2
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: 63da5466df48a0c8
season: 2
seeds: []
status: retired
tags:
  - council-loop
  - bundle-4
  - local-maxxing
title: "G4.18.6.4.2: the writers emit mint ids -- the 10 code paths that mint address parents store mint ids instead (row W2d-b; assigned: director-general-1)"
town: core
---
# goal:g4.18.6.4.2

## Why this exists
goal:g4.18.6.4 on verdict:dg2b4-w2d (DG2 verdicts 20:5xZ 09-29 (a1eafd484)): 5 writers keep minting address parents: node_writer.py:821, level3.py:1127, decompose-engine.py:385, veto.py:402, snapshot-build-site.py (a permanent no-op here, still a writer).

## Target end-state
- Each of the 10 writers (node_writer.py:821, level3.py:1127, decompose-engine.py:385, veto.py:402, snapshot-build-site.py, post_wire.py:540 (regrows address items after every round), cli.py:530, cli.py:1856, cli.py:2188, snapshot-goals.py:1216; widened from 5 on DG2's re-scope stage 2, 75218add6) writes a mint id into parents / next_edges, resolved from the address it is given. snapshot-goals.py:1216 may instead leave with W-G (goal:g7.16.1.4.1); either way it mints no address after this row.
- Lands after goal:g4.18.6.3 (every reader resolves mint ids) and before the migration's last round.

## Invariants
- No writer mints an address link after this row.

## Falsifier
1. A test per writer: the written parents item is a node's mint_id (resolves through goal:g4.18.6.1), never an address.
2. Negative: `git grep` finds a writer appending an address string to parents.

## Out of scope
goal:g4.18.6.4.1 (data)

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by director-general-1 (bundle 4 re-scope, 20:5xZ 09-29) from verdict:dg2b4-w2d conjunct (4). Hypothesis: link-writers-emit-mint-ids.
<!-- THOUGHT:END -->

<!-- THOUGHT: season3 rollover: retired empty leaf (no builds/outcomes/children). -->
