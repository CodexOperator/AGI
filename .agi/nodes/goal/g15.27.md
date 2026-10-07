---
id: goal:g15.27
mint_id: dc9964dc8bf44104bef789b9f25bb897
type: goal
parents:
  - goal:g1
next_edges: []
confidence: 0.6
edited_by: director-general-4
goal_id: G15.27
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: 42d48a43bed959dd
season: 2
seeds:
  - hypothesis:send-undelivered-notice-lands-in-the-comms-root
  - hypothesis:write-body-range-guard-is-fence-aware-and-clamped
  - hypothesis:mur-0921-residue-batch-into-season2-main
  - hypothesis:mur-0921-engine-residues-dispositioned-and-corrected
  - hypothesis:alarms-loop-runs-flat-and-the-capture-grace-restarts-per-session
status: active
tags:
  - core
  - engine
  - residue-batch
title: "G15.27: 09-21 PRIME RESIDUE BATCH, ENGINE SLICE -- chunk 1 R1 send.py undelivered notice + R2 write.py fence/EOF guard merged up 09-23; chunk 2 = the 15 engine rounds (130 residues: node corrections + fix rounds FR-A..FR-D)"
town: core
---
<!-- BODY:BEGIN -->
# goal:g15.27 — 09-21 Prime residue batch, ENGINE SLICE (director-engine)

```
source    hypothesis:mur-0921-residue-batch-into-season2-main (belam 11:49Z 09-21 + TM TME.17; owner 01:4xZ: batch the residues, ONE batch mur)
split     33 rounds by the batch node's own rule: 15 engine (incl. engine-delta) = THIS goal · 13 lm-* = thought-master · 6 under g7.33 = HELD
chunk 1   R1 hypothesis:send-undelivered-notice-lands-in-the-comms-root   EF.12  PROVED
          R2 hypothesis:write-body-range-guard-is-fence-aware-and-clamped EF.11  PROVED
          batch mur R1 ACCEPT · R2 accept_with_residue · 0 demote -> [merge-up] to thought-master 08:3xZ 09-23 @4c5dee025   DONE
chunk 2   table   hypothesis:mur-0921-engine-residues-dispositioned-and-corrected -- 130 items: F 34 · C 34 · K 58 · G 4; its round applies C
          FR-A    hypothesis:alarms-loop-runs-flat-and-the-capture-grace-restarts-per-session -- LIVE: alarms recursion + capture stamp
          leaves  g15.27.1-.6 (KEEP SPLITTING, owner 10:4xZ): .1 FR-B1 · .2 FR-B2 · .3 FR-B3 · .4 FR-C1 · .5 FR-C2 · .6 FR-D1 -- one small round each:
                  FR-B rotate verbs read MAIN rows + migrate resolves the grant before seating (rotate.py)
                  FR-C kid wait + turn-end evidence (cli.py dispatch.py heal.py) · kid ceiling + liaison moral (brief.py)
                  FR-D write.py outside-ref gate + escaped && · paths.py / boxes.py / crons.py audits
          flagged research-review F items (thought-side node) -> thought-master · lm-replace-body-anchor demote (g7.33.1) -> HELD
done when chunk 1 merged up (done) · the table's C items applied · every F item landed or carried by name ·
          ONE batch mur over the corrected demote rounds + the landed FR rounds returns no demote · one [merge-up] names the batch node
```

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Re-parented goal:g15 -> goal:g1 (director-general-4 on belam [decision] 00:xZ 09-30, option a: retired designation g15 -> g20 -> goal:g1, the Prime template rule that a retired id is never used). parents field only: no renumber, mint_id untouched. Deviation from the order's letter, recorded here: belam named the 32 active LEAVES; they hang under three active intermediates (goal:g15.27 x6, g15.28 x3, g15.29 x23), so the intermediates move and the leaves keep their nesting -- moving each leaf would flatten the tree and strand these three as active goals with no leaves. This one carries 6 of them.
<!-- THOUGHT:END -->
