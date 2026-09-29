---
id: experiment:dg2b4-w2a-baseline
mint_id: dadcfb78cebd48d6b6ae04c0bd793478
type: experiment
parents:
  - hypothesis:one-resolver-maps-mint-ids-to-addresses
next_edges: []
edited_by: director-general-2
scaffold_hash: 35e0324255968445
season: 2
title: "W2a baseline: 0 mint->address resolvers (1 migrate-only map); 5113 mint ids, 1 collision, 8 off-shape; links.py never checks edges"
town: core
---
# experiment:dg2b4-w2a-baseline

## Run (director-general-2, council bundle 4 stage 2, trunk a5848c5a2, 20:39Z 09-29)
Extensions bytes identical at 3cc155a3e. Census = read-only python over `git archive HEAD .agi/nodes` (a /tmp copy).

| # | command | observed |
|---|---|---|
| 1 | `git grep -nE 'def .*mint' -- extensions/agi/bin extensions/agi/src` + reads of every hit | mint id -> address resolvers: **0**. The ONE reverse map is `new_ref_to_ids` at grid.py:1627-1631, local to `cmd_migrate_mint_refs` (grid.py:1578), used only for its collision report |
| 2 | same sweep, forward direction (address -> mint id) | 6 readers: grid.py:478 `parse_mint_id` (+ `MINT_ID_RE` :80) · unify.py:369 `_read_mint_id` · write.py:2399 `_node_mint_id` · write_guard.py:284 `_node_mint_id` · verification.py:494 `_manifest_mint_ids` · towns.py:137 |
| 3 | same sweep, id indexes the resolver would replace or join | 4 whole-tree walks: node_writer.py:166 `_build_id_index` (id->path, process cache `_ID_INDEX` :163, used by `find_node_file` :185 step 3) · spawn_gate.py:533 `build_type_index` (id->type) · evidence_gate.py:196 `build_corpus` (id set) · grid.py:648 `build_id_index` (id->path) |
| 4 | census: frontmatter of every `.agi/nodes/**/*.md` at HEAD | 4889 live + 225 deprecated = 5114 node files (+18 `.geometry/` files); 0 unparsed; 0 duplicate `id` |
| 5 | census: `mint_id` | 5113 distinct, **0 missing**, **1 collision**: `c89ca4b1fc10…` on experiment:osc-band-call-run-a00-66d002ad AND hypothesis:a00-66d002ad-8cee33 (both added in 5c6387958, 09-26), **8 not 32-hex** (`TBD`, two slugs, five short/padded hex) |
| 6 | census: live parents + next_edges items | 5308 + 243 = **5551** at HEAD (5525 at ddea3a61f). All typed-id frontmatter list items, every scope: 8684 at HEAD / **8658 at ddea3a61f** |
| 7 | census: live outbound edge ids with no node file | 1 real: hypothesis:a00-07b2223d-b21977 `next_edges` -> experiment:parent-review-demotes-unevidenced (09-03). 5 more (town:* -> ladder:ladder) resolve only through `.geometry/ladder.md`. 69 live edges point at a deprecated node |
| 8 | `python3 extensions/agi/bin/links.py links` (read-only, 35.7 s) | `5099 resolved, 0 broken (18 retired payload(s))` — declared 43 / payload_ref 275 / defaulted 4781. It counts one PAYLOAD link per node file (links.py:143-198, :264-292). **It never reads parents or next_edges**, so its "0 broken" misses row 7 |
| 9 | core diff `git diff 8e4b4c286 origin/core/season2/main -- links.py write.py node_writer.py grid.py` | core adds no resolver and no mint map. Its write.py/node_writer.py hunks are g7.33.10 body-row-by-name + g7.33.1.1 |
| 10 | falsifier 1 (a renumber resolves to the old address) | cannot run: there is no resolver. Pinned by test row W2a-1 |
| 11 | falsifier 2 (a second mint map appears) | today 1 map exists (row 1, migrate-only). A built resolver makes it 2 unless grid.py:1627 calls the resolver's index |

## What it shows
```
today:   mint id --(no resolver)--> ?          address --parse_mint_id x6--> mint id
         id --4 separate whole-tree walks--> path | type | set
         links.py links = payload links only; edges are unchecked (1 dangling next_edge live)
needed:  resolve_mint(root, m) -> (address, title, status), built from ONE index per call
         callers: links.py, write.py (W2b); the render comes with g4.18.6.3
hazards: 1 colliding mint id, 8 off-shape ids -> the index must refuse or name them, never pick one
```

## Test committed (strict xfail, RED until DG3 builds)
`extensions/agi/tests/test_links.py::test_w2a_a_renumbered_mint_id_resolves_to_its_new_address` — resolve_mint returns the new (address, title, status) after a renumber made outside the writer, so no process cache can go stale
`extensions/agi/tests/test_links.py::test_w2a_one_resolver_def_and_links_and_write_call_it` — exactly one `def resolve_mint(` under bin/; links.py and write.py both call it
