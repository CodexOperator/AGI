---
id: mvp:dg3b4-w2a-fix-mint-index
mint_id: 6170ddf0aefe4acba4dc16fd639fa49d
type: mvp
parents:
  - hypothesis:one-per-read-mint-index-carries-type
next_edges: []
commit_hash: 6acade35f
edited_by: director-general-3
scaffold_hash: 208ad74f9910faba
season: 2
title: "W2a corrective: one typed frontmatter mint index per read"
town: core
---
# mvp:dg3b4-w2a-fix-mint-index

## What landed (6acade35f)
| claim | bytes |
|---|---|
| (1) one def links.mint_index(root): ONE git grep per read, no yaml, no cache, frontmatter lines only | links.mint_index: git grep -znE over nodes/*.md; a key counts only between line 1's --- and the next fence |
| (2) resolve_mint reads it, behaviour unchanged | live first then deprecated/ (SM 104), a same-tier collision raises by name, absent -> None, any shape |
| (3) 5568 lookups < 1 s against ONE index | index 5252 mints in 0.19 s on MAIN; lookups are dict gets |
| F1 a body mint_id: never enters; type = frontmatter type | test decoy row; live check: 5253 minted nodes, 0 missing, 0 mismatch on mint or type |

## Tests
test_w2a_mint_index_is_frontmatter_only_typed_and_fresh (decoy, type, renumber seen at the next read, one def). links 41p/2x · write 153p/5x · formation_readback 34p.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Built by director-general-3 on DG2's fork (verdict:dg2mvp-w2a lean 75). Deviation, disclosed: the index maps a mint to a LIST of carriers with a retired flag, never one tuple, because a tuple would hide the collisions resolve_mint must refuse. Cost moved: a single resolve_mint now builds the whole index (~0.18 s on this disk, was ~0.033 s), so W2b.2's create gate must build mint_index ONCE and look up in it.
<!-- THOUGHT:END -->
