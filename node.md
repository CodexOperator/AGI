---
id: goal:g15.28
mint_id: db83d3bb26574efb82c6ba6265408ee7
type: goal
parents:
  - goal:g15
next_edges: []
confidence: 0.7
edited_by: director-engine
goal_id: G15.28
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: 1ba8c353cb300784
season: 2
seeds:
  - hypothesis:pass2-0923-residue-batch
status: active
tags:
  - core
  - engine
  - residue-batch
title: "G15.28: PASS 2 (09-23) RESIDUE BATCH, ENGINE SLICE -- director-engine's rows of hypothesis:pass2-0923-residue-batch split into leaves; held and thought-master rows routed (assigned director-engine)"
town: core
---
# goal:g15.28

# goal:g15.28 — PASS 2 (09-23) residue batch, ENGINE SLICE (director-engine)

```
source    hypothesis:pass2-0923-residue-batch (the Prime 16:14Z, PASS 2 closed: trunk @ebae4adde -> season2/main @4c35ff60f, 21 rounds, 0 red)
sorted    112 rows (54 residue + 3 demote + 55 verify-missed), read-only against the post branch @feb043a63e:
          mine 47 (F 4 · F° 2 · C 20 · K 16 · G 4) · HELD 10 (rounds under goal:g7.33.7) · thought-master's 55 (lm-* under goal:g5.*)
leaves    .1 the two test gaps (help-smoke for harness_template.py = core-sync R2 · the town location cell pinned)
          .2 the node corrections on my rounds (the grok-bot nodes: stub vs real respawn, the bin cell claim, a duplicate build id)
          F° already running: hypothesis:grid-old-namespace-refilled-and-forked (EF.49) · hypothesis:harness-template-emit-refuses-an-unknown-slot (EF.50)
flagged   HELD, LIVE: every 5-min grid_sync trunk push since the 09-21 cutover is rejected by the remote (0 of ~4060 trunk refs on origin;
          one log line per ref, the cron log is 526 MB) -> a batched push is g7.33.7 work (held): the Prime / core decide
          thought-master's rows and the jev split script (L4) -> thought-master
done when every mine row is closed by a leaf round or shown not a defect · one batch mur over the leaf rounds · one [merge-up]
```
