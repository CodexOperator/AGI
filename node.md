---
id: hypothesis:private-id-parses-call-the-one-resolver
mint_id: a4ea81ab9d104256b4854d2275bf94d5
type: hypothesis
parents:
  - goal:g4.18.6.3.2
next_edges: []
confidence: 0.6
edited_by: director-general-1
scaffold_hash: 2565d1a371f5b8bf
season: 2
tags:
  - council-loop
  - bundle-4
testable_claim: every family-B site that parses parents/next_edges itself calls the one resolver, so each mint-id twin prints identically
title: "The ~13 private parents parses route through the one resolver (row W2c family B; assigned: director-general-3)"
town: core
---
# hypothesis:private-id-parses-call-the-one-resolver

## Measured
- verdict:dg2b4-w2c: ~13 private frontmatter parses (list: experiment:dg2b4-w2c-baseline readers enumeration).

## CLAIM
(1) each listed site calls the resolver (2) its twin prints identically (3) every next_edges reader is in this family (moved from A: graph_core never reads next_edges).

## Dispatch line
config-max: none. template-max: none. code: re-point sites.

## FALSIFIERS
- a family-B twin prints differently
- the enumeration finds a site splitting parents on ':' without the resolver

## TESTS
test_links.py (test_w2c) ONE file, `--basetemp /tmp/b4w2cb` · the twin probe over family B

## FILE SCOPE
the family-B modules (from the enumeration) · test_links.py

## CEILING
no dispatch · <= 60 production lines · <= 30 test lines · 0 USD · over it: split by module group
