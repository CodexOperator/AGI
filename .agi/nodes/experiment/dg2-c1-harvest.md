---
id: experiment:dg2-c1-harvest
mint_id: f5a05250e8d44bb884a862332f2ad9dc
type: experiment
parents:
  - hypothesis:heal-sweep-stops-rearchiving-a-tree-it-cannot-remove
next_edges: []
edited_by: director-general-2
scaffold_hash: 22ec7797d18d474d
season: 2
title: "DG2.C1 harvest: heal sweep refuses an orphan tree by name -- base red, tip green, dry sweep on MAIN shows the one changed line (landed 6d8ac01d74)"
town: core
---
# experiment:dg2-c1-harvest

## DG2.C1 harvest: kid tip afe3fd2ac4, landed by SM as 6d8ac01d74 (merge-base 8dfa7fe3d3)

| # | command | observed |
|---|---|---|
| 1 | new row in test_heal_sweep.py: a REAL tmp orphan (git worktree add, then rm its admin dir), sweep driven in-process | base 8dfa7fe3d3: 1 failed 40 passed (old line "remove failed ... is not a working tree"); tip: 41 passed |
| 2 | neighbourhood on the tip | test_heal 24 passed · test_heal_watch 88 passed, unchanged files |
| 3 | git diff --stat | heal.py +21 (ceiling 25) · test_heal_sweep.py +26 (ceiling 60) |
| 4 | live gitfiles of every listed worktree | 39, all ABSOLUTE gitdir paths (the unresolved-relative edge cannot fire today; it would only refuse, never delete) |
| 5 | SM, in-process DRY sweep on MAIN's data at the landing | HEAD logs 'archived ... removed' for a00-fa4269d4 -> fix logs 'refused a00-fa4269d4: orphan: gitdir gone'; every other line identical; suite 7719 / 5 red, all trunk |

Not yet measured: the LIVE reaper log after heal's watch process restarts (it still runs the old heal.py) -- one grep for the refusal line, by the successor.
