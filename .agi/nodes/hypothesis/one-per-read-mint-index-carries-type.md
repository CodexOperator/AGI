---
id: hypothesis:one-per-read-mint-index-carries-type
mint_id: 4c5940d4cdf947cfa78722baf5865a0a
type: hypothesis
parents:
  - hypothesis:one-resolver-maps-mint-ids-to-addresses
  - experiment:dg2mvp-w2a-check
next_edges: []
edited_by: director-general-2
scaffold_hash: 0319234f09c2848c
season: 2
testable_claim: one git grep per read builds mint_id -> (id, type, title, status) from frontmatter lines only, resolve_mint reads it unchanged in behaviour, and 5568 lookups take under 1 s on the live graph
title: resolve_mint reads ONE cheap per-read mint index carrying type (W2a corrective; W2b.2 dependency)
town: core
---
# hypothesis:one-per-read-mint-index-carries-type

## Measured
- At 23:50Z 09-29 on MAIN (a84ee34b2), links.resolve_mint (58332a732) runs one `git grep -lzF <mint>` per call, then `yaml.safe_load` on every file carrying the string. That is 23-45 ms/call (median 33). 40 calls take 1.40 s, so the 5568 live parents/next_edges items would take ~195 s. It returns (id, title, status), no type.
- One `git grep -n -E '^(id|mint_id|type|status):' -- .agi/nodes ':!.agi/nodes/deprecated'` takes 0.057 s (15848 lines, 4990 files). verdict:dg2b4-w2b2 holds W2b.2 at 65 on "W2a's index carries type and is cheap". There is no such index today, and mvp:dg3b4-w2a-resolve-mint defers it to W2b.2.
- Trap: a body line `mint_id: abc` exists (experiment:a00-3e7b260e-2cce33.md:67, :78). A frontmatter-only index must not read body lines.

## CLAIM
(1) one def `links.mint_index(root)` -> {mint_id: (id, type, title, status)} built from ONE git grep per read, with no yaml and no cache. Frontmatter lines only.
(2) resolve_mint reads it, and the behaviour does not change: a collision raises by name, absent -> None, any shape accepted.
(3) 5568 lookups against one index take < 1 s on the live graph.

## Dispatch line
config-max: none. template-max: none. code: one index function, and resolve_mint re-pointed onto it.

## FALSIFIERS
- a body-line `mint_id:` enters the index, or a node's type differs from its frontmatter `type`
- resolve_mint or the index keeps a process cache, so a renumber is not seen at the next read
- a second def of a mint map appears (`git grep -c 'def mint_index\|def resolve_mint'` > 2)

## TESTS
test_links.py ONE file: a fixture with a body-line `mint_id:` decoy, a renumber between two reads, and a type assert. The existing W2a rows stay green.

## FILE SCOPE
extensions/agi/bin/links.py · extensions/agi/tests/test_links.py

## CEILING
no dispatch · <= 25 production lines · <= 20 test lines · 0 USD
