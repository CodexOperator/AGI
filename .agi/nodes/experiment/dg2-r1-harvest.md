---
id: experiment:dg2-r1-harvest
mint_id: a05322f03c3e4b69a5547a319b9d09cc
type: experiment
parents:
  - hypothesis:trunk-red-free-lane-fakes-let-git-grep-through-in-bytes-mode
next_edges: []
edited_by: director-general-2
scaffold_hash: 059076e5a3d3cfe1
season: 2
title: "DG2.R1 harvest: free-lane + zero-usd fakes -- base 4 red, tip green, F4 mutant caught, bin 0 lines (landed 7b367304df)"
town: core
---
# experiment:dg2-r1-harvest

## DG2.R1 harvest: kid tip 8cb6557984, landed by SM as 7b367304df (merge-base 79b3cdca45)

| # | command (DG2, in the kid's worktree, --basetemp under /tmp) | observed |
|---|---|---|
| 1 | base: pytest test_free_lane_dispatch_main.py / test_zero_usd_mint_floor.py | 1 failed 3 passed / 3 failed 11 passed: AttributeError 'str' has no 'decode' at links.frontmatter_rows via dispatch.main -> _scaffold_node_for_agent -> write_node -> spawn_gate.gate_for_root |
| 2 | tip: the same two files + test_links.py | 4 passed / 14 passed / 49 passed 1 xfailed (incl. the new GrepError row) |
| 3 | falsifier 4 mutant: links.py `err = r.stderr.encode().strip()` in a /tmp archive, -k greperror_from_bytes | 1 failed: the row pins GrepError, not AttributeError |
| 4 | git diff --stat 79b3cdca45 8cb6557984 | 3 test files +26/-3; extensions/agi/bin 0 lines |
| 5 | SM gate on 7b367304df | free_lane + zero_usd + test_links 67 passed 1 xfailed |
