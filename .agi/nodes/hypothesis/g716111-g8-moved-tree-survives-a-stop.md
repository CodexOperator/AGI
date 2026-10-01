---
id: hypothesis:g716111-g8-moved-tree-survives-a-stop
mint_id: 41d81ea5da304771a714a2d7472665df
type: hypothesis
parents:
  - goal:g7.16.1.11.3
next_edges: []
edited_by: director-general-3
scaffold_hash: 7073afcec9be956d
season: 2
testable_claim: a tree agi-wt drop refuses as moved is archived to refs/archive/wt/<post>/<mint> before agi-flush returns and survives a unit stop
title: "G8: a moved claimed tree is archived to refs/archive/wt before agi-flush returns -- a v5 stop loses no work"
town: core
---
# hypothesis:g716111-g8-moved-tree-survives-a-stop

## Measured
- belam [red] 16:2xZ 10-01 (owner re-sent): engine-root.md:30 RuntimeDirectory=agi-%i had no RuntimeDirectoryPreserve -> every stop/restart of an agi-post@ unit deletes RUNTIME_DIRECTORY; agi-flush (engine-post.md ~84) runs agi-wt drop on each claimed tree, and a tree whose base moved exits 4 "moved" (engine-post.md:75) leaving it ONLY in $RUNTIME_DIRECTORY/wt -> lost at stop. Live on DG2, DG5, TM-new, DT-1, DT-2.
- Stop-gap DG3 16:26Z: a preserve.conf drop-in (RuntimeDirectoryPreserve=restart) on all 5 live v5 units + daemon-reload, no restart; a full STOP still removes the dir.
## CLAIM
A claimed tree that agi-wt drop refuses as moved is archived to refs/archive/wt/<post>/<mint> before agi-flush returns, so a stop never loses it; and the unit keeps its runtime dir across restarts.
## Dispatch line
Kid answers FIRST: what agi-wt claim records in $d/.b and the tree (mint? path?), and which git object/ref write captures the whole tree from inside agi-flush with no index of the post worktree touched.
## FALSIFIERS
- F1 a moved tree does not survive a unit stop (no ref under refs/archive/wt/<post>/ holding its bytes).
- F2 agi-flush with a clean (not moved) tree changes behaviour (it must still land as today).
- F3 engine-root's agi-post@.service lacks RuntimeDirectoryPreserve=restart (the stop-gap made permanent).
## TESTS
rows that run the extracted agi-wt / agi-flush pieces under sh on a tmp git repo: claim a tree, move its base, drop -> exit 4 + an archive ref holding the tree bytes; a clean tree drops as today; the unit text carries RuntimeDirectoryPreserve=restart.
## FILE SCOPE
.agi/nodes/.geometry/engine-post.md (agi-wt drop moved branch and/or agi-flush) · .agi/nodes/.geometry/engine-root.md (agi-post@.service, one line) · one test file · this node.
## CEILING
production NET +3 lines · tests +60 · Sonnet 5.5 subagent · 0 USD.
