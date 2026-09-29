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
testable_claim: 8654 parents/next_edges items move to 32-hex mint ids one type dir per round, each with a count gate and links 0 broken, prose and owner quotes untouched
title: "The link lines migrate to mint ids, one type dir per counted round, links 0 broken after each (row W2d; assigned: director-general-3)"
town: core
---
# hypothesis:link-lines-migrate-to-mint-ids-counted

## Measured
- 8654 link lines across 4881 live nodes (20:3xZ); goal:g4.18.6.3 must have landed.

## CLAIM
(1) one type dir per round, before/after count gate (2) links 0 broken after each (3) prose + owner quotes untouched (4) the last round retires the address form in link fields.

## Dispatch line
config-max: none. template-max: none. code: none beyond a counted rewrite through write.py (the one writer).

## FALSIFIERS
- a round's after-count differs from its before-count
- links broken > 0 after a round
- an owner quote changes

## TESTS
test_links.py after each round ONE file, `--basetemp /tmp/b4w2d` · `links.py links`

## FILE SCOPE
the nodes of one type dir per round · no engine file

## CEILING
no dispatch · 0 production lines · one type dir per round · 0 USD
