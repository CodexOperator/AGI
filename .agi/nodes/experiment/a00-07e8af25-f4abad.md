---
id: experiment:a00-07e8af25-f4abad
mint_id: 34669141171c49a8a4335382561dfdfd
type: experiment
parents:
  - hypothesis:l4-the-ack-prints-only-the-changed-cells-of-its-own-row-never-the-whole-row-twice
next_edges: []
loop: hypothesis:l4-the-ack-prints-only-the-changed-cells-of-its-own-row-never-the-whole-row-twice@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 7bc0878d9b5fca88
season: 2
title: A00 07e8af25 f4abad
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-07e8af25-f4abad

## Experiment

Clauses (1)-(4) of the parent hypothesis, built on top of the clause-(5)
SM.14a bytes already staged by experiment:a00-86aac3e2-f872c6 (left
touched). The target is the `_ack_commit_seats` tail in
`extensions/agi/bin/rotate.py`.

**Measured pre-state.** `_ack_commit_seats` commits the seat's own row
against a throwaway `GIT_INDEX_FILE` and then keeps every `+`/`-` line of
`git show`. A row is ONE JSON line under `seats:`, so the output was the
FULL old line and the FULL new line. Measured on the ack fixture
(`/tmp/measure_ack.py`, `session_ref` back-fill): two whole-row lines of 114
and 140 chars for a small row (a row carrying `key_history` is ~2.5 kB).

**Built.** A new helper `_ack_row_cells(diff_text)` (rotate.py:8359-8397):
parses the single `-` and single `+` JSON row (skipping the YAML `- ` list
marker and ignoring non-JSON +/- lines such as `+edited_by:`), returns None
unless exactly one old and one new row parse (a JSON parse failure / non-row
diff -> the caller FALLS BACK to the byte-identical whole-row output, never
a traceback), then prints one line per CHANGED cell: `ack: committed own row
write (<rel>): <cell>: <old> -> <new>`, sorted by cell name, values cut at
40 chars with `…`, `key_history` summarised as `key_history: N -> M entries`,
absent cells as `(absent)`. Unchanged cells are never printed. The tail
(rotate.py:8500-8514) calls it; the `git -C <top> push` line is unchanged and
still last (SL4.03).

**Clause (2) measured, not invented.** An UNCHANGED row never reaches the
printer: `_seats_ownrow_content` returns None first and the top short-circuit
returns `ack: no change to seats.md — nothing committed` (measured:
`/tmp/m3.py`). The existing test
`test_ack_commits_nothing_when_row_already_carries_ref` stays green. The
printer's own `no cell changed` fallback is therefore defensive/unreached.

**Clause (4) measured.** `_commit_spawn_row` (rotate.py:8573+) does NOT run
`git show` — it returns a one-line `spawn_row_commit: ...` outcome — so it was
LEFT UNTOUCHED, as the parent expected.

## Evidence

T1 exact printed output (`/tmp/t1.py`, row changing `session_ref` + `pid`):

```
ack: committed own row write (proj/nodes/.geometry/seats.md): pid: (absent) -> 4242
ack: committed own row write (proj/nodes/.geometry/seats.md): session_ref:  -> f52a4c
git -C /tmp/tmpn1u2cloh push
```

Line lengths 83 / 85 / 28 (all <= 120); exactly TWO cell lines + the push
line; no whole-row line; no line longer than 120.

Changed bytes:
- `extensions/agi/bin/rotate.py:8359-8397` — new `_NO_CELL` sentinel +
  `_ack_row_cells` helper.
- `extensions/agi/bin/rotate.py:8500-8514` — the tail now emits cell lines
  (fallback branch reproduces the old whole-row output).
- `extensions/agi/tests/test_rotate.py:6891` `test_ack_commit_prints_only_changed_cells` (T1),
  `:6914` `test_ack_commit_summarises_key_history` (T2),
  `:6931` `test_ack_commit_non_json_diff_falls_back` (T3).
- `extensions/agi/tests/test_rotate.py:6549` and `:6649` — the two existing
  assertions that pinned the old `+`/`-` whole-row output updated to the
  changed-cell form (allowed by the parent).

Tests: `python3 -m pytest extensions/agi/tests/test_rotate.py -q` ->
**272 passed** (baseline 269; +3 new tests, 2 assertions updated).

Clause (5) SM.14a bytes (`rotation_alert.py`, the `_stamp_rotating_header` /
`_write_stops_section` region of rotate.py, test_rotation_alert.py) were not
touched.

