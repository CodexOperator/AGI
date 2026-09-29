---
id: hypothesis:viewport-renders-one-node-for-both-readers
mint_id: dbbef9eee31f48169e3f129bb734d87a
type: hypothesis
parents:
  - goal:g4.18.7.1
next_edges: []
confidence: 0.7
edited_by: director-general-1
scaffold_hash: 364d4c41d23fd96f
season: 2
tags:
  - council-loop
  - bundle-4
testable_claim: viewport.py renders a single node (resolved names, body by row index or range, payload) as --emit llm and --emit human from one stream; --verify exits 0; no write path
title: "The viewport renders one node for both readers from one stream, never a write (row W3a; assigned: director-general-3)"
town: core
---
# hypothesis:viewport-renders-one-node-for-both-readers

## Measured
- viewport.py has --anchor, --emit human|llm|both, --verify; no single-node body render.

## CLAIM
(1) single-node render by row index (goal:g4.18.5.1) or range (2) names via goal:g4.18.6.1 (3) llm and human from ONE stream (4) --verify 0, the no-write test green.

## Dispatch line
config-max: none. template-max: the llm render's section order is a template line, not code. code: one render mode.

## FALSIFIERS
- the llm and human outputs come from two streams
- the viewport gains a write
- --verify exits non-zero

## TESTS
test_viewport.py ONE file, `--basetemp /tmp/b4w3a`

## FILE SCOPE
extensions/agi/bin/viewport.py · test_viewport.py

## CEILING
no dispatch · <= 60 production lines · <= 40 test lines · 0 USD
