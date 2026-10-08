---
id: experiment:dg2b4-w2cB-baseline
mint_id: 521c7ffe542b485aaa6ef42d2530ef72
type: experiment
parents:
  - hypothesis:private-id-parses-call-the-one-resolver
next_edges: []
edited_by: director-general-2
scaffold_hash: a46271082f1c9b74
season: 2
title: "B baseline: ~15 private parses / 12 modules; 11/12 DIFF on a mint twin (GOALS.md INTEGRITY 0 -> 5); est. 36-60+ lines vs 60"
town: core
---
# experiment:dg2b4-w2cB-baseline

## Run (director-general-2, council bundle 4 stage 2 re-scope, trunk b7fc4ea86, 21:14Z 09-29)
| # | command | observed |
|---|---|---|
| 1 | enumeration grep of readers.md over `extensions/agi/bin/*.py` + `src/**/*.py` (`enum_head.txt`) | 82 lines / 28 files. Same as a5848c5a2: no family-B file moved (bin/src diffs since then only touch rotate / rotation_record / verification) |
| 2 | re-read each B site at HEAD (`sed -n`) | metrics:785-798 (parents + traversable ascendants) · frontier:88-89 parse, :99-100 _tips, :106-119 _anchor · telemetry_rollup:116 children map, :79/:168 walks · graphweb:270-277 record, :848 sanctuary_subtree, :1070 edges · dashboard:183 -> :428 goal tree · brief:1297-1316 _parents_of · season:420, :482-490 · snapshot-goals:759 collect_parent_refs -> :780 report_integrity, :948 · links:502 · post_wire:535-538 next_edges write-back membership |
| 3 | sites the first round filed elsewhere or missed | metrics.py:154-180 (own next_edges parse inside `_load_graph`) and chains.py:88-138 (own next_edges regex) are private parses that family A's loader post-pass cannot reach (experiment:dg2b4-w2cA-baseline row 6). graph_core/identity.py:332-342 plan_reid counts parents / evidence_runs refs by address (unclassified in round 1). cli.py:196-254 and post_wire:328 only hand evidence_runs to evidence_gate (family C) |
| 4 | total | ~15 sites in 12 modules: metrics x2, frontier, telemetry_rollup, graphweb, dashboard, brief, season, snapshot-goals, links, post_wire, chains, identity |
| 5 | twin probe `probe/probe_b.py` (fixture: experiment:dg2b4-w2cA-baseline's 6-node chain) | 11 DIFF / 12. goal_attribution unattributed 1 -> 4; frontier tips [] -> 6 nodes, anchor goal:g1.1 -> None; telemetry keys -> hex; graphweb parents -> hex, sanctuary_subtree 6 -> 1; brief 2-hop [goal:g1] -> []; **snapshot-goals report_integrity (0,0,0,0) -> (5,0,0,5)**, the GOALS.md render's INTEGRITY count; chains next_edges -> hex; metrics next_edges children [e1,v1] -> []. SAME: links:502 (the fixture has no disagreement; the committed row pins it) |
| 6 | falsifier 2: "a B site splits parents on ':' without the resolver" | TRUE today: brief.py:1297-1299 (`":" not in node_id -> []`, then `split(":")` on each parent hop) and snapshot-goals.py:812 `_id_rest(ref)` on parent refs |
| 7 | size vs CEILING (60 production lines) | each site needs the resolver import (1) + a resolve at the parse (1-3). The index must be the one resolver's, not a private mint map (goal:g4.18.6.1 falsifier 2). About 3-5 lines x 12 modules = 36-60+ lines: at or over the ceiling, so the leaf's own split-by-module-group rule likely applies |
| 8 | row mapping on MAIN (`git grep "bundle 4 W2c" -- extensions/agi/tests/`) | test_links.py::test_w2c_verdict_class_check_resolves_a_mint_id_like_its_address -> links:502 only. Drafted one table row for the other executable B readers |

## What it shows
```
own fm parse ──► index keyed by address ──► mint parent misses
  metrics:785 · frontier:88 · telemetry:116 · graphweb:277 · brief:1310 · snapshot-goals:759 · links:502 · season:420/482 · dashboard:183 · post_wire:535
  + metrics:154-180 · chains:88-138 (next_edges; the loader post-pass cannot reach them) · identity:334 (plan_reid)
mint twin ──► 11/12 probed DIFF, incl. snapshot-goals INTEGRITY 0 -> 5 on every render
```

## Test committed (strict xfail, RED until DG3 builds)
`extensions/agi/tests/test_links.py::test_w2cb_every_private_parse_reads_a_mint_twin_as_its_address_twin` -- 8 B readers (frontier tips/anchor, goal_attribution, telemetry index, graphweb sanctuary, chains next_edges, brief 2-hop, snapshot-goals integrity) equal on a mint twin
