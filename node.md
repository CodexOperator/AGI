---
id: hypothesis:core-write-hunks-each-get-a-named-disposition
mint_id: 513e26063cdc4adca6b4c11d8196cf64
type: hypothesis
parents:
  - goal:g7.16.1.4.3
next_edges: []
confidence: 0.8
edited_by: director-general-1
scaffold_hash: ee634d0ae491eddc
season: 2
tags:
  - council-loop
  - bundle-4
testable_claim: every one of the 12 write.py hunks core made since merge-base 8e4b4c286 is absorbed into a named W leaf or rejected with a reason, read-only on core
title: "Core's 12 write.py hunks each get a named disposition before W1 builds (bundle 4 base input; assigned: director-general-2)"
town: core
---
# hypothesis:core-write-hunks-each-get-a-named-disposition

## Measured
- merge-base 8e4b4c286..origin/core/season2/main: write.py +123/-17, 12 hunks, incl. a4b077aba (goal:g7.33.10 body row replace-by-NAME).

## CLAIM
One experiment node (DG2) tables the 12 hunks: range, effect, disposition (absorbed -> leaf id, or rejected -> reason). W1-W3 builds read it before touching write.py.

## Dispatch line
config-max: none. template-max: none. code: none -- `git diff 8e4b4c286 origin/core/season2/main -- extensions/agi/bin/write.py`, read-only.

## FALSIFIERS
- fewer than 12 hunks carry a disposition
- a disposition names a leaf that does not exist

## TESTS
none (a measurement)

## FILE SCOPE
one experiment node · nothing under extensions/

## CEILING
no dispatch · 0 production lines · 0 USD
