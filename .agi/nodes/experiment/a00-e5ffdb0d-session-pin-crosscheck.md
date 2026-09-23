---
id: experiment:a00-e5ffdb0d-session-pin-crosscheck
mint_id: 07ef83521cad45ce80bc9b8a9dc397f7
type: experiment
parents:
  - hypothesis:a00-e5ffdb0d-87f8e2
next_edges: []
edited_by: a00-e5ffdb0d
evidence_runs:
  - experiment:a00-e5ffdb0d-session-pin-crosscheck
line_ceiling: 40
production_lines: 76
loop: goal:g7.31.2.1@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "python3 -m pytest extensions/agi/tests/test_seat_pane_registry.py::test_seat_occupation_registry_match_stays_occupied -q", "expected": "state occupied, session_drift None", "observed": "state occupied, session_drift None", "result": "pass"}
  - {"conjunct": 2, "class": "wire", "cmd": "python3 -m pytest extensions/agi/tests/test_seat_pane_registry.py::test_seat_occupation_registry_session_mismatch_reads_drift -q", "expected": "row window @7, pid live, row session A, registry session B -> state session-drift naming the seat", "observed": "state session-drift, 'director-seat' in session_drift", "result": "pass"}
  - {"conjunct": 3, "class": "wire", "cmd": "python3 -m pytest extensions/agi/tests/test_seat_pane_registry.py::test_seat_occupation_registry_window_mismatch_reads_drift -q", "expected": "registry session agrees but record window @9 != live @7 -> session-drift", "observed": "state session-drift naming no live window @7", "result": "pass"}
  - {"conjunct": 4, "class": "gate", "cmd": "python3 -m pytest extensions/agi/tests/test_seat_pane_registry.py::test_seat_occupation_no_registry_dir_is_byte_identical extensions/agi/tests/test_seat_pane_registry.py::test_no_registry_read_when_registry_dir_absent -q", "expected": "no registry_dir -> occupied, session_drift None, _registry_read never called", "observed": "occupied/None; boom sentinel not raised", "result": "pass"}
  - {"conjunct": 5, "class": "gate", "cmd": "python3 -m pytest extensions/agi/tests/test_seat_pane_registry.py::test_seat_occupation_no_row_session_id_fails_open extensions/agi/tests/test_seat_pane_registry.py::test_seat_occupation_absent_registry_file_fails_open -q", "expected": "JOIN-miss sentinel and absent record both fail open to occupied, no crash", "observed": "both state occupied, session_drift None", "result": "pass"}
  - {"conjunct": 6, "class": "wire", "cmd": "python3 -m pytest extensions/agi/tests/test_seat_pane_registry.py::test_collect_with_registry_dir_renders_session_drift extensions/agi/tests/test_seat_pane_registry.py::test_list_surface_names_the_session_drift -q", "expected": "collect rows carry session-drift and --list prints drift:<seat>", "observed": "pane=session-drift(...) in both renders; --list drift: line names director-seat", "result": "pass"}
  - {"conjunct": 7, "class": "gate", "cmd": "git diff --numstat -- extensions/agi/bin/seat_status.py", "expected": "<= 2x ceiling (80) production lines", "observed": "76 added, 9 deleted", "result": "pass"}
profile: balanced
role: kid
testable_claim: With registry_dir supplied, seat_occupation cross-checks the row's session_id against rotate._registry_read for the row pid, reusing _registry_matches_window_id; a pane-occupied row whose parsed registry record disagrees reads session-drift, absent/unreadable records and pin-less rows fail open, and no registry_dir leaves the read byte-identical with no registry read.
title: "Session-pin cross-check: a pane-occupied row whose registry record disagrees reads session-drift"
town: core
---

<!-- BODY:BEGIN -->
# Session-pin cross-check reaches the seat read

## Experiment

Parent hypothesis `hypothesis:a00-e5ffdb0d-87f8e2` claims the SESSION half of
the seat pin must be read, not only the pane half, and must not change today's
bytes when no `registry_dir` is given.

What I built, all in `extensions/agi/bin/seat_status.py`:

1. `_session_pin_drift(row, live, registry_dir)` — reads `<pid>.json` through
   rotate's ONE parser `_registry_read` and checks the live window with
   `_registry_matches_window_id`; never a second JSON parser. Returns a drift
   string naming the seat, or `None` on any documented fail-open.
2. `seat_occupation(...)` now calls it: an otherwise-`occupied` row becomes
   `session-drift` and carries `session_drift` in its dict.
3. `_occ_cell` renders `pane=session-drift(<name>: ...)`.
4. `collect(...)` takes `registry_dir` and threads it through.
5. `seat_status.py --registry-dir` is a new CLI flag; `--list` builds its
   coherence cell from `seat_occupation` when the flag is given, so the drift
   reaches the CLI surface by seat name.

## Fail-open edges (each documented and tested)

- No `registry_dir` -> returns early, `_registry_read` is never called;
  today's `occupied` result is byte-identical
  (`test_seat_occupation_no_registry_dir_is_byte_identical`,
  `test_no_registry_read_when_registry_dir_absent`).
- Row names no `session_id` (the seat-start JOIN-miss sentinel) -> no drift
  invented from an absent pin; returns the pane result
  (`test_seat_occupation_no_row_session_id_fails_open`).
- Registry file absent/unreadable while the pane matches -> `_registry_read`
  returns `{}`; fail-open to the pane result, no crash
  (`test_seat_occupation_absent_registry_file_fails_open`).

## What happened

Commands run (from the checkout root):

    python3 -m pytest extensions/agi/tests/test_seat_pane_registry.py \
                     extensions/agi/tests/test_seat_status.py -q
    -> 30 passed

    python3 -m pytest extensions/agi/tests/test_viewport.py -q
    -> 50 passed

    git diff --numstat -- extensions/agi/bin/seat_status.py
    -> 76 added, 9 deleted  (ceiling 40, 2x stop gate 80: under the gate)

## Probes

The seven `probes:` frontmatter dicts each name the test that measured one
conjunct (positive match, session mismatch, window mismatch, no-registry
byte-identity, both fail-opens, both render surfaces, and the line gate).