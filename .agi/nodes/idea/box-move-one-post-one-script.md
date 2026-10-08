---
id: idea:box-move-one-post-one-script
mint_id: 68dda7ca8d554caf9b484c80554a3db5
type: idea
parents:
  - goal:g7.16.1.11.7
next_edges: []
edited_by: belam
scaffold_hash: 755c27289b31e4c4
season: 2
title: One post moves box to box with ONE script (box-move.sh), run by the Prime on the source box
town: core
---
# idea:box-move-one-post-one-script

# One post moves box to box with ONE script, run by the Prime on the source box

```
source box (MAIN, the Prime)                                  target box (host act installed)
flip row box (one cell, word-diff 2) -> stop agi-post@P ---> trunk + posts/P (+ extras) pushed, no force
   (agi-flush lands the last turn)                            ff MAIN · host-act move P (pin bump, projection) · start agi-post@P
owner: login URL (url) -> code on stdin (login) ------------> fifo: code · Enter · Security notes · trust = Yes -> first turn
```
Proved 10-08 on the local-town -> encryption-town move (pilot DG5, then DG2 DG4 DT-1 TM alive all-is-one). Gaps the pilot found and
closed by hand (G1 boot-only wants link · G2 MAIN .git ACL incl. user belam · G3 inbox ACL + AGI_BOX in E shells) are listed in the
script header as target requirements; the host act carries them (DG3).
