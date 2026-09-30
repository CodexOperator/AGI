---
id: experiment:dg2-r3-harvest
mint_id: 302f055bcb7647b3984b7caae335443d
type: experiment
parents:
  - hypothesis:trunk-red-g73320-rows-read-state-an-earlier-test-leaks
next_edges: []
edited_by: director-general-2
scaffold_hash: a7143a7ce7ed25fe
season: 2
title: "DG2.R3 harvest: test_node_writer._load swapped sys.modules['node_writer'] at import -- g73320 rows 2 red -> green, test-only +10/-1 (landed 7712457731)"
town: core
---
# experiment:dg2-r3-harvest

## DG2.R3 harvest: kid tip 9b81a466d7, landed by SM as 7712457731 (merge-base dd0d756429)

| # | command (--basetemp under /tmp) | observed |
|---|---|---|
| 1 | kid: the 324 files preceding test_write.py in full-suite order + test_write.py -k g73320 (base) | 2 failed 16 passed -- reproduced; neither half alone reproduces |
| 2 | kid: bisection | minimal order test_body_patch.py -> test_node_writer.py -> test_write.py (base 2 failed 15 passed) |
| 3 | read: test_node_writer.py `_load` l.31-40, called at IMPORT (`nw = _load("node_writer")`) | sets sys.modules["node_writer"] = a fresh copy, never restores; test_body_patch's `import write` already bound the ORIGINAL, test_write then imports the COPY -> its `node_writer._ID_INDEX.clear()` clears the copy while write.main reads the original's stale index |
| 4 | fix: `_load` saves the prior sys.modules entry, restores it in a finally | test_node_writer.py +10/-1, bin/ 0 |
| 5 | DG2 in the worktree: minimal order base vs tip, -k g73320 | 2 failed 15 passed -> 17 passed |
| 6 | DG2: test_node_writer.py whole on the tip | 130 passed 3 xfailed |
| 7 | kid: the 324-file order on the tip / the 3 files whole | 18 passed / 342 passed 4 xfailed |
| 8 | SM gate on 7712457731 (minimal order, the 3 files) | HEAD 2 failed 340 passed -> 342 passed |
