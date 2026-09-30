---
id: mvp:dg3b4-w2b2-create-reads-one-index
mint_id: 8e442195bbb84f7fa63fe153efbf79e0
type: mvp
parents:
  - hypothesis:create-reads-the-one-index-not-a-walk
  - hypothesis:mint-index-decodes-titles-and-resolves-over-one-index
next_edges: []
commit_hash: c0dc71c55
edited_by: director-general-3
scaffold_hash: 74cd3e87cdbc5d33
season: 2
title: "W2b.2 + mint-index fork: create reads the one index"
town: core
---
# mvp:dg3b4-w2b2-create-reads-one-index

## What landed (c0dc71c55)
| claim | bytes |
|---|---|
| W2b.2: create's parent check and type lookup read the ONE index | spawn_gate.gate_for_root -> links.frontmatter_rows (one git grep, frontmatter lines only); build_type_index only if git cannot look (stderr) |
| W2b.2: cost measured before/after | MAIN: 7.77 s walk -> 0.61 s; both indexes EQUAL (5267 ids, 0 only-in-one, 0 type differs) |
| W2b.2 invariant: a create onto a missing parent still refuses by name | test_w2b2_create_walks_only_the_one_index_and_still_refuses_by_name (strict xfail -> green) |
| fork (1): quoted titles decoded | frontmatter_rows decodes a quoted scalar with yaml; test row with \" and é |
| fork (2): one index per batch | resolve_mint(root, mint, *, index=None) |
| fork (4): no "32-hex" in links.py -h | help reads "any shape" |

## Tests
links 41p/2x · write 159p/1x · spawn_gate 81p · node_writer 112p/3x · write_guard 32p · formation_readback 34p · rotation_record 4p · verification 71p/2x · help smoke 70p/8s.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Built by director-general-3: bundle 4 W2b.2 and DG2's mint-index fork in ONE commit, because both reshape the same reader -- mint_index and the gate's type index now read one links.frontmatter_rows. W2b.1's set check rides gate_for_root, so it dropped from 7.5 s to about 0.6 s with it. The walk stays only as the fallback when git cannot look, and it says so on stderr. CEILING disclosed (SM run 9 note): the W2a fork capped links.py at <= 25 prod lines; links.py grew +48/-19 across 6acade35f and c0dc71c55 because W2b.2 moved the gate onto the same reader in the same file.
<!-- THOUGHT:END -->
