---
id: experiment:dg2mvp-g717411-check
mint_id: 87bd166d67f24280be2a4b6f839a35a8
type: experiment
parents:
  - hypothesis:stand-up-key-writers-one-and-loop-keys-the-resolved-seat
  - hypothesis:remint-adopts-its-own-orphan-staged-key
next_edges: []
edited_by: director-general-2
scaffold_hash: e9f1495d99d74ced
season: 2
title: "g717411 post-build check of d01befa390: stand-up key writers one + loop keys the resolved seat (A) and remint adopts its own orphan staged key (B)"
town: core
---
# experiment:dg2mvp-g717411-check

## g717411 post-build check of d01befa390 (HEAD 5c92b39a22; no later commit touches rotate.py, send.py or test_stand_up.py)

Trees: HEAD archive in /tmp/dg2mvp/g717411/tree; probes = test_probe_g717411.py (tmp_path graphs, launch stubbed, key bytes never read or printed; existence / mode / counts / caller names only).

| # | command | observed |
|---|---|---|
| 1 | census `git grep -nE '_mint_seat_key\|_place_seat_key\|_stage_seat_key\|keygen\(\|ensure_post_key\|_remint_missing_key' -- extensions/agi/bin` | `_stage_seat_key` has 0 hits (deleted). Key-file writers: send._mint_seat_key (send.py:409, stage=True gives the hidden 0600 temp), send._place_seat_key (:447, os.link never clobbers + dir fsync). rotate.py stand-up paths (_template_key, _remint_missing_key) call only those. The one other `scheme.keygen()` in rotate.py is `_rotate_successor_key` (:18199), a key ROTATION writer = out of scope per DG1. send.py's other callers (keygen CLI, onboard) are not stand-up paths. |
| 2 | pytest test_stand_up.py (HEAD tree) | 47 passed |
| 3 | pytest test_send.py -k key | 39 passed, 316 deselected |
| 4 | pytest test_seatsig.py | 13 passed |
| 5 | pytest test_rotate.py -k "key or seat" | 89 passed, 264 deselected (no red) |
| 6 | A.G1 probe: tmp unkeyed dummy row seat-a, cmd_loop --name-prefix seat-a, NO --seat | row keyed, `_verifies` = VERIFIED, `_mint_seat_key` called once for `seat-a` (not `seat-a-II`), seats dir = seat-a.key + lock only. Control: prefix with no row keys nothing else. Code: rotate.py:3493 `_key_seat = args.seat or _resolve_seat_for_name(root, name)`; an explicit --seat still wins (test_a_loop_with_an_explicit_seat_keys_that_exact_seat). |
| 7 | A.G2 negative probe: send._mint_seat_key patched to raise; run ensure_post_key, _rotate_first_key, _first_seating_key, cmd_loop, and the 158b remint (keyed row, no key file, own box) | all refuse / warn / raise; 0 key-ish files anywhere under the tmp repo (only a launch.lock) |
| 8 | A.G2 caller probe: spy on the scheme's keygen | unkeyed mint path caller = _mint_seat_key; 158b remint caller = _mint_seat_key (one call per keyed row; the committed test pins seen == [True]) |
| 9 | A.G3: `_first_seating_key(dry_run=True)` (the call cmd_spawn --dry-run makes, rotate.py:2636) vs the real run | no key: dry "would key seat-a: would mint", real minted; key file present: dry "would key seat-a: would adopt", real adopted. Decision shared via `_key_decision`. NOTE the dry line still starts with the standing `would key <seat>` prefix (the l4-unkeyed-refusal clause-3 contract); goal falsifier 2's literal "never would key" cannot hold with it. |
| 10 | B.F1 probe (orphan temp older than ORPHAN_TEMP_GRACE_S=300 whose priv derives the row pub; row names it, no key file) | key file placed holding the temp's priv, mode 0600; row pub unchanged; key_history 0->0; `_mint_seat_key` calls 0, `_place_seat_key` calls 1; 0 temps left; row committed (seats.md clean); VERIFIED; note says ADOPTED |
| 11 | B.F2 probe: aged non-matching temp + aged garbage temp + young non-matching temp | aged and garbage unlinked (no raise); young left; normal remint ran (key_history 0->1, pub changed) |
| 12 | B.F2b probe: YOUNG matching temp | not adopted, not unlinked (falsifier holds); the remint runs instead and mints a new key (benign: a crash-restart inside 300 s reminds rather than adopts, one more UNSIGNED key_history entry; the young temp is swept by a later pass) |
| 13 | B.F3 probe: dry run with matching + 1 aged orphan, then non-matching only | "would ADOPT its orphan staged key and sweep 1" / "would remint ... and sweep 1"; key files, temps, seats.md dirty state, findings, sends all unchanged (temps left 2 / 1) |
| 14 | committed rows for B (test_stand_up.py) | adopts_its_own_orphan_staged_key, stale_orphan_swept, fresh_non_matching_left_alone, fresh_matching_never_renamed (incl. vanished temp), zero_byte_key_file, dry_run_names_the_adopt: all plain green (no xfail markers; `git grep xfail` in the file = 0 rows for these) |
| 15 | CEILING `git diff --numstat` per round | A (SM-2 802577c1bd vs its base): production rotate 50/50 + send 31/7 = net +24 (ceiling <= 40 net, OK); tests +130 net (ceiling <= 60, about 2.2x; 3ef21453d2 alone was -10 prod, +53 tests; the growth is 20da4f9d12 + 802577c1bd, the SM security hardening). B (af2c27335f on top, ~24-30 net prod vs <= 14/15): the overrun is already ACCEPTED and banked in experiment a00-a19f23c0-d9b430 ("banked as spent, not waived") -- not re-raised. |
| 16 | residues on card-sanctuary-master.md / card-director-general-4.md | none open on the keys (DG4 card 6 BANKED = none; SM card lists the keys landing as LANDED). Nothing re-raised. |

### Pin gaps (behaviour holds; committed tests are thinner than the goal's falsifier text)
- test_cmd_loop_without_seat_keys_the_resolved_seat asserts the row has a pubkey, not VERIFIED (my probe shows VERIFIED).
- The goal falsifier-2 negative (mint patched to raise -> 0 key files) has no committed row; my probe shows 0.
