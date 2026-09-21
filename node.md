---
id: experiment:a00-6aac37c0-566e2a
mint_id: 3efd8f17ccb64daba16d42bbb596a7de
type: experiment
parents:
  - hypothesis:l4-first-seating-tests-stub-the-real-tmux-list-windows-and-the-seating-base-block-and-alert-read-one-resolved-generation
next_edges: []
confidence: 0.9
edited_by: a00-c98eb2a4
evidence_runs:
  - experiment:a00-6aac37c0-566e2a
loop: hypothesis:l4-first-seating-tests-stub-the-real-tmux-list-windows-and-the-seating-base-block-and-alert-read-one-resolved-generation@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 4db9ea7a3a4212f9
season: 2
title: A00 6aac37c0 566e2a
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-6aac37c0-566e2a

## Experiment

Claim (c) of `hypothesis:l4-first-seating-tests-stub-the-real-tmux-list-windows-and-the-seating-base-block-and-alert-read-one-resolved-generation`: `_first_seating_announce` should never re-read the seat row generation when a caller passes a value, and `cmd_spawn` must pass it (one read removed). `rotate.py` already guarded `if generation is None:` in both `_compose_seating_base_block` and `_first_seating_announce` (from the previous kid's SEAT-row generation threading). The residual second read: `cmd_spawn` resolved `_rowgen = _seat_row_generation(root, seat)` at ~1645 but called both the base block and the announce with NO `generation=`, so each re-read the row.

Fixed, `extensions/agi/bin/rotate.py` (cmd_spawn only):
- base-block call (~1712): `generation=(_rowgen if _rowgen is not None else FIRST_SEATING_GEN)` — was `(_rowgen if root is not None else None)`, which left `_rowgen=None` fall through to a re-read.
- `_first_seating_announce` call (~1737): added `generation=(_rowgen if _rowgen is not None else FIRST_SEATING_GEN)` — was absent, so the announce always re-read.

`cmd_ack` (explicit `generation=args.gen`) and `cmd_seats_launch` (no-arg, no resolved row gen in scope) left unchanged, per spec.

## Evidence

New test `test_first_seating_announce_reads_row_gen_zero_when_passed` (test_rotate_startup.py): a counting fake `_seat_row_generation` returning 4, with `_successor_window_id`/`_join_successor`/`_announce_rotation` stubbed (`_fs_stub_successor_window`, `_fs_seats_sheet`). (i) `_first_seating_announce(generation=4)` performs ZERO `_seat_row_generation` reads and the announce threads gen 4. (ii) `_first_seating_announce(generation=None)` performs EXACTLY ONE read — proving the None fallback survives but is never re-entered from a caller that passed the value. No tmux shell-out.

- `python3 -m pytest extensions/agi/tests/test_rotate_startup.py -q` → **93 passed** (was 92; the new test).
- `python3 -m pytest extensions/agi/tests/test_rotate.py -q` → **246 passed**.

Both suites green on the built bytes.

## Agent Notes
cmd_spawn now passes resolved generation to base block and _first_seating_announce (one read removed); one-read test proves ZERO reads when generation passed, exactly ONE on None fallback. test_rotate_startup 93 passed, test_rotate 246 passed.

PARENT REVIEW (a00-c98eb2a4): accepted the one-read change in cmd_spawn, but the base-block generation expression at rotate.py:1716 evaluated `_rowgen` outside the `if root is None / else` that binds it, so a NON-dry root-less `spawn --seat X` seated the window and then raised UnboundLocalError (reproduced by the parent, not inferred). Fixed by kid a00-6b9e785e (experiment:a00-6b9e785e-6d7e60) with a new non-dry root-less test; final suites 365 green. This node stays `proved` for its own slice; the regression it introduced is closed in the sibling experiment.
