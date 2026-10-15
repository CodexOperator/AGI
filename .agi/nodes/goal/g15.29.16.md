---
id: goal:g15.29.16
mint_id: 2eef627b25d246819f2716507adf306d
type: goal
parents:
  - goal:g15.29
next_edges: []
confidence: 0.7
edited_by: director-engine
goal_id: G15.29.16
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: 3bd6ef44006e30ca
season: 2
seeds:
  - hypothesis:secrets-error-own-type-and-hook-reads-graph-secrets-node
status: active
tags:
  - core
  - engine
  - residue-batch
  - leaf
title: "G15.29.16: SECRETSERROR IS ITS OWN TYPE AND THE HOOK READS THE GRAPH'S SECRETS NODE (0923b mur residue leaf; assigned director-engine)"
town: core
---
# goal:g15.29.16

# goal:g15.29.16 — SECRETSERROR IS ITS OWN TYPE AND THE HOOK READS THE GRAPH'S SECRETS NODE

```
leaf      one small round: hypothesis:secrets-error-own-type-and-hook-reads-graph-secrets-node
source    R-EF59 S1 (SecretsError widened to ValueError) · M1 (the test asserts ValueError) · M2 (the hook path reads no secrets node)
          bytes verified by a read-only triage pass for director-engine 21:3xZ 09-23 on the post tip a281bb0d85 (every file:line read)
rule      KEEP SPLITTING (owner 09-23 10:4xZ, goal:g5): one leaf, one small round; split again if it grows
round     hypothesis:secrets-error-own-type-and-hook-reads-graph-secrets-node
writer    director-engine
```
