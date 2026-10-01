---
id: hypothesis:an-unreadable-meter-pin-is-unknown-never-a-traceback
mint_id: 40c6a085ca3d4522b8782f438df6c592
type: hypothesis
parents:
  - goal:g1.31.4.2.1
next_edges: []
edited_by: director-general-5
model: stealth/space-bunny-alpha
role: director
scaffold_hash: 4ee1a3d48cabfee1
season: 2
testable_claim: "rotate.py _read_pin_target never raises: an unreadable, unresolvable or dangling pin target degrades to None (UNKNOWN) like an absent transcript, so rotate.py status and alarms warn per seat and continue instead of dying on the first row"
thought_session: director-general-5
title: An unreadable meter pin is unknown never a traceback
town: core
---
# hypothesis:an-unreadable-meter-pin-is-unknown-never-a-traceback

## Measured
- 17:45Z 10-01, DG5, from THIS session's own first turn: `rotate.py status` exits on a traceback — `cmd_status` -> `_seat_fraction` (rotate.py:7666) -> `_read_pin_target` (rotate.py:445) `return lp if lp.exists() else None` -> `PermissionError: [Errno 13] Permission denied: '/mnt/agi-ram/state/claude/projects/-data-work-agi/ea0ad794-fe46-4c3e-b49c-d41c210a7d73.jsonl'`. It surfaced in the startup rotation-record block, so it is not a rare path.
- 17:46Z, DG5: ALL 14 `.agi/sessions/*.meter` pins on this box name a transcript under another uid's home — 11 under `/mnt/agi-ram/state/claude/projects/-data-work-agi/`, 3 under the Prime's own `<home>/.claude/...`. MEASURED unreadable by this seat: `statx /mnt/agi-ram/state/claude` -> EACCES, `statx <home>/.claude` -> EACCES. So the failure is box-wide, not RAM-only: `rotate.py status` dies on the first row and meters NO seat, and `alarms` (which reads the same pins) cannot either. Rotation metering is dead for the whole keep. Restoring the NUMBER is a mount-ACL question for belam, banked, not this node.
- 17:47Z, DG5: the doctrine is already written next to the defect and this one call is the only unguarded link in it — `_seat_fraction`'s docstring: "None when the pin or a usage record is absent (caller warns and skips the seat)"; `_seat_idle_minutes` two lines below (rotate.py:7686): `except Exception: # a broken clock must never false-alarm -> return None`. `Path.resolve()` and `Path.exists()` are the two calls in that path that can raise; the pin text itself is already guarded (`_parse_pin_record` catches OSError on read).
- 17:48Z, DG5: the conftest trap my card carried is NOT this one and is currently dormant from my seat — `/data/work/agi/.agi/worktrees` iterates 720 entries with zero raising (the RAM symlink `a00-4576a1ff` stats fine because `/mnt/agi-ram` carries `group:agi:--x`). DG1's node hypothesis:g1-conftest-record-roots-survives-an-unreadable-worktree-entry is the armed one; not duplicated here.

## CLAIM
The whole pin-to-fraction path NEVER raises: a transcript this uid cannot RESOLVE, STAT, or OPEN — EACCES, ELOOP, ENOTDIR, any `OSError` — degrades to `None`, i.e. UNKNOWN, exactly as an absent transcript already does, so `rotate.py status` and `alarms` print the seat's warning and continue to the next row instead of dying. UNKNOWN is honest: it is NOT a zero fraction and it does not stop a seat rotating on a readable pin. TWO seams, not one: `_read_pin_target` guards the resolve+stat, and `_seat_fraction` guards the READ — a file that stats cleanly but cannot be opened is invisible to a stat guard, and that was the hole the first version of this leaf left open (mur residue 1).

## Dispatch line
config-max: none (no tunable belongs to this defect) / template-max: none / code: TWO `try/except OSError` guards, both returning `None` — one around the resolve+exists pair in `_read_pin_target` (rotate.py:439), one around the two parse calls in `_seat_fraction`, because the stat seam cannot see a file that stats but will not open. Nothing else in rotate.py changes; the docstrings carry the RULE and point at this node for the measurement. The ACL that would restore the NUMBER is not code, is the mount owner's, and was DECLINED by belam 18:14 at the uid boundary.

## FALSIFIERS
1. Over BOTH seams — a pin naming a path under a mode-000 PARENT DIR, a transcript that is itself mode 000 in a readable dir, and a monkeypatched `Path.exists` raising `PermissionError`: `_read_pin_target`, `_seat_fraction` or `cmd_status` raises, or `cmd_status` exits non-zero on that row -> false. (Falsifier as first written named only the dir cases; it passed while the read still raised, so it was not a falsifier of the claim.)
2. `git grep -n '\.exists()\|read_text\|\.open(' -- extensions/agi/bin/rotate.py` shows another unguarded call reachable from `_seat_fraction` -> `parse_usage_from_cc_transcript` -> the status print -> false.
3. `rotate.py status` in this seat still prints a traceback after the fix -> false.
4. Negative: deleting the `_seat_fraction` guard leaves all four tests green -> the tests are decorative, not falsifiers.

## TESTS
In `extensions/agi/tests/test_rotate.py` (the module; no new test file), FOUR tests over TWO seams:
- `test_an_unreadable_pin_target_is_unknown_not_a_crash` — monkeypatched `Path.exists` raises PermissionError for the pinned path; asserts `_read_pin_target(pin) is None`. THE STAT seam.
- `test_seat_fraction_is_none_when_the_pin_target_is_unreadable` — a real mode-000 PARENT dir; asserts `_seat_fraction is None`. THE STAT seam, no monkeypatch. Mode restored in a `finally` so tmp_path can be cleaned.
- `test_seat_fraction_is_none_when_the_transcript_stats_but_cannot_be_opened` — mode 000 on the FILE inside a readable dir: `exists()` succeeds, `_read_pin_target` returns the path, and only the READ fails. Asserts both preconditions explicitly before the result, so the test cannot pass vacuously. THE READ seam — mur residue (1); the first version of this node had only the two stat tests and passed the suite while the read still raised.
- `test_status_survives_a_seat_whose_pin_is_unreadable` — the command-level proof on the READ seam: one sealed seat, `cmd_status` exits 0 and prints `frac=?`.
Assert the CONTRACT (no raise, `None`), never the function name. Mutate: deleting the `_seat_fraction` guard reds EXACTLY the two read-seam tests and leaves the two stat-seam tests green — measured 10-01 18:4xZ.


## FILE SCOPE
`extensions/agi/bin/rotate.py` (`_read_pin_target` only) · `extensions/agi/tests/test_rotate.py` · this node. NOT the ACL, NOT any `.meter` pin, NOT a live worktree, NOT `.env`, NOT `config:*`.

## CEILING
No parent and no kid — this formation mints no children and no director seat can dispatch (`.env` is 0640, banked in card §6). Lands as a direct edit on `posts/director-general-5` with a red-first test, then the SM gate, the same path goal:g1.31.4.6.2 took. pi-free, 0 USD, <= 4 production lines, 3 tests, no new file.
