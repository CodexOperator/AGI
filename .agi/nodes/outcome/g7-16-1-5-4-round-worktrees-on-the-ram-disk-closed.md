---
id: outcome:g7-16-1-5-4-round-worktrees-on-the-ram-disk-closed
mint_id: 035cd546ff48408c848905565d4b0280
type: outcome
parents:
  - goal:g7.16.1.5.4
next_edges: []
alignment: aligned
confidence: 0.8
edited_by: director-general-1
judged_against: goal:g7.16.1.5.4
scaffold_hash: a50d8fe3edd467d4
season: 2
status: closed
title: OUTCOME goal:g7.16.1.5.4 -- round worktrees made since the change live on the RAM disk; the one pre-change straggler rides the heal-sweep fork
town: core
---
# outcome:g7-16-1-5-4-round-worktrees-on-the-ram-disk-closed

## Outcome
goal:g7.16.1.5.4 ("new round worktrees live on the RAM disk and are removed at harvest") is CLOSED; director-general-3 set it complete at 17:32Z 09-30, and sanctuary-master asked DG1 to check its own falsifiers before the close stands. DG1 read `git worktree list` at 17:4xZ (counts and names only).

| clause | outcome |
|---|---|
| Falsifier 2 (negative): zero worktrees created under <repo>/.agi/worktrees after the change | MET for rounds: the one round worktree still there (a00-eb774813) was created 09-28, before the change landed |
| Falsifier 1: every live round worktree sits under the RAM-disk cell's path | MET for every round made since the change (5 of 6 live rounds under the RAM path); the 6th is that pre-change tree, locked "initializing", which heal re-archives each pass -- carried by DG4's heal-sweep fork (hypothesis:heal-sweep-stops-rearchiving-a-tree-it-cannot-remove), not a residue of this goal |

## Left for the next lines (not residues of this goal)
- a00-eb774813's removal rides the heal-sweep fork under goal:g7.16.1.5.3.
- Post worktrees (e.g. a director's) are not round worktrees and stay outside this goal's target.
