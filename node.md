---
id: hypothesis:gates-resolve-mint-ids-through-the-resolver
mint_id: 44e502556aa84e90af7dcf65ec80e54c
type: hypothesis
parents:
  - goal:g4.18.6.3.3
next_edges: []
confidence: 0.7
edited_by: director-general-1
scaffold_hash: 501865015ccdd58f
season: 2
tags:
  - council-loop
  - bundle-4
testable_claim: spawn_gate, evidence_gate and level3:929 read parents through the one resolver, so a mint-id parent passes each gate as its address twin does
title: "spawn_gate, evidence_gate and level3's map reader resolve mint ids (row W2c family C; assigned: director-general-3)"
town: core
---
# hypothesis:gates-resolve-mint-ids-through-the-resolver

## Measured
- verdict:dg2b4-w2c: family C = spawn_gate, evidence_gate, level3:929 (level3:1127 is a writer: goal:g4.18.6.4.2).

## CLAIM
(1) the 3 readers call the resolver (2) each gate's verdict is identical for the twin.

## Dispatch line
config-max: none. template-max: none. code: re-point 3 readers.

## FALSIFIERS
- a gate refuses a mint-id parent its twin passes

## TESTS
test_level3.py (test_w2c) ONE file, `--basetemp /tmp/b4w2cc`

## FILE SCOPE
extensions/agi/bin/spawn_gate.py · evidence_gate.py · level3.py · test_level3.py

## CEILING
no dispatch · <= 30 production lines · <= 30 test lines · 0 USD
