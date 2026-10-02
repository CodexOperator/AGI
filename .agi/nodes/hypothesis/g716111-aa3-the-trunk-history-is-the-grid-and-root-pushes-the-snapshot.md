---
id: hypothesis:g716111-aa3-the-trunk-history-is-the-grid-and-root-pushes-the-snapshot
mint_id: e727cfe306804885974345dd199fcb29
type: hypothesis
parents:
  - goal:g7.16.1.11.13
next_edges: []
confidence: 0.6
edited_by: director-general-1
scaffold_hash: ce70910a17bcf6e5
season: 2
testable_claim: "After the switch: (V1) `git for-each-ref refs/grid | wc -l` stays constant for 1 h while posts work (nothing new is written, nothing moved or deleted); (V2) the origin trunk tip is never older than 65 min (root's carrier pushes the trunk + refs/box/* hourly; branch_push retires; no snapshot commit, every change already IS a commit); (V4) `git log --format=%h -1 -- <node>` on the trunk names the land that carried that node's last per-turn commit (the trunk's history IS the grid, one node per commit checked at the land); grid.py's READ verbs keep working on the archive refs and `grid.py commit` retires."
title: "AA3.10: the hourly snapshot is root's carrier pushing the trunk, the trunk's history replaces the per-node grid refs, and grid_sync retires while refs/grid/* stay as the archive"
town: core
---
# hypothesis:g716111-aa3-the-trunk-history-is-the-grid-and-root-pushes-the-snapshot

## Measured
- doc:rse-aa3-land AA3.10 (all-is-one-merge-up-2 0efe1e0f6; belam [decision] 00:25Z, owner 00:3x-00:4xZ). TRUE STATE (00:3xZ 10-02): the global grid is LIVE (35 refs/grid/* written in the last hour, 189 in 24 h; 5,756 refs/grid/local-maxxing + 3,807 refs/grid/node = 9,563 of 11,779 refs, all pushed to origin); `branch_push` '7 * * * *' pushes the CHECKED-OUT branch from belam's crontab; v5 uids hold no GitHub credential.
- A post cannot delete a ref and moving 9.5k refs is a delete + create, so the grid refs are NOT moved: they ARE the archive.
- OPEN for belam: whether refs/grid/* stay pushed to origin (history GitHub already holds) or are dropped from the carrier's refspec (an owner call: it is the GitHub copy).
- DEPENDS ON goal:g7.16.1.11.11 (the carrier, the one GitHub key stored on root) and AA1.V (per-turn one-node commits onto posts/<p>).

## CLAIM
After the switch: (V1) `git for-each-ref refs/grid | wc -l` stays constant for 1 h while posts work (nothing new is written, nothing moved or deleted); (V2) the origin trunk tip is never older than 65 min (root's carrier pushes the trunk + refs/box/* hourly; branch_push retires; no snapshot commit, every change already IS a commit); (V4) `git log --format=%h -1 -- <node>` on the trunk names the land that carried that node's last per-turn commit (the trunk's history IS the grid, one node per commit checked at the land); grid.py's READ verbs keep working on the archive refs and `grid.py commit` retires.

## Dispatch line
config-max: cron:crons `grid_sync` enabled false, `branch_push` retired, the carrier's hourly schedule (cells) / template-max: none / code: root's carrier push line (AA1's carrier), no new engine bytes.

## FALSIFIERS
AA3.10 V1 refs/grid count constant for 1 h under live work · V2 the origin trunk tip never older than 65 min · V4 `git log -1 -- <node>` on the trunk names the carrying land · negative: no process other than root writes refs/grid/* after the switch, and `git for-each-ref refs/grid | wc -l` before and after the switch is equal.

## TESTS
a scratch repo test: a land range with one commit per node, `git log -- <node>` names it; the carrier's push cadence asserted from the cell; the live check is one hour of refs/grid counts.

## FILE SCOPE
cron:crons cells (grid_sync, branch_push, the carrier schedule) · the carrier push line · this node's kid node. The Prime lands cells it owns. Never delete or move a refs/grid ref.

## CEILING
1 parent · kids <= 1 · 0 B in the zygote · regular review. HORIZON behind the boxes carrier (goal:g7.16.1.11.11).
