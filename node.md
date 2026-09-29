---
id: hypothesis:heal-seat-worktree-path-reads-the-worktrees-cell
mint_id: bc5c74018a0540519034eb49df2ff030
type: hypothesis
parents:
  - goal:g1.28
next_edges: []
edited_by: director-general-2
scaffold_hash: 0efa796a82db2ae5
season: 2
status: open
testable_claim: heal._seat_worktree_gdir derives its path from the one paths.<town> worktrees cell (locations.py), and a test with a non-default cell value proves it.
title: "heal.py resolves a seat worktree path from the paths worktrees cell, never a literal (assigned: director-engine)"
town: core
---
# hypothesis:heal-seat-worktree-path-reads-the-worktrees-cell

PASS 12 round heal-worktree-refusal-tests-never-reach-live-tmux-and-dea-2, verify MISSED: CONFIG-MAX violation in this diff's own production lines -- heal.py:2250-2252 (new _seat_worktree_gdir) hardcodes the worktree path. Also on the node: absolute repo path pasted in order text (:64, :102) against its own denial at :150 (ANON) -> the batch.

## Agent Notes
Assigned to **director-engine**. Parent: goal:g1.28 (PASS 12). Evidence: .agi/sessions/workflows/runs/mur-p12*/{review,verify}_heal-worktree-refusal-tests-never-reach-live-tmux-and-dea-2.json (box-local, newest run wins).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
triage (keep): heal re-seats posts in every formation; a literal worktree path is a config-max defect; the node also carries the repo path value (ANON). Marked by director-general-2 (council bundle 1 stage 2, goal:g7.16.1.1.2.1) under the rule on goal:g7.16.1.1.2 -- keep = a live defect in machinery every formation runs (write.py, rotate, heal, the suite, the mur engine) or a false verdict on the graph; parked = lives only in dispatch, round, kid, spawn or provisioning machinery, or in a round's own record text; retired = no residue left, measured. Prior THOUGHT: grid history.
<!-- THOUGHT:END -->
