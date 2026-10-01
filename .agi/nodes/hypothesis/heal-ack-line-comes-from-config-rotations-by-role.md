---
id: hypothesis:heal-ack-line-comes-from-config-rotations-by-role
mint_id: 9f097430380345e0b2a7dc69682f6d02
type: hypothesis
parents:
  - goal:g1
next_edges: []
edited_by: sanctuary-master
scaffold_hash: db2d84353e605c80
season: 2
testable_claim: heal builds a recovered seat's ack instruction from a config:rotations cell keyed by the row role, so a non-prime recovered seat is never told --gen and heal.py carries no ack text literal
title: "heal's recovered-seat ack line comes from config:rotations keyed by role: no --gen for non-prime seats"
town: core
---
# hypothesis:heal-ack-line-comes-from-config-rotations-by-role

## Measured
- heal.py `ack_gate` (both arms, RECOVERED and RESUMED) hard-codes `rotate.py ack --seat {seat} --gen {gen} --ref <ref> continue` into EVERY recovered seat's prompt; the agi-rotate skill §3 gives `--gen` to the recovery path, while non-Prime posts write no generation (master template §3: "Non-Prime posts write no gen N").
- The ack line is text a template owns, not code: it belongs in config:rotations keyed by role.
- Ordered by belam 19:0xZ 10-01 (direct message, relayed on doc:card-sanctuary-master §1).

## CLAIM
heal builds the recovered seat's ack instruction from a config:rotations cell keyed by the row's role (prime vs every other role), so a non-prime recovered seat is never told `--gen`; heal.py carries no ack text literal.

## Dispatch line
config-max: the ack line per role moves to a config:rotations cell / template-max: the recovered/resumed wording lives in that cell, not in heal.py / code: the lookup by row role, with a by-name refusal when the cell is absent.

## FALSIFIERS
- A recovered non-prime row's built prompt contains `--gen`.
- heal.py still contains the literal `rotate.py ack --seat`.
- The cell absent -> a silent empty prompt instead of a refusal by name.

## TESTS
A committed test building the prompt for a prime row and a director row from a fixture config:rotations (fakes only); the live config:rotations gains the cell in the same round (check the LIVE config holds it, not only the test fixture).

## FILE SCOPE
extensions/agi/bin/heal.py (`ack_gate` only) · .agi/nodes/.geometry/rotations.md (the one cell) · its test · this node.

## CEILING
1 pi-free parent · <= 12 production lines · 0 USD.
