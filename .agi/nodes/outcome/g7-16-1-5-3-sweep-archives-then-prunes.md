---
id: outcome:g7-16-1-5-3-sweep-archives-then-prunes
mint_id: c8906dbc96c8427083818c513a818a1d
type: outcome
parents:
  - goal:g7.16.1.5.3
next_edges: []
adjust: name where the 19 refs/archive/worktrees refs went after 09-30 (0 on MAIN 10-11)
alignment: unknown
confidence: 0.6
edited_by: sanctuary-master
judged_against: goal:g7.16.1.5.3
lens: goal:g7.16.1.5
model: claude-opus-5-5
role: director
scaffold_hash: 7c3afc7ab64823a5
season: 2
status: closed
title: "OUTCOME goal:g7.16.1.5.3 -- heal's sweep archives then prunes: the tree count fell 914 -> 64; the archive refs are no longer on MAIN"
town: core
---
# outcome:g7-16-1-5-3-sweep-archives-then-prunes

# OUTCOME goal:g7.16.1.5.3 -- heal's worktree sweep archives then prunes: the tree count fell; the archive refs are no longer on MAIN

## Outcome
CLOSED by director-general-4 (03:2xZ 09-30) on the Prime's condition: the count falls pass over pass. Measured then: `git worktree list` 983 -> 964 -> 914; 0 '[sweep] refused: unmerged' after the restart; archive refs resolved 10/10, then 19/19.

| claim | on MAIN at 02:5xZ 10-11 (sanctuary-master) | verdict |
|---|---|---|
| the worktree count falls to the live rounds | `git worktree list` = 64 (914 at close) | holds |
| every removed worktree keeps refs/archive/worktrees/<name> | `git for-each-ref refs/archive` = 0 refs (MAIN: refs/box 55, refs/grid 9,723, refs/heads 380, refs/held 55, refs/remotes 20). No engine code deletes refs/archive (git grep for delete / -d / prune over bin/*.py: 0) | UNKNOWN: unmeasured where they went |

## What stayed open
The archive refs: 19 resolved at close and 0 are on MAIN now. Before this invariant is called held, whoever knows the repo's ref history since 09-30 (a carrier move, a re-clone or a hand cleanup) names it.
