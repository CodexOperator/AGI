---
id: experiment:a00-dbcd3780-session-pin
mint_id: 6ca5d5dbaec548549d1904de6859b656
type: experiment
parents:
  - hypothesis:a00-dbcd3780-afb0ca
next_edges: []
confidence: 0.8
edited_by: a00-dbcd3780
evidence_runs:
  - experiment:a00-dbcd3780-session-pin
line_ceiling: 40
loop: goal:g7.31.2.1@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "scratch probe.py -> real rotate.cmd_spawn seating with window_path @7 director-seat and a registry dir whose record carries view:@7.%0 and session_id abcd1234-...; read the committed row back", "expected": "row window @7; row session_id == the registry session; state occupied; session_ok true", "observed": "row_window @7 row_session_id abcd1234-aaaa-bbbb-cccc-dddd12345678 state occupied session_ok true", "result": "pass"}
  - {"conjunct": 2, "class": "auth", "cmd": "seat_occupation on the same row with session_id forced to foreign-sid", "expected": "state occupied (pane half unaffected) but session_ok false, and the cell names session-drift", "observed": "state occupied session_ok false cell= pane=occupied(@7) session-drift(row foreign-sid live abcd1234-...)", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "a JOIN-miss seating (registry dir noreg) read back with the empty registry dir", "expected": "row session_id empty and session_ok null -- unknown, never a false true", "observed": "row_window @7 row_session_id  state occupied session_ok null", "result": "pass"}
  - {"conjunct": 4, "class": "gate", "cmd": "seat_occupation with no registry_dir supplied", "expected": "session_ok null and the rendered cell byte-identical to before", "observed": "session_ok null cell= pane=occupied(@7)", "result": "pass"}
production_lines: 69
profile: balanced
role: kid
scaffold_hash: 28cc57a20e5cb66f
season: 2
testable_claim: seat_status.seat_occupation consulted the seat registry for the live window @id and returns a three-valued session_ok (True match / False stale-or-empty / None unknown); a False is named in the rendered cell and no-registry renders are byte-identical
title: The occupation read names the session pin, not only the pane pin
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# The occupation read now names the session pin, not only the pane pin

## Experiment

Built the SESSION half of `goal:g7.31.2.1`'s falsifier on top of the landed
READ half (`seat_status.seat_occupation`, `pane_coherent`).

Pre-fix state (measured): `seat_occupation` certified `occupied` from the
pane @id and `pid` liveness alone. It accepted a `registry_dir` argument whose
docstring said it "is not consulted", so a row whose committed `session_id`
was stale, foreign, or empty (a seating JOIN miss) still read `occupied` with
the live window belonging to a DIFFERENT session. Falsifier clause "live
pane/**session** pin matching tmux" was unmet.

What was built, in `extensions/agi/bin/seat_status.py`:

- `_live_registry_session(registry_dir, window_id)` — ONE non-blocking scan
  of `<registry_dir>/*.json`, matching PARSED JSON through rotate's ONE
  matcher `_registry_matches_window_id` (never a substring join; `@7` cannot
  join `@70`). Never polls — a seating's bounded join already owns waiting.
  Returns the record's `session_id`, or `None` when no dir/record answers.
- `seat_occupation(..., registry_dir=)` now returns `session_id` (the row's),
  `live_session` (the registry's), and three-valued `session_ok`: `True` iff
  row session is non-empty and equals the registry's session for the LIVE
  window @id; `False` when the live session is known but the row's is empty
  or foreign; `None` (fail-open) when unknown.
- `_occ_cell` appends ` session-drift(row <x> live <y>)` ONLY when
  `session_ok is False`; an unknown or matching session adds no byte.
- `collect(..., registry_dir=)` threads the seam; the CLI gains
  `--registry-dir`.

## Evidence

Falsifier (`goal:g7.31.2.1`): after seat start, posts/seat registry shows
occupied with the live pane/session pin matching tmux.

Scratch probe `.agi/sessions/iter-DH.178/a00-dbcd3780/probe.py` drives a real
`rotate.cmd_spawn` seating end-to-end (window seam + per-session registry dir)
and reads the committed row back through `seat_status`. Four conjuncts, all
MEASURED on the built bytes:

    {"conjunct": 1, "class": "wire", "row_window": "@7",
     "row_session_id": "abcd1234-aaaa-bbbb-cccc-dddd12345678",
     "state": "occupied", "session_ok": true}
    {"conjunct": 2, "class": "auth", "state": "occupied",
     "session_ok": false,
     "cell": " pane=occupied(@7) session-drift(row foreign-sid live abcd1234-...)"}
    {"conjunct": 3, "class": "gate", "row_window": "@7",
     "row_session_id": "", "state": "occupied", "session_ok": null}
    {"conjunct": 4, "class": "gate", "session_ok": null,
     "cell": " pane=occupied(@7)"}

- conjunct 1 (wire): a JOIN HIT seating commits `window == "@7"` AND
  `session_id ==` the registry's session; the read returns `occupied` with
  `session_ok true`. The session pin matches tmux at seat start -- the
  falsifier clause that was open.
- conjunct 2 (auth): the same row with a foreign `session_id` still reads
  `occupied` on the pane, but `session_ok false` and the render NAMES it. This
  is the falsifier's exact failure mode, now visible instead of silent.
- conjunct 3 (gate): a JOIN-miss seating (empty registry) leaves `session_id`
  empty and reads `session_ok null` -- unknown, never a false `true`.
- conjunct 4 (gate): no registry dir supplied -> `session_ok null` and the
  cell is byte-identical to before (` pane=occupied(@7)`).

A seating whose joined pid is dead reads `pane-drift` regardless (measured
mid-probe: with registry file `12345.json`, `state` was `pane-drift`); the
session half is orthogonal and does not mask the pane/pid half.

Repo suite (the touched files):

    $ python3 -m pytest extensions/agi/tests/test_seat_pane_registry.py \
        extensions/agi/tests/test_seat_status.py -q
    26 passed, 18 warnings in 70.86s

5 new tests in `test_seat_pane_registry.py`: session-ok on a match,
session-drift on a foreign row, session-drift on an empty (join-miss) row,
fail-open `None` with no registry, and the collect/render seam naming only a
KNOWN drift.

Production lines: 69 added / 11 removed in
`extensions/agi/bin/seat_status.py` (`git diff --numstat`; test file
excluded). Ceiling 40; under the 80 = 2x stop line, recorded rather than
re-briefed.

Caveat: the session join reads the per-session registry DIRECTORY, not tmux
itself; and the row's short `session_ref` is still harness-only and empty at
seat start by design. The session pin that IS live at seat start is the
registry-joined `session_id`, which is what this read now checks.

## Probes

- conjunct 1 (wire): JOIN HIT seating -> row `session_id` == registry session
  and `session_ok true`.
- conjunct 2 (auth): foreign row session -> `session_ok false`, named in the
  rendered cell.
- conjunct 3 (gate): empty registry -> `session_ok null`, never true.
- conjunct 4 (gate): no registry dir -> no cell byte changes.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.178. Differs from the landed READ half (experiment:seat-occupation-view) in
exactly one place: `seat_occupation` now consults the `registry_dir` its own
docstring used to say was "not consulted", and returns the session half of
goal:g7.31.2.1's falsifier as three-valued `session_ok`. Chose a NEW optional
key plus a drift-only cell over changing `state`: `state` is the pane/pid
classification and overloading it with session drift would have broken the
byte-identical no-seam contract and every existing assertion. Chose a single
non-blocking registry scan (reusing rotate's ONE matcher) over rotating's
`_join_successor`, which polls and would block a read path. Measured mid-probe
that a JOIN-HIT row with a DEAD joined pid reads `pane-drift` regardless --
the session half is orthogonal and deliberately does not mask it. Deviation:
none. Production lines 69 vs ceiling 40 -- recorded, under the 80 = 2x stop
line, so no re-brief.
<!-- THOUGHT:END -->
