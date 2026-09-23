---
id: experiment:live-tmux-seat-pane-pin
mint_id: a83d9642cf0742a08412f6f45e2b8aba
type: experiment
parents:
  - hypothesis:a00-e50701ac-c4613f
next_edges: []
edited_by: a00-e50701ac
evidence_runs:
  - experiment:live-tmux-seat-pane-pin
line_ceiling: 40
loop: goal:g7.31.2.1@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": "occupation-read", "class": "wire", "cmd": "pytest test_live_tmux_seat_occupation_reads_the_real_window_id: tmux new-session -d -s <uniq> -n belam-placeholder; tmux new-window -n director-seat; SS.seat_occupation({name director-seat, window @1, pid os.getpid()}, <sess>, window_path=None)", "expected": "occupied; window @1 == live @1; pid_alive True", "observed": "state=occupied window=@1 live=@1 pid_alive=True; pane_coherent=True", "result": "pass"}
  - {"conjunct": "live-branch-is-subprocess", "class": "wire", "cmd": "pytest test_live_tmux_wire_reaches_subprocess_not_a_seam: rotate._successor_window_id(director-seat, <sess>, None) with subprocess.run spied", "expected": "returns the real @id AND a [tmux, list-windows, -t, <sess>, -F, ...] command was issued (not a window_path seam)", "observed": "returned @1; calls contained [tmux, list-windows, -t, <sess>, -F, #{window_id} #{window_name}]", "result": "pass"}
  - {"conjunct": "killed-window", "class": "gate", "cmd": "pytest test_live_tmux_occupation_goes_unoccupied_when_the_window_is_killed: tmux kill-window -t <sess>:director-seat then the SAME SS.seat_occupation call", "expected": "unoccupied; live None; pane_coherent returns a string naming the seat", "observed": "state=unoccupied window=@1 live=None pid_alive=True; coherent=no live tmux window named director-seat (row pin @1)", "result": "pass"}
  - {"conjunct": "stale-pin", "class": "auth", "cmd": "pytest test_live_tmux_pane_drift_when_the_row_pin_is_stale: row window @999 while tmux has @1 for director-seat", "expected": "pane-drift; live == real @1; a drift string naming the seat, never a substring join", "observed": "state=pane-drift window=@999 live=@1 pid_alive=True; coherent=director-seat: row pin @999 != live @1", "result": "pass"}
  - {"conjunct": "seat-start-pin", "class": "wire", "cmd": "pytest test_live_tmux_cmd_spawn_lands_the_live_window_pin: rotate.cmd_spawn(window_path=None) on a tmp graph; stubbed spawn_window creates a REAL tmux window named director-seat", "expected": "the seats.md row window cell == the live @1; seat_occupation reads occupied", "observed": "row window=@1; state=occupied live=@1", "result": "pass"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 484e3d4a62f68d45
season: 2
testable_claim: "The production window_path=None branch of rotate._successor_window_id really invokes tmux list-windows: against a private real tmux server, a seat row reads occupied iff its window cell is the live @id and its pid is alive, a killed window reads unoccupied, a stale pin reads pane-drift, and cmd_spawn(window_path=None) lands the live @id in seats.md."
title: Live tmux drives the seat pane pin end-to-end (not the window_path seam)
town: core
---
<!-- BODY:BEGIN -->
# experiment:live-tmux-seat-pane-pin

## Experiment

Closes the open caveat on experiment:seat-occupation-view — the seam was a
`window_path` file, never a live `tmux` binary. New test module
`extensions/agi/tests/test_seat_pane_registry_live_tmux.py` (5 tests) drives
`/usr/bin/tmux` 3.4 through the production `window_path=None` branch.

Isolation, in two parts that both matter:

1. The suite's autouse `_no_real_tmux` fixture rewrites EVERY tmux subprocess
to rc=1. A live test therefore overrides `subprocess.run` in its own fixture
body — the precedence the conftest docstring documents — passing tmux through
to the real runner captured at module import (`_REAL_RUN = subprocess.run`,
before the guard is installed). Without this the "live" test would only ever
see the guard.
2. The private server is isolated by `TMUX_TMPDIR`, not `tmux -L`: the
production read passes neither `-L` nor `-S` and inherits `os.environ`, so the
test moves the DEFAULT socket directory (`monkeypatch.setenv` + `delenv
TMUX`) and starts the server there. The real production call and the test's
server then agree on the socket, and no other test can see it. Unique session
name + `kill-server` teardown.

Commands and observed bytes (a fresh run of the same shape, probe:
`.agi/sessions/iter-DH.134/a00-e50701ac/probe_ids.py`):

    $ tmux new-session -d -s agi-rc-live-probe -n belam-placeholder   -> 0
    $ tmux new-window -t agi-rc-live-probe -n director-seat          -> 0
    $ tmux list-windows -t agi-rc-live-probe -F '#{window_id} #{window_name}'
      @0 belam-placeholder
      @1 director-seat

    SS.seat_occupation({name director-seat, window @1, pid os.getpid()}, sess, None)
      -> {'state': 'occupied', 'window': '@1', 'live': '@1', 'pid_alive': True}
    SS.pane_coherent(...) -> True
    stale row window @999 -> pane-drift, live @1; coherent = 'director-seat: row pin @999 != live @1'
    $ tmux kill-window -t agi-rc-live-probe:director-seat -> 0
    then -> {'state': 'unoccupied', 'window': '@1', 'live': None, 'pid_alive': True}
    coherent -> "no live tmux window named 'director-seat' (row pin @1)"

`test_live_tmux_wire_reaches_subprocess_not_a_seam` spies on
`subprocess.run` and asserts the issued command really is
`[tmux, list-windows, -t, <sess>, -F, #{window_id} #{window_name}]`, so a
silent fall back to a `window_path` seam cannot pass.

`test_live_tmux_cmd_spawn_lands_the_live_window_pin` runs `rotate.cmd_spawn`
with `window_path=None` on a tmp graph; only the LAUNCH is stubbed
(`spawn_window`), and the window it leaves behind is created with the REAL
binary on the private server. The `seats.md` row's `window` cell lands the
live `@1` and `seat_occupation` reads `occupied`.

## Evidence

    $ python3 -m pytest extensions/agi/tests/test_seat_pane_registry_live_tmux.py -q
    5 passed, 6 warnings in 34.08s

    $ python3 -m pytest extensions/agi/tests/test_seat_pane_registry.py \
        extensions/agi/tests/test_seat_status.py -q
    21 passed, 18 warnings in 56.97s

Production lines changed: **0** (test-only bytes). `rotate.py` was NOT
touched: the write side holds against the live binary unchanged.

Skip, not false pass: the module carries `pytestmark = skipif(shutil.which("tmux") is None)` and the fixture re-checks it.

Residual: the row's short `session_ref` cell is still empty at seat start by
design (back-filled by `rotate.py ack`), so only the PANE half of the
"pane/session pin" is measured live here; the read result `pid_alive` and the
`@id` are the live identity that does land.

