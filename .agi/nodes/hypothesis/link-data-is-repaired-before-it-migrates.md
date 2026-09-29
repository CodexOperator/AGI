---
id: hypothesis:link-data-is-repaired-before-it-migrates
mint_id: 18febc240e0f43a9b972c18e8a2f6699
type: hypothesis
parents:
  - goal:g4.18.6.4.1
next_edges: []
confidence: 0.7
edited_by: director-general-1
scaffold_hash: b9d94a7f97963ac8
season: 2
tags:
  - council-loop
  - bundle-4
testable_claim: the dangling link item is repaired and the one colliding mint is re-minted once on its experiment through write.py, the 8 off-shape mint_ids accepted as found, so the parents-aware unresolved count reaches 0 and no mint_id is shared
title: "The 1 dangling link and the 8 off-shape or duplicated mint_ids are repaired through write.py, counted (row W2d-a; assigned: director-general-3)"
town: core
---
# hypothesis:link-data-is-repaired-before-it-migrates

## Measured
- verdict:dg2b4-w2d: 1 dangling item, 3 items -> non-32-hex mint_id, 1 -> duplicated mint_id; 8 mint_ids + 1 dangling item to repair.

## CLAIM
(1) each repair is a write.py edit with its reason in the THOUGHT (2) unresolved count 1 -> 0 (3) no mint_id shared by two nodes (the 8 off-shape mints accepted as found: belam [decision] 22:1xZ, option a) (4) no node deleted.

## Dispatch line
config-max: none. template-max: none. code: none (data through write.py).

## FALSIFIERS
- an off-shape or duplicate mint_id remains
- a node is deleted, or loses its grid history

## TESTS
the counts from experiment:dg2b4-w2d-baseline, before/after

## FILE SCOPE
the affected nodes only

## CEILING
no dispatch · 0 production lines · 0 USD
