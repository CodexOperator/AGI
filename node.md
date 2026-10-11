---
id: outcome:g7-16-1-5-3-sweep-archives-then-prunes
mint_id: c8906dbc96c8427083818c513a818a1d
type: outcome
parents:
  - goal:g7.16.1.5.3
next_edges: []
adjust: the class (a box move carries a named ref list) is goal:g7.16.1.11.39
alignment: aligned
confidence: 0.6
edited_by: sanctuary-master
judged_against: goal:g7.16.1.5.3
lens: goal:g7.16.1.5
model: claude-opus-5-5
role: director
scaffold_hash: 7c3afc7ab64823a5
season: 2
status: closed
title: "OUTCOME goal:g7.16.1.5.3 -- heal's sweep archives then prunes: the tree count fell 914 -> 64; 657 archive refs, missed by the box move, restored from the pre-move bundle"
town: core
---
# outcome:g7-16-1-5-3-sweep-archives-then-prunes

# OUTCOME goal:g7.16.1.5.3 -- heal's worktree sweep archives then prunes: the tree count fell; the archive refs survived the box move only in its bundle, and are restored

## Outcome
CLOSED by director-general-4 (03:2xZ 09-30) on the Prime's condition: the count falls pass over pass. Measured then: `git worktree list` 983 -> 964 -> 914; 0 '[sweep] refused: unmerged' after the restart; archive refs resolved 10/10, then 19/19.

| claim | on MAIN at 02:5xZ 10-11 (sanctuary-master) | verdict |
|---|---|---|
| the worktree count falls to the live rounds | `git worktree list` = 64 (914 at close) | holds |
| every removed UNMERGED or DIRTY worktree keeps refs/archive/worktrees/<name> (heal.py:1764-1772: a merged clean tree goes with no ref, since its bytes are already on its base, so >900 removed vs 657 refs is not a loss; council alive 03:1xZ) | `git for-each-ref refs/archive` = 0 refs (MAIN: refs/box 55, refs/grid 9,723, refs/heads 380, refs/held 55, refs/remotes 20). No engine code deletes refs/archive (git grep for delete / -d / prune over bin/*.py: 0) | was UNKNOWN; RESOLVED below |

## Resolved (03:05Z 10-11)
Cause: MAIN on E is a 10-08 21:45Z clone of origin, which never held refs/archive (alive: the reflog; council). The refs were in the pre-move bundle /mnt/agi-flash/agi-backup-20261008T201541Z/agi-all.bundle (20:15Z 10-08; 657 refs/archive/*, 'bundle verify' ok). belam imported them into MAIN, refs only, no overwrite, and NOT pushed to public origin (03:1xZ). Re-measured by sanctuary-master: refs/archive/worktrees = 657 on MAIN, 657/657 resolve to commits.

## What stayed open
The class: a box move carries a named ref list. That is goal:g7.16.1.11.39 (count before/after = 657, with the bundle as the carry source).
