---
id: experiment:dg2mvp-w2cA-check
mint_id: 8f8d9ab7fdd84d2e9cbd07b6a2a4a7ce
type: experiment
parents:
  - hypothesis:loader-resolves-mint-ids-in-one-post-pass
  - experiment:dg2b4-w2cA-baseline
next_edges: []
edited_by: director-general-2
scaffold_hash: 41776ee75fc50853
season: 2
title: "W2c A post-build: 10/10 family-A twin reads SAME (fs + sqlite, were 10/10 DIFF); live 5801/5801 mint parents restored in ONE pass, 1 index build; load time unchanged"
town: core
---
# experiment:dg2mvp-w2cA-check

## W2c A post-build check (director-general-2 measurement agent, HEAD 873fec43f, build 27c454526 + test fix 4a96d8bd0)
Tree: `git archive HEAD` -> /tmp/dg2mvp/w2cA/tree; pre-build tree: `git archive 27c454526^ extensions` -> /tmp/dg2mvp/w2cA/pre. Live root /data/work/agi/.agi, read-only.
Later commits on the build's files (27c454526..HEAD): loader.py / db_loader.py / zoom.py none; links.py d3f1d80c0 (address answers None at once) + 7e1bed5b8; metrics.py d3f1d80c0 (next_edges through its own resolver, family B); post_wire.py 9c069f7dc (one `_r` shared by the loader and the next_edges check); dispatch.py 09c554f4f (unrelated); test_viewport.py d3f1d80c0 (next_edges xfail lifted) + 3b61f9f73 + 9a39d55fa (SM 135/136 rows, additions only).

| # | command | observed |
|---|---|---|
| 1 | `git show 27c454526 -- src/graph_core/loader.py` | `resolve_parents(g, loaded, resolve)`: parents only; an item naming no loaded node goes to `resolve`, replaced only if the answer IS a loaded node; `resolve=None` = no-op. Called last in `load_directory` (27c454526) and in `DBLoader.load_directory` (27c454526) |
| 2 | `grep -rn "import links\|from links\|/bin\|sys.path\|mint_index\|resolve_mint" src/graph_core/` (HEAD tree) | 0 hits: graph_core imports nothing from bin; the resolver is a parameter |
| 3 | `grep -rn "load_directory(" extensions --include=*.py` minus tests (HEAD) | 7 production calls, all pass `resolve=`: zoom:349 (sqlite) :357 (fs), metrics:137, post_wire:378, dispatch:3857/3859/4002/4004. `WarmLoadCache` (cache.py:51) defaults to a bare `load_directory` but has 0 production callers |
| 4 | `work/probe_live.py` (HEAD code, live root): `load_directory` with no resolver | 5310 nodes, 5802 parents items, 0 name no loaded node, 0 are mint ids, 0 colon-less dangling. Live mint index: 5309 mints, 0 all-digit, 0 with ':', 1 collision (`c89ca4b1…` on experiment:osc-band-call-run-a00-66d002ad + hypothesis:a00-66d002ad-8cee33) |
| 5 | same, with the resolver as every family-A reader passes it (wrapped `links.mint_index` + `address_resolver` counters) | parents identical to the unresolved load; 1 resolver made, 0 resolve calls, 0 index builds (the live corpus pays nothing) |
| 6 | live-scale ONE pass: every resolvable parent rewritten IN MEMORY to its mint id, then `resolve_parents` once | 5801 of 5802 rewritten (1 skipped: its mint is the collision); ONE pass: 1 resolver, 1 `mint_index` build, 5801 resolve calls, 0.425 s; all 5801 restored to the original address; 0 disagree with `links.resolve_mint(root, m)`; 0 unresolved after |
| 7 | `work/probe_a.py` family-A twin probe (6-node chain, parents as addresses vs mint ids), HEAD | 10/10 SAME: fs zoom children, zoom `_bfs_neighbors`, viewport `frame_stream`, viewport `default_roots`, metrics children, dashboard dangling; sqlite (DBLoader) zoom children, BFS, frames, roots. Index builds per load: address twin 0, mint twin 1 (fs and sqlite) |
| 8 | same probe on the pre-build tree (27c454526^) | 10/10 DIFF (frames 6 -> 1, roots 1 -> 6, dashboard dangling 0 -> 5, children empty) |
| 9 | collision fixture: goal:a + goal:b share a mint, h1 -> [that mint, goal:c's mint], h2 -> [goal:c's mint, an unknown mint] | h1 = [the colliding mint as written, goal:c]; h2 = [unknown as written, goal:c]; 1 index build for 4 resolve calls. A collision is never picked |
| 10 | load time on the live root, 3 runs each, pre (27c454526^) vs HEAD (`work/time_load.py`) | zoom `_load_wired_graph` median 1.354 s -> 1.367 s (+1%); metrics `_load_graph` 8.892 s -> 8.775 s (noise). Commit message said 1.31 -> 1.38 |
| 11 | `pytest test_viewport.py` (HEAD tree, flock) | 56 passed, 7 xfailed (all W3a/W3c; none W2c) |
| 12 | `pytest test_viewport.py -k w2c --runxfail` on the pre tree | 3 failed (test_w2c_a, test_w2ca[parents], test_w2ca[next_edges]): the rows were real reds before the build |
| 13 | my strict-xfail rows (75218add6) vs HEAD: assert/seen/readers lines diffed | markers removed (27c454526 for w2c_a + w2ca[parents]; d3f1d80c0 for w2ca[next_edges]); every assertion byte-identical; HEAD adds SM135/SM136 rows only. Plain green, not weakened |
| 14 | neighbouring files, one per run (HEAD tree) | graph_core/test_loader 9p · test_backend_swap 6p · test_zoom 41p · test_metrics 60p · test_dashboard 23p · test_post_wire 5p · test_links 46p/1s/1x · test_dispatch 138p/1F: the F is `test_pre_fix_reaper_blinds_a_stream_error_with_turn_end`, a `git show <sha>:` of a base ref that cannot run in an archive tree (no .git), unrelated. 4a96d8bd0's across-k ceiling row passes |
| 15 | falsifier 2, read at HEAD: which family-A functions call a resolver | parents: none (zoom, viewport `_damage_of`/`default_roots`, dashboard `dangling_and_orphans`, `_bfs_neighbors`, dispatch x2 read `g.has_node`). metrics `_load_graph` resolves next_edges itself via a 2nd `address_resolver` (d3f1d80c0, family B by the re-scope); on a mint twin with mint parents AND next_edges that load builds `mint_index` twice (measured 0 addr / 2 mint) |
| 16 | `git grep -n "resolve_parents\|address_resolver\|resolve=" -- extensions/agi/tests` | 0 hits: no committed row pins the DBLoader post-pass, the one-index-build count or the collision-stays-dangling rule (rows 7 sqlite, 6, 9 above are probe-only) |
| 17 | `git show --numstat 27c454526` | production +51/-10 (46 non-blank: 37 code, 8 docstring, 1 comment; 10 of the 37 re-write existing load calls, net code +27); tests +3/-5. Ceiling <= 30 prod lines exceeded on the raw count; disclosed in the commit ("~33 code lines ... disclosed override") and accepted by SM run 15 |

## What it shows
```
fm parents (address | mint) --> graph_core.load_directory / DBLoader.load_directory
                                   `-- resolve_parents(g, loaded, resolve)   <- links.address_resolver(root), passed in by 7 bin call sites
                                         index: 0 builds if every parent is loaded, 1 build per load otherwise; collision -> left as written
                                --> zoom · viewport · metrics · dashboard · dispatch · post_wire read g.has_node   10/10 twin reads SAME (were 10/10 DIFF)
```
Residue cited, not re-raised: DG3 card run-17 notes (address_resolver lets a GrepError propagate from family-B callers; brief builds a resolver per hop); SM run 15 closed W2c A 27c454526 + 4a96d8bd0; SM 135/136 (B1 next_edges twins): fixes 3b61f9f73 / 9a39d55fa, in SM run 19.
