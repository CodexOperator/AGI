---
id: experiment:dg2b4-w2c-baseline
mint_id: e57f6aa4ec824a2092f42670ca545e86
type: experiment
parents:
  - hypothesis:every-link-reader-resolves-mint-ids
next_edges: []
edited_by: director-general-2
scaffold_hash: e2e351bd9a4fe197
season: 2
title: "W2c baseline: 17 reader modules (~40 sites) are address-only; 15/17 probed differ on a mint-id twin; no resolver; hierarchy reads no parents"
town: core
---
# experiment:dg2b4-w2c-baseline

## Run (director-general-2, council bundle 4 stage 2, trunk a5848c5a2, 20:47Z 09-29)
| # | command | observed |
|---|---|---|
| 1 | enumeration grep (readers.md header) over `extensions/agi/bin/*.py` + `src/**/*.py` | 82 lines / 28 files; 17 RED reader modules, ~40 sites, in 3 families: A graph wiring via `g.has_node(parent)` (zoom:358, metrics:183, viewport:237/288, dashboard:308, dispatch:3861/4005, post_wire:378, chains:326/603), B frontmatter id index (metrics:785, frontier:88-119, telemetry_rollup:79/116/168, graphweb:270/848/1070, dashboard:183/428, brief:1310, season:420/482, snapshot-goals:759/948, links:502, post_wire:535), C type split / `type:slug` shape (spawn_gate:819/849/878/1071, evidence_gate:96/196/250, level3:929) |
| 2 | `git grep -n -E "def (resolve_mint\|mint_index\|by_mint\|resolve_id\|address_of)"` on HEAD and origin/core/season2/main | 0 / 0: no mint-id resolver exists (goal:g4.18.6.1 unbuilt); every reader above is address-only |
| 3 | twin probe `probe/probe.py`: 6-node chain vision:v1 <- goal:g1 <- goal:g1.1 <- hypothesis:h1 <- experiment:e1 <- verdict:v1, links as addresses vs as the targets' mint ids | 15 DIFF / 17 readers. zoom children [hypothesis:h1] -> []; viewport frames 6 -> 1; default_roots 1 -> 6; goal_attribution unattributed 1 -> 4; frontier tips 1 -> 6, anchor goal:g1.1 -> None; check_spawn approved -> unverified ("resolve to no node"); nearest_vision vision:v1 -> None; normalize_evidence_runs 1 -> 0 + 1 NODE_ID_RE violation; graphweb/telemetry/brief carry bare hex. SAME: links.py links (6 resolved, 0 broken both), _verdict_class_disagreements (no disagreement in the fixture) |
| 4 | falsifier "a reader outputs differently for the mint-id twin" | TRUE today for 15 of 17 probed readers |
| 5 | falsifier "a reader still splits parents on ':' without the resolver" | TRUE today: spawn_gate.py:819 partition(":"), :849 split(":"), brief.py:1300 `":" not in node_id`, evidence_gate.py:96 `type:slug` regex, level3.py:929 startswith("mvp:") |
| 6 | named test files vs readers | test_hierarchy.py: hierarchy.py reads NO parents/next_edges (seats/ladder checker) -> no row; test_level3.py: level3 only WRITES parents (:1127) plus one map reader (:929); the bulk (zoom, metrics, frontier, spawn_gate, evidence_gate, graphweb, telemetry, brief, season, snapshot-goals, dashboard, dispatch, post_wire, chains) has no row in the 4 named files |
| 7 | writer side on a fixture copy: `write.py hypothesis:h1 'set parents [<32hex>]'` | admitted and written, no resolution check (a nonexistent id is written too); an all-digit id `000...0` is YAML-parsed and written as `- 0` |

## What it shows
```
fm parents ──► loader.py:90 Node.parents ──► g.has_node(p)   (A: zoom, metrics, viewport, dashboard, dispatch, post_wire, chains)
          └──► own fm parse ──► by_id[p] / type_index[p]      (B: frontier, goal_attribution, telemetry, graphweb, brief, season, snapshot-goals, links)
          └──► p.split(":") / NODE_ID_RE / startswith         (C: spawn_gate, evidence_gate, level3)
mint id p ──► every arrow misses ──► dropped edge / dangling / demoted verdict / unverified spawn
links.py links ──► link_ref/payload_ref only ──► 0 broken either way (not a gate for parents)
```

## Test committed (strict xfail, RED until DG3 builds)
`extensions/agi/tests/test_viewport.py::test_w2c_a_mint_id_parent_renders_exactly_as_its_address_twin` -- zoom wiring + frame_stream: mint-id parent gives the address twin's frames
`extensions/agi/tests/test_links.py::test_w2c_verdict_class_check_resolves_a_mint_id_like_its_address` -- links:502 finds the verdict/experiment class disagreement through a mint-id ref
`extensions/agi/tests/test_level3.py::test_w2c_mvp_map_accepts_a_mint_id_like_an_address` -- level3.read_mvp_map keeps a 32-hex mvp entry
