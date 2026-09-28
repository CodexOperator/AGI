---
id: goal:g15.29.23
mint_id: 287f2ac459c041368ca382690ccd5242
type: goal
parents:
  - goal:g15.29
next_edges: []
confidence: 0.7
edited_by: director-engine
goal_id: G15.29.23
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: de5b29c04e1fa879
season: 2
seeds:
  - hypothesis:authority-deferred-key-swap-completes-at-the-next-publish
status: active
tags:
  - core
  - engine
  - residue-batch
  - leaf
title: "G15.29.23: AN AUTHORITY-DEFERRED KEY SWAP COMPLETES AT THE NEXT SUCCESSFUL PUBLISH (0923b mur residue leaf; assigned director-engine)"
town: core
---
# goal:g15.29.23

# goal:g15.29.23 — AN AUTHORITY-DEFERRED KEY SWAP COMPLETES AT THE NEXT SUCCESSFUL PUBLISH

```
leaf      one small round: hypothesis:authority-deferred-key-swap-completes-at-the-next-publish
source    R-EF67 S1 (an authority-deferred pending has no production completion site) · M1 (send._signing_key_obj prefers the pending key) · M2 (the next rotation mints from the predecessor key)
          bytes verified by a read-only triage pass for director-engine 21:3xZ 09-23 on the post tip a281bb0d85 (every file:line read)
rule      KEEP SPLITTING (owner 09-23 10:4xZ, goal:g5): one leaf, one small round; split again if it grows
round     hypothesis:authority-deferred-key-swap-completes-at-the-next-publish
writer    director-engine
```
