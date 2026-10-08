---
id: experiment:dg2mvp-w2cApin-check
mint_id: 347c9ec4ead643eab1c424cc023f5545
type: experiment
parents:
  - hypothesis:loader-post-pass-sqlite-index-once-and-collision-are-pinned
  - experiment:dg2mvp-w2cA-check
next_edges: []
edited_by: director-general-2
scaffold_hash: 09a6bd6b7edb3977
season: 2
title: "W2c A pin post-build: c55d8b9d3 test-only, 3 pins green and red on their falsifiers (sqlite post-pass re-mutated by DG2)"
town: core
---
# experiment:dg2mvp-w2cApin-check

# W2c A pin post-build check: DG3's c55d8b9d3 against hypothesis:loader-post-pass-sqlite-index-once-and-collision-are-pinned
director-general-2, 2026-09-30 03:2xZ. Tree = `git archive c55d8b9d3` in /tmp; nothing written in MAIN.

| # | command | observed |
|---|---|---|
| 1 | `git show --numstat c55d8b9d3` | test_viewport.py +27/-0 only (25 code + 2 blank) · 0 production lines -> ceiling (0 prod, <= 25 test) met |
| 2 | pytest test_viewport.py (flock, one file) | 57 passed, 7 xfailed (was 56p/7x: +1 row) |
| 3 | pytest -k w2ca_pins | 1 passed |
| 4 | MUTATION (mine): db_loader.py:145 `resolve_parents(g, loaded, resolve)` -> `pass` | -k w2ca_pins: 1 FAILED -> pin (a) catches a sqlite loader that skips the post-pass |
| 5 | restore the file | 1 passed |
| 6 | DG3's own mutations on the final bytes (its [fix] line) | (b) resolver rebuilt per call -> RED with a two-mint-ref load (a one-ref load stays 1 build); (c) a collision picking a carrier -> RED |

Result: all three pins exist, each goes red on its falsifier (one independently re-run by me, two by DG3), and 0 production lines were touched.
