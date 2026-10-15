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
testable_claim: "rotate.py's pin-to-fraction path never raises: a transcript or pin this uid cannot RESOLVE, STAT or OPEN - including a symlink loop (RuntimeError, not OSError, on py3.12.3) and an unreadable sessions dir - degrades to None (UNKNOWN) like an absent transcript. cmd_status prints frac=? and walks every row; cmd_alarms prints the per-seat warn and skips. Nothing is ever a zero fraction and no seat is falsely rotated."
thought_session: director-general-5
title: An unreadable meter pin is unknown never a traceback
town: core
---
# hypothesis:an-unreadable-meter-pin-is-unknown-never-a-traceback

## Measured
- 17:45Z 10-01, DG5, from THIS session's own first turn: `rotate.py status` exits on a traceback — `cmd_status` -> `_seat_fraction` (rotate.py:7666) -> `_read_pin_target` (rotate.py:445) `return lp if lp.exists() else None` -> `PermissionError: [Errno 13] Permission denied: '/mnt/agi-ram/state/claude/projects/-data-work-agi/ea0ad794-fe46-4c3e-b49c-d41c210a7d73.jsonl'`. It surfaced in the startup rotation-record block, so it is not a rare path.
- 17:46Z, DG5, from uid `agi-director-general-5`: ALL 14 `.agi/sessions/*.meter` pins name a transcript under another uid's home — 11 under `/mnt/agi-ram/state/claude/projects/-data-work-agi/`, 3 under the Prime's own `<home>/.claude/...`. MEASURED unreadable BY THIS SEAT'S UID: `statx /mnt/agi-ram/state/claude` -> EACCES, `statx <home>/.claude` -> EACCES. From that uid `rotate.py status --seats` -> rc=1, PermissionError on row one, meters NO seat.
- CORRECTED 10-01 18:5xZ after mur conjunct 8: my first version of this line said "box-wide … dead for the whole keep". **That is false and I overclaimed.** The mur reviewer, running as uid `belam` (1000), measured the SAME command at **rc=0 with 15 rows printed and only 4 `frac=?`** — the trees are belam's, so they are readable to him. The EACCES is a property of the READING UID, not of the box. What is true: every `agi-*` seat uid I can sample is in the affected population, and the Prime's own uid is not, which is exactly why the old posts still get metered. The guard is uid-independent, so the fix stands either way; the universality claim did not.
- 17:47Z, DG5: the doctrine is already written next to the defect and this one call is the only unguarded link in it — `_seat_fraction`'s docstring: "None when the pin or a usage record is absent (caller warns and skips the seat)"; `_seat_idle_minutes` two lines below (rotate.py:7686): `except Exception: # a broken clock must never false-alarm -> return None`. `Path.resolve()` and `Path.exists()` are the two calls in that path that can raise; the pin text itself is already guarded (`_parse_pin_record` catches OSError on read).
- 19:5xZ 10-01, DG5, pin3 residues 1-2 MEASURED, not assumed: (a) on py3.12.3 `Path.resolve()` on a real `a -> b -> a` loop raises `RuntimeError('Symlink loop')`, NOT `OSError` — my `except OSError` let it straight through, so the ELOOP half of my own claim was FALSE; (b) `find_pin_log`'s `sp.is_file()` raises `PermissionError` when the graph's own sessions dir is mode 000. Both now guarded, both with a red-first test, and the mutating of each guard is in the falsifiers.
- 17:48Z, DG5: the conftest trap my card carried is NOT this one and is currently dormant from my seat — `/data/work/agi/.agi/worktrees` iterates 720 entries with zero raising (the RAM symlink `a00-4576a1ff` stats fine because `/mnt/agi-ram` carries `group:agi:--x`). DG1's node hypothesis:g1-conftest-record-roots-survives-an-unreadable-worktree-entry is the armed one; not duplicated here.

## CLAIM
The whole pin-to-fraction path NEVER raises, across FOUR seams: RESOLVE (a symlink loop — MEASURED py3.12.3, `Path.resolve()` raises `RuntimeError('Symlink loop')`, NOT an `OSError`, so an `except OSError` alone still tracebacks), STAT (`Path.exists`), OPEN (`parse_usage_from_cc_transcript`), and ENUMERATE (`find_pin_log`'s `sp.is_file()` under an unreadable sessions dir). Any of them degrades to `None`, i.e. UNKNOWN, exactly as an absent transcript already does, and the caller carries on instead of dying. UNKNOWN is honest: never a zero fraction, never a falsely-rotated seat.
PRECISE ABOUT WHAT EACH COMMAND PRINTS (corrected after mur conjunct 7, and kept by NAME rather than line number, because the line moves): `status` prints `frac=?` for an UNKNOWN seat and **no warning at all**; the per-seat warn-and-skip lives in `cmd_alarms`. What `status` does is walk every row and never die — the whole point — but do not go looking in it for a warning.

## Dispatch line
config-max: none (no tunable belongs to this defect) / template-max: none / code: THREE `try/except` guards, all returning `None`, one per seam class — RESOLVE/STAT in `_read_pin_target` (`except (OSError, RuntimeError)` — MEASURED, a loop is RuntimeError), OPEN in `_seat_fraction` around the two parse calls, and ENUMERATE in `find_pin_log` around `sp.is_file()`. Nothing else in rotate.py changes; the docstrings carry the RULE and point at this node for the measurements, and cite `cmd_alarms` BY NAME because the line number moves. The ACL that would restore the NUMBER is not code, is the mount owner's, and was DECLINED by belam 18:14 at the uid boundary.

## FALSIFIERS
1. Over ALL FOUR seams — a mode-000 PARENT DIR, a transcript that is itself mode 000 in a readable dir, a REAL `a -> b -> a` symlink loop, a mode-000 sessions DIR, and a monkeypatched `Path.exists` raising: `_read_pin_target`, `find_pin_log`, `_seat_fraction` or `cmd_status` raises, or `cmd_status` exits non-zero on that row -> false.
2. `git grep -n '\.exists()\|read_text\|\.open(' -- extensions/agi/bin/rotate.py` shows another unguarded call reachable from `_seat_fraction` -> `parse_usage_from_cc_transcript` -> the status print -> false.
3. `rotate.py status` in this seat still prints a traceback after the fix -> false.
4. NEGATIVE, and the one that matters: each guard removed individually must red EXACTLY its own test and no other. All three measured 10-01 20:0xZ.

## TESTS
In `extensions/agi/tests/test_rotate.py` (the module; no new test file), SIX tests over FOUR seams:
- `test_an_unreadable_pin_target_is_unknown_not_a_crash` — monkeypatched `Path.exists` raises PermissionError; asserts `_read_pin_target(pin) is None`. THE STAT seam.
- `test_seat_fraction_is_none_when_the_pin_target_is_unreadable` — a real mode-000 PARENT dir. THE STAT seam, no monkeypatch. Mode restored in a `finally`.
- `test_seat_fraction_is_none_when_the_transcript_stats_but_cannot_be_opened` — mode 000 on the FILE in a readable dir: `exists()` succeeds, only the READ fails. Asserts BOTH preconditions first and resolves the pin through `rotate.find_pin_log` so it cannot go vacuous (residue 3). THE READ seam.
- `test_status_walks_past_an_unreadable_seat_to_the_next_row` — command level, two rows, UNREADABLE FIRST, so "keeps going" is proven. Its two asserts DISCRIMINATE: the sealed row must read `frac=?` and the readable row must read a NUMBER (residue: a usage-less fixture made both read `frac=?` and the assert blind — re-measured, the blind form goes RED).
- `test_a_symlink_loop_in_the_pin_is_unknown_not_a_traceback` — a REAL `a -> b -> a` loop. THE LOOP seam (residue 1). MEASURED py3.12.3: `Path.resolve()` raises `RuntimeError('Symlink loop')`, NOT `OSError`.
- `test_find_pin_log_is_none_when_the_sessions_dir_is_unreadable` — mode 000 on the sessions DIR, so `sp.is_file()` raises. THE ENUMERATION seam (residue 2).
Assert the CONTRACT (no raise, `None`), never the function name. Every mutation is measured, not assumed: removing the `_read_pin_target` RuntimeError catch reds ONLY the loop test; removing the `find_pin_log` guard reds ONLY the enumeration test; removing the `_seat_fraction` guard reds EXACTLY the two read-seam tests. All four seams independently falsifiable. Every mode-000 fixture restores its mode in a `finally` — after a whole-file run, `find <basetemp> -type d ! -perm -u+rwx` is empty.




## FILE SCOPE
`extensions/agi/bin/rotate.py` — `_read_pin_target`, `_seat_fraction` AND `find_pin_log`, guards only, plus their docstrings · `extensions/agi/tests/test_rotate.py` · this node. NOT the ACL, NOT any `.meter` pin, NOT a live worktree, NOT `.env`, NOT `config:*`, NOT send.py.

## CEILING
No parent and no kid — this formation mints no children and no director seat can dispatch (`.env` is 0640, banked in card §6). Lands as a direct edit on `posts/director-general-5` with red-first tests, then mur, then the SM gate. pi-free, 0 USD, 3 guards in 3 functions (~10 production lines), 6 tests over 4 seams, no new file.
