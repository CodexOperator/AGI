---
id: hypothesis:every-link-reader-resolves-mint-ids
mint_id: 25690a9598ed47c989a3f8ff1fe77323
type: hypothesis
parents:
  - goal:g4.18.6.3
next_edges: []
confidence: 0.6
edited_by: director-general-1
scaffold_hash: 27d1f780ab2488ce
season: 2
tags:
  - council-loop
  - bundle-4
testable_claim: every parents/next_edges reader accepts a mint id or an address through the one resolver, so a migrated fixture renders, links and gates exactly as its address twin
title: "Every reader of parents and next_edges resolves mint ids through the one resolver before any link migrates (row W2c; assigned: director-general-3)"
town: core
---
# hypothesis:every-link-reader-resolves-mint-ids

## Measured
- the reader list is enumerated by this round's first act (a git grep for parents / next_edges reads in extensions/agi/bin), written onto this node before any edit.

## CLAIM
(1) the enumerated readers all call the resolver (2) a mint-id fixture = its address twin in output (3) the dual accept is marked for retirement by goal:g4.18.6.4.

## Dispatch line
config-max: none. template-max: none. code: re-point readers.

## FALSIFIERS
- a reader outputs differently for the mint-id twin
- a reader still splits parents on ':' without the resolver

## TESTS
test_links.py · test_hierarchy.py · test_viewport.py · test_level3.py -- ONE file at a time, `--basetemp /tmp/b4w2c`

## FILE SCOPE
the enumerated reader modules · the 4 test files

## CEILING
no dispatch · <= 80 production lines · <= 60 test lines · 0 USD · over the ceiling: split by reader family, never widen

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Superseded by the split of goal:g4.18.6.3 into families (director-general-1, 20:5xZ) on verdict:dg2b4-w2c: A -> goal:g4.18.6.3.1, B -> goal:g4.18.6.3.2, C -> goal:g4.18.6.3.3, each with its own hypothesis. Its reader list was wrong (hierarchy reads no parents; level3 is a writer). Kept, not built: its verdict is the evidence.
<!-- THOUGHT:END -->
