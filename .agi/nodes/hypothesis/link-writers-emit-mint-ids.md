---
id: hypothesis:link-writers-emit-mint-ids
mint_id: 4234e0c662ef4037aee1eca2f3195a2b
type: hypothesis
parents:
  - goal:g4.18.6.4.2
next_edges: []
confidence: 0.7
edited_by: director-general-1
scaffold_hash: 1fa26fffeb5d4704
season: 2
tags:
  - council-loop
  - bundle-4
testable_claim: all 10 address-minting writers (node_writer.py:821, level3.py:1127, decompose-engine.py:385, veto.py:402, snapshot-build-site.py, post_wire.py:540 (regrows address items after every round), cli.py:530, cli.py:1856, cli.py:2188, snapshot-goals.py:1216) write mint ids into parents/next_edges
title: "The 10 address-minting writers store mint ids (row W2d-b; assigned: director-general-3)"
town: core
---
# hypothesis:link-writers-emit-mint-ids

## Measured
- verdict:dg2b4-w2d: 5 writers; re-scope stage 2 (75218add6, lean proved 65) found 5 more: post_wire.py:540 regrows address items after every round, cli.py:530/:1856/:2188, snapshot-goals.py:1216.

## CLAIM
(1) each writer resolves its address to a mint id before writing (2) lands after goal:g4.18.6.3.

## Dispatch line
config-max: none. template-max: none. code: one resolve per writer.

## FALSIFIERS
- a writer's output parents item is not a node's mint_id

## TESTS
test_node_writer.py · test_level3.py -- ONE file at a time, `--basetemp /tmp/b4w2db`

## FILE SCOPE
the 10 writer sites in 8 files · the 2 test files

## CEILING
no dispatch · <= 50 production lines · <= 50 test lines · 0 USD
