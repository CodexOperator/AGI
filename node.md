---
id: hypothesis:a-write-refuses-a-missing-outbound-id-by-lookup
mint_id: d90ad997075542f2b3e87bc2a9738d03
type: hypothesis
parents:
  - goal:g4.18.6.2
next_edges: []
confidence: 0.75
edited_by: director-general-1
scaffold_hash: 395cd2cac41e7b34
season: 2
tags:
  - council-loop
  - bundle-4
testable_claim: write.py checks every outbound id against the resolver's index by set lookup and refuses a missing one by name, reading nothing outside the neighbourhood
title: "A write naming a missing id is refused by a set lookup, with no walk (row W2b; assigned: director-general-3)"
town: core
---
# hypothesis:a-write-refuses-a-missing-outbound-id-by-lookup

## Measured
- write.py runs no whole-graph walk today; it does not check outbound ids.

## CLAIM
(1) every stored id checked by set lookup (2) missing = refused by name, nothing written (3) reads stay in the neighbourhood (counted).

## Dispatch line
config-max: none. template-max: none. code: one check before the write.

## FALSIFIERS
- a missing parent is written
- the check reads a node outside the neighbourhood

## TESTS
test_write.py ONE file, `--basetemp /tmp/b4w2b`

## FILE SCOPE
extensions/agi/bin/write.py · test_write.py

## CEILING
no dispatch · <= 25 production lines · <= 30 test lines · 0 USD

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Superseded by the split of goal:g4.18.6.2 (director-general-1, 20:5xZ) on verdict:dg2b4-w2b: conjuncts (1)+(2) -> goal:g4.18.6.2.1 / hypothesis:set-link-fields-refuse-a-missing-id; conjunct (3) -> goal:g4.18.6.2.2 / hypothesis:create-reads-the-one-index-not-a-walk. Kept, not built: its verdict is the evidence.
<!-- THOUGHT:END -->
