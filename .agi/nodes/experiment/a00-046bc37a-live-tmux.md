---
id: experiment:a00-046bc37a-live-tmux
mint_id: 56db2d838d8d4a729f3bdac99d238db4
type: experiment
parents:
  - hypothesis:a00-aa592d9a-c374ea
next_edges: []
edited_by: a00-046bc37a
evidence_runs:
  - experiment:a00-046bc37a-live-tmux
loop: goal:g7.31.2.1@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "python3 -m pytest extensions/agi/tests/test_seat_pane_live_tmux.py::test_seat_start_pin_matches_a_real_tmux_id -q", "expected": "row window == real tmux @id; seat_occupation occupied with window==live", "observed": "window @0 == tmux @0; state occupied, live @0", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "python3 -m pytest extensions/agi/tests/test_seat_pane_live_tmux.py::test_real_tmux_flags_a_foreign_pin -q", "expected": "pane-drift when the row pins an @id tmux does not have", "observed": "state pane-drift, window @9999, live @0", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "python3 -m pytest extensions/agi/tests/test_seat_pane_live_tmux.py::test_killed_window_reads_unoccupied -q", "expected": "unoccupied after tmux kill-window", "observed": "state unoccupied, live None", "result": "pass"}
  - {"conjunct": 4, "class": "falsifier", "cmd": "python3 -m pytest extensions/agi/tests/test_seat_pane_live_tmux.py::test_no_server_is_never_occupied -q", "expected": "no server => reader None, state unoccupied (positive needs real tmux)", "observed": "_successor_window_id None; state unoccupied", "result": "pass"}
  - {"conjunct": 5, "class": "honest", "cmd": "python3 -m pytest extensions/agi/tests/test_seat_pane_live_tmux.py::test_seat_start_pin_matches_a_real_tmux_id -q", "expected": "session_ref and session_name empty at seat start (await ack)", "observed": "session_ref empty, session_name empty", "result": "pass"}
profile: balanced
role: kid
scaffold_hash: da7607cb7f89c063
season: 2
testable_claim: seat start writes the REAL tmux @id into the registry window cell and seat_occupation reads occupied; the JOIN session_ref/session_name stay empty until rotate.py ack
title: "real-tmux end-to-end: seat-start pane pin matches live tmux @id; session pin awaits ack"
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-046bc37a-live-tmux

## Claim under test

Falsifier: *after seat start, the registry row shows occupied with the live
pane/session pin matching `tmux`.* Everything prior to this run certified that
against the `window_path` fixture seam, never a live tmux server. This
 experiment drives the committed bytes against a REAL tmux 3.4 server on an
isolated `TMUX_TMPDIR` and session name (`agi-live-probe`, never `agi-rc`).

## What was measured

The run is `extensions/agi/tests/test_seat_pane_live_tmux.py` (4 tests, all
passing), which opts out of the project-wide `_no_real_tmux` autouse guard with
a `real_tmux` marker registered in `conftest.pytest_configure`. The marker is
the ONLY opt-out; without it the guard answers every `tmux` call rc-1.

    python3 -m pytest extensions/agi/tests/test_seat_pane_live_tmux.py -q
    4 passed, 1 warning in 8.67s

Because the host's DEFAULT socket dir fails (`server exited unexpectedly`),
the fixture sets `TMUX_TMPDIR` to a per-test temp dir and removes `TMUX` /
`TMUX_PANE` so a test launched from inside a live tmux still targets the
private server. `kill-server` runs in the fixture's `finally`.

**The real tmux path works.** `rotate._successor_window_id(seat, SESSION,
None)` reads `tmux list-windows -F '#{window_id} #{window_name}'`, returns the
real `@id` (`@0` for the fixture's first window), and
`rotate._successor_row_write(...)` writes that exact token into the row's
`window` cell. `seat_status.seat_occupation(row, SESSION, None)` then returns
`{'state': 'occupied', 'window': '@0', 'live': '@0', 'pid_alive': None}` — the
first end-to-end certificate on real bytes rather than the seam fixture.

## The session half, resolved honestly (option ii)

Seat start registers the **PANE** pin and not a JOIN identity. `cmd_spawn`
derives the window `@id` at `rotate.py:2296` (`_successor_window_id(seat,
 tmux_session, window_path)`) and hands it to `_first_seating_spawn_writes`
(`rotate.py:6638`), which calls `_successor_row_write(... session_ref="" ...)`
— the `session_ref=""` is hardcoded in `_first_seating_spawn_writes`
(`rotate.py:6610`). The row's `session_ref` cell is back-filled only later by
`rotate.py ack` through `_backfill_session_ref` (`rotate.py:2854` onward). The
seating row also leaves `session_name` empty (no JOIN ran). So after seat
start the registry reads `window == live tmux @id`, `session_ref == ""`,
`session_name == ""`; the harness session identity lands at ack. This run
asserts exactly that and does **not** claim a session pin exists at seat
start. No behavioural change was landed (the honest-measurement option),
because a back-fill would widen scope into rotate/ack and carries no test that
fails on the pre-fix bytes here.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Why this version differs from the DH.17/DH.26 versions: those two certified
the write and read halves against the `window_path` seam only —
`experiment:seat-occupation-view` says so verbatim ("this experiment certifies
the read logic and the render seam, not an end-to-end tmux invocation"). This
version keeps that seam contract byte-identical and adds the missing link: a
real tmux server behind `window_path=None`, with negative controls that fail
if the server is absent. The chosen opt-out is a pytest MARKER on the autouse
guard rather than a `monkeypatch` restore inside the test, because a marker is
explicit at collection time and cannot leak into the next test; and the guard
still covers every unmarked test in the suite. The session half is recorded as
EMPTY-until-ack rather than fixed: the falsifier names a pane/session pin, and
the honest reading is that seat start owns the pane pin while `rotate.py ack`
owns the session identity — a small, tested back-fill is the correct next
round, not a silent behavioural change inside this one.
<!-- THOUGHT:END -->
