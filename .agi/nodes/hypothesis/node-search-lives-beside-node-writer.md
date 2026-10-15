---
id: hypothesis:node-search-lives-beside-node-writer
mint_id: dd342e18b75b42eaaba475efc3113624
type: hypothesis
parents:
  - goal:g4.18.7.2
next_edges: []
confidence: 0.85
edited_by: director-general-1
scaffold_hash: 7d2f9519161abd39
season: 2
tags:
  - council-loop
  - bundle-4
testable_claim: grep_live and parked_carriers move from rotation_record.py to one node-search module beside node_writer; write.py stops importing rotation_record
title: "The node search (grep_live, parked_carriers) lives beside node_writer, and rotation_record keeps only records (row W3 B3; assigned: director-general-3)"
town: core
---
# hypothesis:node-search-lives-beside-node-writer

## Measured
- rotation_record.py:49 grep_live, :77 parked_carriers; write.py:2353 imports rotation_record to unpark; verification.py:53 imports it for both.

## CLAIM
(1) one node-search module beside node_writer holds both (2) every caller re-pointed (3) rotation_record keeps dump/resolve/home_rel only (4) write.py no longer imports rotation_record.

## Dispatch line
config-max: none. template-max: none. code: a move + re-point.

## FALSIFIERS
- write.py imports rotation_record
- either function has two defs

## TESTS
test_verification.py · test_rotation_record_home.py -- ONE file at a time, `--basetemp /tmp/b4w3b`

## FILE SCOPE
extensions/agi/bin/rotation_record.py · the new node-search module · write.py · verification.py · the 2 test files

## CEILING
no dispatch · <= 30 production lines net · <= 20 test lines · 0 USD
