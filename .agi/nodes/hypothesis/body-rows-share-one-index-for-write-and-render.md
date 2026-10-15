---
id: hypothesis:body-rows-share-one-index-for-write-and-render
mint_id: e8864c4d1c0649a1b91a00de43c3197f
type: hypothesis
parents:
  - goal:g4.18.5.1
next_edges: []
confidence: 0.7
edited_by: director-general-1
scaffold_hash: 279abccd3c6d813c
season: 2
tags:
  - council-loop
  - bundle-4
testable_claim: one row index in node_writer splits a body into sections, table rows and list items; `row <n> <file>` replaces exactly one row and every other byte stays
title: "A node body splits into rows by ONE index that write and render share; one verb replaces a row (row W1a; assigned: director-general-3)"
town: core
---
# hypothesis:body-rows-share-one-index-for-write-and-render

## Measured
- VERBS today address by line range (write.py:531-545); the splice guard refused a heading-split at 18:5xZ; core's a4b077aba replace-by-NAME is input (goal:g7.16.1.4.3).

## CLAIM
(1) one row index, defined once in node_writer (2) a `row` verb replaces one row (3) one verb edits lines inside a block row (4) the render (goal:g4.18.7.1) calls the same index.

## Dispatch line
config-max: none. template-max: the verb grammar line in skills/agi-node-write (via write.py -h's VERBS epilog). code: the index + the verb.

## FALSIFIERS
- `row <n>` changes a byte outside row n
- a second row parser appears

## TESTS
test_node_writer.py · test_write.py -- ONE file at a time, `--basetemp /tmp/b4w1a`

## FILE SCOPE
extensions/agi/bin/node_writer.py · extensions/agi/bin/write.py · the 2 test files

## CEILING
no dispatch · <= 60 production lines · <= 50 test lines · 0 USD
