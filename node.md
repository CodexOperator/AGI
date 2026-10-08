---
id: goal:g15.27.3
mint_id: 4625fb7baafb4a98bc8b8e7d921c9c48
type: goal
parents:
  - goal:g15.27
next_edges: []
confidence: 0.7
edited_by: director-engine
goal_id: G15.27.3
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: 292e2930fbb2735f
season: 2
seeds:
  - hypothesis:migrate-transcript-copy-survives-sftp-mode-scp
status: active
tags:
  - core
  - engine
  - residue-batch
  - leaf
title: "G15.27.3: FR-B3 MIGRATE COPIES THE TRANSCRIPT WITH A PATH SCP CAN RESOLVE (0921 engine slice leaf; assigned director-engine)"
town: core
---
# goal:g15.27.3

# goal:g15.27.3 — FR-B3 MIGRATE COPIES THE TRANSCRIPT WITH A PATH SCP CAN RESOLVE

```
leaf      MEASURE first: does the migrate transcript copy's remote "$HOME/..." path fail under OpenSSH 9.6 SFTP-mode scp (inferred, never measured)
source    l4-quick-migrate #11 (rotate.py migrate scp ~20747; inferred, not measured)
          sources: the 0921 mur disposition table (hypothesis:mur-0921-engine-residues-dispositioned-and-corrected)
rule      KEEP SPLITTING (owner 09-23 10:4xZ, goal:g5): one leaf, one small round; split again if it grows
round     hypothesis:migrate-transcript-copy-survives-sftp-mode-scp
```
