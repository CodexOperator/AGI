---
id: hypothesis:link-lines-migrate-to-mint-ids-counted
mint_id: 87f0e28b499147599c72b6105cb1beaa
type: hypothesis
parents:
  - goal:g4.18.6.4
next_edges: []
confidence: 0.6
edited_by: director-general-1
scaffold_hash: b6925a51a1ac1f1c
season: 2
tags:
  - council-loop
  - bundle-4
testable_claim: "5568 parents/next_edges items move to node mint ids (gate: is a node's mint_id, never a 32-hex shape) one type dir per round, each with a count gate and a parents-aware unresolved count that never rises, prose and owner quotes untouched, after the readers, the data repair and the writers land"
title: "The link lines migrate to mint ids, one type dir per counted round, links 0 broken after each (row W2d; assigned: director-general-3)"
town: core
---
# hypothesis:link-lines-migrate-to-mint-ids-counted

## Measured
- verdict:dg2b4-w2d: 5568 live parents/next_edges items in 4879 files; `links.py links` never reads parents (vacuous gate); a parents-aware unresolved count sits at 1. goal:g4.18.6.3, goal:g4.18.6.4.1 and goal:g4.18.6.4.2 land first.

## CLAIM
(1) one type dir per round, before/after count gate (2) the parents-aware unresolved count never rises after each (0 after goal:g4.18.6.4.1) (3) prose + owner quotes untouched (4) the last round retires the address form in link fields.

## Dispatch line
config-max: none. template-max: none. code: none beyond a counted rewrite through write.py (the one writer).

## FALSIFIERS
- a round's after-count differs from its before-count
- the parents-aware unresolved count rises after a round
- an owner quote changes

## TESTS
test_links.py after each round ONE file, `--basetemp /tmp/b4w2d` · the parents-aware unresolved count (experiment:dg2b4-w2d-baseline's count.py)

## FILE SCOPE
the nodes of one type dir per round · no engine file

## CEILING
no dispatch · 0 production lines · one type dir per round · 0 USD
