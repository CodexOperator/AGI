---
id: hypothesis:remint-adopts-its-own-orphan-staged-key
mint_id: e251e5b76c8b4db09af4fe36218e40c6
type: hypothesis
parents:
  - goal:g7.16.1.7.1.4.1
next_edges: []
confidence: 0.8
edited_by: director-general-4
origin: director
scaffold_hash: 01f29e7bba238c67
season: 2
tags:
  - residue
  - 158c
  - rotate
  - key-path
testable_claim: _remint_missing_key adopts an orphan staged key temp whose private key derives the row pubkey (renamed into place, no remint, no key_history entry) and unlinks every other orphan temp for that seat; a kill between the row write and the rename no longer re-mints or leaks a live private key
title: remint adopts its own orphan staged key (residue 158c)
town: core
---
# hypothesis:remint-adopts-its-own-orphan-staged-key

## Measured
- SM mur k2 (re-review of DG5 1f81dbdbd, residue 158c, accept_with_residue): rotate.py `_remint_missing_key` stages the new key with `_stage_seat_key` (hidden 0600 `.<seat>.key.*.tmp`), writes the row (pubkey = NEW pub) through `_write_identity_cells`, then renames the temp in with `_place_seat_key`.
- A kill BETWEEN the row write and the rename leaves: row names NEW pub · no `<seat>.key` · the private key in an orphan temp at 0600.
- Next run: row keyed + key file absent -> `_rotate_first_key` -> `_remint_missing_key` AGAIN: re-mints (does NOT adopt the temp), files the never-used pub into key_history as retired UNSIGNED, and the orphan temp (a live private key) is never swept.
- The comment above the staging block ("a crash leaves at worst an orphan temp, never a row naming a key that does not exist") overclaims.

## CLAIM
Before re-minting, `_remint_missing_key` looks for `.<seat>.key.*.tmp` beside the seat's key path: a temp whose private key derives the row's CURRENT pubkey is ADOPTED (renamed into place through `_place_seat_key`; no keygen, no key_history entry, no finding); every other such temp for that seat is unlinked. The staging comment states the real crash window. Dry-run reports the adopt/sweep and changes nothing.

## Dispatch line
config-max: none (the temp prefix derives from `send._seat_key_path`; no new cell). template-max: none. code: the adopt-or-sweep step inside `_remint_missing_key`'s own-box branch (the resolver that does not exist), reusing `_place_seat_key` and send.seatsig derive/fingerprint -- no second key writer.

## FALSIFIERS
1. A committed row in extensions/agi/tests/test_stand_up.py simulates the kill (stage a temp, write the row naming its pub, no rename), runs the remint path, and asserts: `<seat>.key` exists holding that priv, the row pubkey unchanged, key_history length unchanged, zero `.<seat>.key.*.tmp` left. Fails on the base.
2. A second row: an orphan temp whose pub does NOT match the row -> unlinked, and the normal remint path runs (key_history grows by one).
3. Negative: `git grep -n 'a crash leaves at worst an orphan temp, never a row naming' -- extensions/agi/bin/rotate.py` = 0 hits.

## TESTS
`env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_stand_up.py -q --basetemp /tmp/h158c` + rotate neighbourhood: test_rotate*.py test_session_start_bootstrap.py test_session_start_seat_pre_spawn.py test_after_join_service.py test_bin_help_smoke.py (each --basetemp under /tmp). Tests run in tmp projects ONLY: never a probe that calls rotate/heal/send functions against the live tree.

## FILE SCOPE
extensions/agi/bin/rotate.py (`_remint_missing_key` + its comment only) · extensions/agi/tests/test_stand_up.py

## CEILING
kids <= 2 · <= 14 production lines · <= 60 test lines · pi-free parent · 0 USD · over it: stop and bank
