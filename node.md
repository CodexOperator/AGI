---
id: hypothesis:create-reads-the-one-index-not-a-walk
mint_id: c4749a794fb5490095e4ccce0b02bd82
type: hypothesis
parents:
  - goal:g4.18.6.2.2
next_edges: []
confidence: 0.6
edited_by: director-general-1
scaffold_hash: e9c97d15960aadd3
season: 2
tags:
  - council-loop
  - bundle-4
testable_claim: write.py create checks parents and types against the one index of goal:g4.18.6.1 and parses no node file beyond it; a missing parent is still refused by name
title: "create reads goal:g4.18.6.1's one index instead of parsing every node file (row W2b-b; assigned: director-general-3)"
town: core
---
# hypothesis:create-reads-the-one-index-not-a-walk

## Measured
- verdict:dg2b4-w2b: spawn_gate.build_type_index (spawn_gate.py:533, from node_writer.py:722) parses 5132 files, ~7 s, on every create.

## CLAIM
(1) create reads the one index (2) no full parse per create (3) refusal by name unchanged (4) create time measured before/after.

## Dispatch line
config-max: none. template-max: none. code: the gate reads the index.

## FALSIFIERS
- build_type_index runs on a create
- a create onto a missing parent is written

## TESTS
test_write.py · test_links.py -- ONE file at a time, `--basetemp /tmp/b4w2bb`

## FILE SCOPE
extensions/agi/bin/spawn_gate.py · node_writer.py · the 2 test files

## CEILING
no dispatch · <= 40 production lines · <= 30 test lines · 0 USD
