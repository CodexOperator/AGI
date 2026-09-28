---
id: goal:g15.27.4
mint_id: f25695742d3c489abb89fe53298b67d2
type: goal
parents:
  - goal:g15.27
next_edges: []
confidence: 0.7
edited_by: director-engine
goal_id: G15.27.4
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: e9fa86106093831f
season: 2
seeds:
  - hypothesis:wait-returns-on-an-empty-kid-set-and-turn-end-keeps-death-evidence
status: active
tags:
  - core
  - engine
  - residue-batch
  - leaf
title: "G15.27.4: FR-C1 A PARENT'S WAIT AND A TURN-END KEEP THEIR EVIDENCE (0921 engine slice leaf; assigned director-engine)"
town: core
---
# goal:g15.27.4

# goal:g15.27.4 — FR-C1 A PARENT'S WAIT AND A TURN-END KEEP THEIR EVIDENCE

```
leaf      cli.py wait returns at once on zero matching kids and prints elapsed; a turn-end reap keeps the stream-error death evidence
source    l5-a-parent-waits DEF1 DEF5 MISSED2 MISSED3 + engine-delta DEF3 (cli.py cmd_wait; dispatch.py turn-end reap; heal.py reap)
          sources: the 0921 mur disposition table (hypothesis:mur-0921-engine-residues-dispositioned-and-corrected)
rule      KEEP SPLITTING (owner 09-23 10:4xZ, goal:g5): one leaf, one small round; split again if it grows
round     hypothesis:wait-returns-on-an-empty-kid-set-and-turn-end-keeps-death-evidence
```
