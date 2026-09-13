# KID BRIEF — hypothesis:l4-spawn-without-name-defaults-to-the-seat-row-name-for-every-non-prime-post

THIS IS A BUILD ORDER (goal:g15.25), not a measurement. You MUST implement the
fix in `extensions/agi/bin/rotate.py`, add the tests, run them, and report.

## The defect (measured, twice)

`rotate.py:1619-1623` — `cmd_spawn` resolves the window name for EVERY spawn as:

```python
name = args.name
if not name:
    existing = _existing_windows(args.tmux_session or DEFAULT_TMUX_SESSION,
                                 args.window_path)
    name = _derive_successor_name(existing, prefix="belam")
```

It never looks at `--seat`. So `spawn --seat sanctuary-director` (a
non-prime post) comes up as a `belam-*` numeral window with no relation to the
row it was seated onto. The SM first seating on 2026-09-12 22:59Z came up as
`belam-S1-L4-XIX` and had to be killed and re-seated.

`rotate-self` (`cmd_rotate_self`, ~line 15124) already derives with
`prefix=seat`; the row resolver is `_find_seat(root, name)` (~line 2800) and
the role cell is `row.get("role")` (`prime_director` is the Prime chain).

## The rule to implement (row is the fact, NOT a config knob)

In `cmd_spawn`, the name block ONLY:

1. `--name` given → `name = args.name`, unchanged, always wins.
2. `--name` absent, `--seat X` names a row whose `role` is NOT
   `prime_director` → `name = X` (the row name, ONE window per post, no
   numeral).
3. `--name` absent, `--seat` names the Prime chain row (`role ==
   "prime_director"`) OR no `--seat` at all → byte-identical to today:
   `_derive_successor_name(existing, prefix="belam")`.
4. `--name` absent, `--seat X` names a row that exists but has NO `role`
   cell → fall back to today's derive AND print ONE line naming why (e.g.
   `spawn: seat 'X' has no role cell; deriving a belam numeral`).
5. `--name` absent, `--seat X` names NO row at all → today's derive
   (unchanged; `_find_seat` returns None).
6. `--dry-run` must print the resolved name on stdout so a test can read it
   with no tmux (add the print INSIDE the name block).

The row lookup needs `root` and `seat`. `root` is the `cmd_spawn` parameter;
`seat` is `getattr(args, "seat", None)`. Do the lookup in the name block even
though the later seat branch calls `_find_seat` again — the file scope is the
name block only.

## HARD CONSTRAINTS

- FILE SCOPE: `extensions/agi/bin/rotate.py` name block (around lines
  1619-1623) ONLY. Nothing else in rotate.py may move.
- CEILING: <= 15 lines net added to rotate.py. ONE test file, <= 4 tests.
  Prefer a new `extensions/agi/tests/test_spawn_name.py` unless test_rotate.py
  already has an obvious home; exactly one test file either way.
- TESTS (exactly these four, fixture `seats.md` with a director row and a
  `prime_director` row; reuse `_write_seats_sheet` / `_write_first_seating_
  rotations` from test_rotate.py if you import from it, else write the fixture):
  1. director seat + no `--name` → resolved name == seat
  2. prime_director row + no `--name` → `belam-S1-…` numeral as today
  3. no `--seat` → unchanged derive
  4. `--name` always wins even with a non-prime `--seat`
- No config:rotations line, no new flag, no new config key.
- DO NOT run git. No add, commit, push, stash, checkout.
- Run `python3 -m pytest extensions/agi/tests/test_rotate.py -q` AND your new
  test file. The spawn neighbourhood MUST be green. A failing assertion you
  did not expect is the assertion working — report it, do not delete it.

## What the node must carry (your evidence)

- the exact new bytes with file:line (the changed name block)
- the exact test command(s) and the pass/fail counts
- which conjunct each test proves
- any existing test that broke and how you fixed it (or why it was correct)

If you cannot fit the change inside the ceiling without touching more of
rotate.py, STOP at 2 attempts and report `pending` with the measured blocker —
do not sprawl.
