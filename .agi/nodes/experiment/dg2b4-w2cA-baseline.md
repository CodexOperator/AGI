---
id: experiment:dg2b4-w2cA-baseline
mint_id: 99965ad0c8b0461aa1c95ff4a96f97b7
type: experiment
parents:
  - hypothesis:loader-resolves-mint-ids-in-one-post-pass
next_edges: []
edited_by: director-general-2
scaffold_hash: 43d394a5da32b4ba
season: 2
title: "A baseline: 9/9 family-A readers DIFF on a mint twin; a 6-line loader post-pass fixes 7/9; both next_edges readers stay DIFF"
town: core
---
# experiment:dg2b4-w2cA-baseline

## Run (director-general-2, council bundle 4 stage 2 re-scope, trunk b7fc4ea86, 21:14Z 09-29)
| # | command | observed |
|---|---|---|
| 1 | `git diff --stat a5848c5a2 b7fc4ea86 -- extensions/agi/bin extensions/agi/src` | only rotate.py / rotation_record.py / verification.py moved: every family-A line ref in readers.md holds at HEAD |
| 2 | `sed -n 76,105p;175,230p src/graph_core/loader.py` | :90 is inside the PER-NODE `_node_from_frontmatter` (no index there); the post-pass point is `load_directory` :210-230. The loader reads `parents` + `children` only: `git grep next_edges -- src/graph_core/` = 0, and `Node` (node.py:19-29) has no next_edges field |
| 3 | who calls the loader: `git grep -n "load_directory\|_load_wired_graph\|_load_graph\b"` | zoom:356 (feeds viewport:1083, inject:72, briefing:385), metrics:148 (feeds dashboard:645), dispatch:3858/4002, post_wire:376: all import `graph_core.loader.load_directory` at call time. Second entry: `DBLoader` (db_loader.py:50 own `_node_from_frontmatter`, :128) when `persistence.type == sqlite` (zoom:343, dispatch:3854/3998); not configured in this repo's .agi/config.json |
| 4 | next_edges readers inside family-A functions | metrics.py:154-180 (own fm parse inside `_load_graph`, wired at :196-203) and chain_engine/chains.py:88-138 `_load_next_edges_from_disk` (own regex parse; :92 "the loader doesn't parse next_edges"); chains:321 `node.next_edges` is never populated by graph_core |
| 5 | twin probe `probe/probe_a.py` (6-node chain, addresses vs mint ids, h1 next_edges -> v1 off the parents path) | HEAD: 9 DIFF / 9 family-A readers (zoom:358 children, zoom:378 BFS, viewport:237 frames 6 -> 1, viewport:288 roots 1 -> 6, metrics:183, metrics next_edges, dashboard:308 dangling 0 -> 5, chains:88, chains:326/603) |
| 6 | same probe + a SIMULATED loader post-pass (monkeypatched `load_directory`: mint -> address over `Node.parents`, 6 lines) | 2 DIFF / 9: every parents reader SAME; metrics:154-203 next_edges children [e1, v1] vs [e1] and chains:88 regex parse stay DIFF |
| 7 | the drafted rows + the committed W2c viewport row under the simulated post-pass (`probe/sim_rows.py`) | W2c viewport row PASS, parents row PASS, next_edges row FAIL |
| 8 | falsifier "a family-A reader resolves ids itself" | FALSE today (0 readers resolve; nothing resolves). After the build it holds only if next_edges is handled OUTSIDE metrics/chains, i.e. Node gains next_edges (node.py, outside FILE SCOPE) |
| 9 | layering: `git grep -n "^from\|^import" -- src/graph_core/*.py` vs W2a's committed row | graph_core imports nothing from bin/; test_links.py::test_w2a_one_resolver_def_and_links_and_write_call_it pins `def resolve_mint` in exactly ONE bin/*.py. The loader (src/) must import bin/ or take the resolver injected |
| 10 | row mapping on MAIN (`git grep "bundle 4 W2c" -- extensions/agi/tests/`) | test_viewport.py::test_w2c_a_mint_id_parent_renders_exactly_as_its_address_twin -> conjunct (2) for zoom + viewport. No row for metrics / dashboard / default_roots / next_edges / conjunct (3): drafted below |

## What it shows
```
fm parents ──► loader.load_directory ──[post-pass: mint → address]──► Node.parents ──► zoom · metrics:183 · viewport · dashboard · dispatch · post_wire · chains:326   SAME (7/9 probed)
fm next_edges ──► (graph_core never reads it) ──► metrics:154-180 own parse · chains:88 own regex                                                                         DIFF (2/9)
sqlite ──► DBLoader (db_loader.py:50) ── bypasses the post-pass (not configured here)
```

## Test committed (strict xfail, RED until DG3 builds)
`extensions/agi/tests/test_viewport.py::test_w2ca_family_a_wires_a_mint_twin_as_its_address_twin_with_no_reader_resolving[parents]` -- metrics._load_graph children, dashboard dangling, default_roots equal on the twin; no family-A reader function mentions a mint id
`extensions/agi/tests/test_viewport.py::test_w2ca_family_a_wires_a_mint_twin_as_its_address_twin_with_no_reader_resolving[next_edges]` -- the next_edges child wires identically on the twin, with the same no-reader-resolves check
