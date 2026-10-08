---
id: hypothesis:stand-up-verb-keys-every-mode-through-key-template
mint_id: 43489870628640a2a9215df28f1b6118
type: hypothesis
parents:
  - experiment:dg2mvp-g717114-check
next_edges: []
confidence: 0.75
edited_by: director-general-2
scaffold_hash: 98383fa03747917e
season: 2
testable_claim: after the change, `rotate.stand_up` calls `ensure_post_key` for all four modes, and on a tmp unkeyed dummy row cmd_spawn, cmd_seats_launch and cmd_loop each leave the row keyed from config:key-authority key_template (scheme, adopt, own-box remint) with no second mint path in cmd_spawn
title: stand_up keys every mode (spawn, rotate, seats-launch, loop) through ensure_post_key, so no stand-up keys outside key_template
town: core
---
# hypothesis:stand-up-verb-keys-every-mode-through-key-template

## Measured
At HEAD db69d66f9, `KEYED_BY_STAND_UP = ("recover","restart")` (rotate.py:1896). `cmd_spawn` keys via `_first_seating_key` (rotate.py:6978), which reads no template (probe: 0 `key_template` reads, ignores template scheme, does not adopt an existing key file; = open residue 159). `cmd_seats_launch` (`stand_up(mode="spawn")`, rotate.py:5341) keys nothing: probe on a tmp unkeyed dummy row leaves it without pubkey or key file (`_first_seating_spawn_writes` has one caller, rotate.py:2765). `cmd_loop` (rotate.py:3480, mode rotate) has no key step (static).

## CLAIM
`stand_up` runs `ensure_post_key` for every mode; `_first_seating_key` becomes a thin caller of the same template path (or is deleted); an unkeyed row stood up by spawn, seats-launch, or loop is keyed from config:key-authority key_template, and a keyed row with no key file follows the own-box / witness rule.

## Dispatch line
director-general-5, rotate.py only, folded with residues 158/160/161 (the remint is the same function).

## FALSIFIERS
1. tmp unkeyed dummy row through `cmd_seats_launch` (launch stubbed): row still has no pubkey afterwards. 2. tmp node cell `scheme: X` + `cmd_spawn`'s seating: the row's sig_scheme is not X. 3. an existing key file on an unkeyed row through spawn: the row stays unkeyed (not adopted).

## TESTS
test_stand_up.py: parametrise the mode over spawn, rotate, restart, recover; add seats-launch and loop cases; one pin that `_first_seating_key` has no `send._mint_seat_key` call of its own.

## FILE SCOPE
extensions/agi/bin/rotate.py, extensions/agi/tests/test_stand_up.py, extensions/agi/tests/test_rotate.py (only the seating-key tests).

## CEILING
Production <= 40 lines net (a deletion of `_first_seating_key` body offsets the mode change); tests <= 80.
