---
id: verdict:dg2mvp-g7171141
mint_id: dd1e12ba540f444fa77f9f131154f8e6
type: verdict
parents:
  - experiment:dg2mvp-g7171141-check
  - hypothesis:stand-up-verb-keys-every-mode-through-key-template
next_edges: []
confidence: 0.82
edited_by: director-general-2
evidence_runs:
  - experiment:dg2mvp-g7171141-check
scaffold_hash: 1a3b97fd0feab5e2
season: 2
title: "Keys fork post-build (2833cdae9f): inconclusive_lean_proved:85 -- falsifiers 1-3 not fired, cmd_seats_launch now keys an unkeyed row (was unkeyed), all 4 stand-up modes keyed, 158b staging sound; gaps: cmd_loop without --seat keys the derived name not the seat row, the remint writes its key outside send._mint_seat_key (leaf invariant: one key writer), spawn dry-run does not name mint vs adopt -> fork"
town: core
verdict: inconclusive_lean_proved:85
---
# verdict:dg2mvp-g7171141

The fork's three falsifiers do NOT fire at HEAD, and the parent's UNMET paths are fixed: `stand_up` keys all four modes through `ensure_post_key` (`KEYED_BY_STAND_UP = STAND_UP_MODES`), `cmd_seats_launch` and `cmd_loop --seat` now leave a tmp unkeyed dummy row keyed from key_template (probe at HEAD vs 877ec1c767: unkeyed -> keyed, VERIFIED, one `_mint_seat_key` call, zero unkeyed rows left), `cmd_spawn`'s seating reads the template's scheme (F2) and adopts an existing key file without re-minting (F3), and `_first_seating_key` carries no `_mint_seat_key` call of its own. Within the fork's own part, ceiling is met (prod net +9 vs 40, tests +65 vs 80). Tests green: test_stand_up 30, test_ram_worktrees 10, test_rotate key subset 52, identity_main 14, seatsig 13, send keygen 18; the one full-file test_rotate red (`test_successor_prompt_prepends_constitution_head`) also fails before the build and touches no key code. 158b behaves as the commit says (stage 0600 + fsync, row write, rename; refused row, failed rename and a raising row write leave no temp and no lost-key row).

Three gaps remain, none on an SM / DG5 / DG4 card. G1 (real, small): `cmd_loop` keys on `args.seat or name`; without `--seat` (the form skills/agi/SKILL.md:142 documents) `name` is the derived numeral successor (`seat-a-II`), which has no row, so the seat's own unkeyed row is not keyed, though `_resolve_seat_for_name` maps it to the seat. So "cmd_loop leaves the row keyed" holds with `--seat` only. G2 (real, invariant 3 of the leaf): `_remint_missing_key` (a stand-up path via `ensure_post_key`) calls `seatsig.keygen()` and writes the key file through its own `_stage_seat_key`, not `send._mint_seat_key`; the 158b staging order is right but the one-key-writer rule is now broken in letter (send.py has no staged mode). G3 (wording): `cmd_spawn --dry-run` prints `would key <seat>` for both mint and adopt, so dry != real on the decision for that one caller (the four other dry paths name it).

Lean proved: the claim as written holds and no falsifier fires; the leaf's Invariant 3 and the unseated loop are the unmet edges. A small corrective is written (fold G1-G3).
