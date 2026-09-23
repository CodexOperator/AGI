---
id: goal:g15.27.2
mint_id: 864b3f97a37d4ba884e40ca27693fc6f
type: goal
parents:
  - goal:g15.27
next_edges: []
confidence: 0.7
edited_by: director-engine
goal_id: G15.27.2
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: d9763949a73ca49f
season: 2
seeds:
  - hypothesis:migrate-resolves-the-grant-before-it-seats
status: active
tags:
  - core
  - engine
  - residue-batch
  - leaf
title: "G15.27.2: FR-B2 MIGRATE RESOLVES THE GRANT BEFORE SEATING (0921 engine slice leaf; assigned director-engine)"
town: core
---
# goal:g15.27.2

# goal:g15.27.2 — FR-B2 MIGRATE RESOLVES THE GRANT BEFORE SEATING

```
leaf      cmd_migrate_receive checks the actor_rows grant before _migrate_seat spawns or writes a cell; an inadmissible grant is skipped by name
source    l4-quick-migrate #5 #9 #10 #12 (rotate.py cmd_migrate_receive ~20938, _migrate_seat ~20869)
          sources: the 0921 mur disposition table (hypothesis:mur-0921-engine-residues-dispositioned-and-corrected)
rule      KEEP SPLITTING (owner 09-23 10:4xZ, goal:g5): one leaf, one small round; split again if it grows
round     hypothesis:migrate-resolves-the-grant-before-it-seats
```
