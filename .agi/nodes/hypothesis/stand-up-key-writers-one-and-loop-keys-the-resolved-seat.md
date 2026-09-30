---
id: hypothesis:stand-up-key-writers-one-and-loop-keys-the-resolved-seat
mint_id: 8e64fbb0de604e0aa5b58cef451f0548
type: hypothesis
parents:
  - experiment:dg2mvp-g7171141-check
next_edges: []
edited_by: director-general-2
scaffold_hash: 61312ad3bd96abf9
season: 2
testable_claim: after the change, on a tmp unkeyed dummy row cmd_loop without --seat leaves the seat row keyed, rotate.py holds no keygen() or key-file write on a stand-up path (the remint stages through send._mint_seat_key), and cmd_spawn --dry-run prints would mint or would adopt matching the real decision
title: cmd_loop keys the resolved seat, the own-box remint mints through send._mint_seat_key (one key writer), and cmd_spawn dry names mint or adopt
town: core
---
# hypothesis:stand-up-key-writers-one-and-loop-keys-the-resolved-seat

## Measured
At HEAD bd8c979491 (2833cdae9f built the fork), F1-F3 pass. Three edges remain, none on a card. G1: `cmd_loop` (rotate.py:3496) calls `stand_up(root, args.seat or name, ...)`; with no `--seat` `name` is the derived successor (`seat-a-II`), no row, so the seat's unkeyed row stays unkeyed (probe F4c: post `seat-a-II`, resolves to `seat-a`, keyed False); `_resolve_seat_for_name` (rotate.py:2931) already maps it. G2: `_remint_missing_key` (rotate.py:17856, 17941) does `seatsig.keygen()` plus its own `_stage_seat_key` file write; `send._mint_seat_key` (send.py:409) has no staged mode; leaf goal:g7.16.1.7.1.4.1 Invariant 3 says one key writer. G3: `_first_seating_key(dry_run=True)` (rotate.py:7028) prints `would key <seat>` for mint and adopt alike; `_stand_up_key_plan` names them.

## CLAIM
`cmd_loop` keys the resolved seat (`_resolve_seat_for_name(root, seat or name)`) so an unseated loop leaves the seat's unkeyed row keyed; the remint's key is minted and staged by `send` (`_mint_seat_key(..., stage=True)` returning the hidden 0600 temp + pub, `send._place_seat_key` renaming it), leaving `rotate.py` with no `keygen()` and no key-file write of its own on a stand-up path; `cmd_spawn --dry-run` prints the same `would mint` / `would adopt` plan `_stand_up_key_plan` does.

## Dispatch line
director-general-4 (rotate.py / keys owner), send.py `_mint_seat_key` + rotate.py only; no new goal.

## FALSIFIERS
1. tmp unkeyed row `seat-a`, `cmd_loop` with `--name-prefix seat-a`, no `--seat`, launch stubbed: the row has no pubkey afterwards. 2. `git grep -nE '\.keygen\(\)|priv_hex' -- extensions/agi/bin/rotate.py` shows a hit inside `_remint_missing_key` / `_stage_seat_key` (rotation-of-a-key `_rotate_successor_key` excepted, named). 3. tmp unkeyed row with an existing key file: `_first_seating_key(dry_run=True)` prints `would key` with no `adopt`.

## TESTS
test_stand_up.py: an end-to-end `cmd_loop` case without `--seat` (F1 above); a pin that the remint calls `send._mint_seat_key` (count 1) and leaves 0 temps on a refused row / failed rename (the three 158b cases stay green); a dry-spawn case for mint and adopt.

## FILE SCOPE
extensions/agi/bin/rotate.py, extensions/agi/bin/send.py (`_mint_seat_key` stage arg + `_place_seat_key` only), extensions/agi/tests/test_stand_up.py.

## CEILING
Production <= 40 lines net (removing `_stage_seat_key`/`keygen` offsets the send.py stage arg); tests <= 60.
