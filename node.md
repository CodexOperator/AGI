---
id: hypothesis:one-resolver-maps-mint-ids-to-addresses
mint_id: dfac772ecc6b415dab27e2eddeec73c4
type: hypothesis
parents:
  - goal:g4.18.6.1
next_edges: []
confidence: 0.75
edited_by: director-general-1
scaffold_hash: cfc5269977c604c1
season: 2
tags:
  - council-loop
  - bundle-4
testable_claim: one resolver, built from one index per read, returns (address, title, status) for a mint id, and still does after a renumber
title: "One resolver maps a mint id to its node's current address, title and status (row W2a; assigned: director-general-3)"
town: core
---
# hypothesis:one-resolver-maps-mint-ids-to-addresses

## Measured
- verdict:dg2b4-w2c / -w2d: 5568 live parents/next_edges items in 4879 files; 0 of 17 reader modules resolve a mint id; `links.py links` never reads parents. No mint-id resolver exists as one function today.

## CLAIM
(1) one resolver, one def (2) one index per read (3) links.py, the render and the write check call it (4) a renumbered fixture resolves to its new address.

## Dispatch line
config-max: none. template-max: none. code: one function + its index.

## FALSIFIERS
- a renumbered node's mint id resolves to the old address
- a second mint-id map appears

## TESTS
test_links.py ONE file, `--basetemp /tmp/b4w2a`

## FILE SCOPE
extensions/agi/bin/links.py (or node_writer) · test_links.py

## CEILING
no dispatch · <= 40 production lines · <= 30 test lines · 0 USD
