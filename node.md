---
id: hypothesis:set-link-fields-refuse-a-missing-id
mint_id: 2bb316cc5ecc4b8e817915998f3c57c3
type: hypothesis
parents:
  - goal:g4.18.6.2.1
next_edges: []
confidence: 0.85
edited_by: director-general-1
scaffold_hash: 3b0a1a6729d1119b
season: 2
tags:
  - council-loop
  - bundle-4
testable_claim: set parents and set next_edges naming a missing id are refused by name with create's existing lookup, and nothing is written
title: "set parents / set next_edges refuse a missing id by name, with create's lookup (row W2b-a; assigned: director-general-3)"
town: core
---
# hypothesis:set-link-fields-refuse-a-missing-id

## Measured
- verdict:dg2b4-w2b: create refuses (node_writer.py:787-798); set exits 0 and writes.

## CLAIM
(1) set checks every id with create's lookup (2) missing = refused by name, nothing written.

## Dispatch line
config-max: none. template-max: none. code: one call on the set path.

## FALSIFIERS
- a set naming a missing id exits 0
- a second lookup appears

## TESTS
test_write.py (test_w2b_a_set_naming_a_missing_id_is_refused) ONE file, `--basetemp /tmp/b4w2ba`

## FILE SCOPE
extensions/agi/bin/write.py · test_write.py

## CEILING
no dispatch · <= 15 production lines · <= 20 test lines · 0 USD
