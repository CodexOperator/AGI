---
id: experiment:a00-4c8d9dd8-real-tmux
mint_id: bdf3f7019ae74e068b289d46569b7149
type: experiment
parents:
  - hypothesis:a00-4c8d9dd8-6f89c2
next_edges: []
edited_by: a00-44d4d8b5
evidence_runs:
  - experiment:a00-4c8d9dd8-real-tmux
line_ceiling: 40
loop: goal:g7.31.2.1@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "python3 probes_real_tmux.py -> rotate._successor_window_id('director-seat', <real session>, None); SS.seat_occupation(row window=real @id, pid=os.getpid(), None)", "expected": "derived @id == the @id real tmux reports; state occupied; live == real", "observed": "derived=@151 real=@151 state=occupied live=@151 pid_alive=true", "result": "pass"}
  - {"conjunct": 2, "class": "wire", "cmd": "python3 probe_row_cells.py -> rotate.cmd_spawn(args tmux_session=<real session>, window_path=None) with only spawn_window stubbed (creates a REAL tmux window)", "expected": "committed row window == the @id real tmux reports; occupation occupied", "observed": "rc=0 row_window=@154 tmux_real=@154 window_matches_tmux=true", "result": "pass"}
  - {"conjunct": 3, "class": "auth", "cmd": "python3 probes_real_tmux.py -> SS.seat_occupation(row window=@999999) while the real seat window @151 is live; and with only a foreign window somebody-else present", "expected": "pane-drift naming the mismatch, never occupied", "observed": "state=pane-drift live=@151", "result": "pass"}
  - {"conjunct": 4, "class": "gate", "cmd": "python3 probes_real_tmux.py -> tmux kill-window <session>:director-seat, then SS.seat_occupation(row window=the @id that was occupied one moment earlier)", "expected": "the pin no longer answers: unoccupied, live null (liveness is read, not cached)", "observed": "state=unoccupied live=null", "result": "pass"}
  - {"conjunct": 5, "class": "gate", "cmd": "python3 probes_real_tmux.py -> shutil.which('tmux')=None, then SS.seat_occupation(window_path=None)", "expected": "None (fail-open, no crash)", "observed": "state=null", "result": "pass"}
  - {"conjunct": 6, "class": "auth", "cmd": "python3 probe_row_cells.py -> read every cell of the seat-start row; assert no cell carries the tmux SESSION name and the three session identity cells are empty", "expected": "session_ref/session_name/session_id empty at spawn; no cell contains the tmux session name", "observed": "row_session_ref='' row_session_name='' row_session_id='' row_carries_tmux_session_name=false session_cells_empty_by_design=true", "result": "pass"}
  - {"conjunct": 7, "class": "gate", "cmd": "python3 -m pytest extensions/agi/tests/test_seat_pane_real_tmux.py -q  (first draft, project-wide _no_real_tmux guard active, no override)", "expected": "the real-tmux assertions FAIL with the binary stubbed, proving they are not vacuous", "observed": "6 failed, 1 passed (the 1 passer was unoccupied-for-the-wrong-reason); with the scoped override 7 passed", "result": "pass"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 898d0fc2c63fec6b
season: 2
testable_claim: A spawn-only seat start writes its row window cell from the live tmux @id, and seat_occupation against the real binary is occupied and names drift/unoccupied/fail-open; the session identity cells are empty at spawn by design and no row cell carries the tmux session name.
title: "Seat-start occupation against REAL tmux: pane pin matches the binary, session cells empty by design"
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-4c8d9dd8-real-tmux

## Experiment

DH.83 removes the `window_path` stub that every earlier test on
`goal:g7.31.2.1` used. `extensions/agi/tests/test_seat_pane_real_tmux.py`
creates a throwaway tmux session (unique name, killed in teardown), names a
window for the seat, and calls `rotate._successor_window_id` /
`seat_status.seat_occupation` / `seat_status.pane_coherent` with
`window_path=None`, so they execute `/usr/bin/tmux` 3.4 itself. It also drives
`rotate.cmd_spawn` end-to-end with a real tmux window, stubbing ONLY the
process-launch boundary (`spawn_window`) — the pin derivation afterwards reads
the real binary. No engine code changed.

    $ python3 -m pytest extensions/agi/tests/test_seat_pane_real_tmux.py \
        extensions/agi/tests/test_seat_pane_registry.py \
        extensions/agi/tests/test_seat_status.py -q -p no:warnings
    28 passed in 43.53s

A real window is reported by tmux as `@154`; the seat-start row committed
`window: "@154"` and a real-tmux occupation read of that row returned
`occupied`. The negative probes below (foreign window, stale pin, window
killed after the pin, tmux unavailable) all returned the drift/unoccupied/
fail-open answers the contract names.

## The session half of the falsifier — settled, not papered over

The falsifier reads "the live pane/session pin matching `tmux`". Measured at a
spawn-only seat start, through the real code:

- `window` (`@<N>`, the tmux PANE @id) is the ONLY cell that matches tmux. It
  is written from `_successor_window_id` reading the live binary.
- `session_ref` is the ListAgents `@id` of the successor session — EMPTY by
  design at spawn, because the spawner cannot know it. It is back-filled by
  `rotate.py ack --ref` (`_backfill_session_ref`).
- `session_name` is the harness registry name (e.g. `agi-d7`), also EMPTY at
  spawn and back-filled by the SAME ack from the registry JOIN.
- `session_id` is the harness Claude-Code session UUID. At spawn it comes from
  the registry JOIN keyed on the `window` @id (`_join_successor`), never from
  tmux; on a join miss it commits EMPTY.
- NO cell carries the tmux SESSION name (here `agi-rtt-…` / in production
  `agi-rc`). The tmux session name is a spawn parameter, never row state.

So a spawn-only seat start CANNOT carry a "session pin" that matches the tmux
session, and does not claim to. The falsifier is satisfied on its PANE half
(registry `window` == live tmux @id, state occupied) and UNSETTLED on its
session half by construction: the session identity arrives later, from the
harness registry via `rotate.py ack`, not from tmux. Recorded as a finding,
not smoothed over.

## Probe: the tests are not vacuous

The project-wide autouse `_no_real_tmux` fixture in `tests/conftest.py`
answers every `tmux` subprocess with rc 1. Run WITH that guard and no
override, the same file fails 6 of 7 tests (measured on the first draft) —
proving the passing assertions genuinely needed the live binary. The file's
own autouse fixture re-arms `subprocess.run` for calls naming ITS throwaway
session prefix only; any tmux call naming another session keeps the guard's
no-session answer, so the live `agi-rc` hazard stays closed.

## Evidence

    seat-start-row-vs-real-tmux (probe_row_cells.py):
    {"rc":0,"row_window":"@154","tmux_real":"@154","window_matches_tmux":true,
     "row_session_ref":"","row_session_name":"","row_session_id":"",
     "row_carries_tmux_session_name":false,"session_cells_empty_by_design":true}

    probes_real_tmux.py:
    wire-real-pin-occupied: derived=@151 real=@151 state=occupied live=@151
      pid_alive=true
    auth-foreign-and-stale: state=pane-drift live=@151
    gate-window-killed-unoccupied: state=unoccupied live=null
    gate-no-tmux-fails-open: state=null

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.83: the first round on goal:g7.31.2.1 with NO window_path seam. Diverged from the parent brief in one place: it asked for parents:[goal:g7.31.2.1], but the experiment schema removed goal from allowed_parents on 2026-09-01 (min 1, allowed {build,experiment,hypothesis,idea,task,verdict}), so the experiment is parented to my own hypothesis instead. No engine code changed: the real-tmux path already worked; what was missing was evidence through it. The one real trap found is the project-wide autouse _no_real_tmux guard in tests/conftest.py, which silently made every tmux read a no-session answer -- the first draft of the new test passed 1/7 for the wrong reason; the file now re-arms subprocess.run only for its own throwaway session prefix.
<!-- THOUGHT:END -->
