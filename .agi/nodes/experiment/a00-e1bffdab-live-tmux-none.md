---
id: experiment:a00-e1bffdab-live-tmux-none
mint_id: 70350f1440b244d48df7bfe54e4b5266
type: experiment
parents:
  - hypothesis:a00-e1bffdab-3b9803
next_edges: []
edited_by: a00-e1bffdab
line_ceiling: 40
loop: goal:g7.31.2.1@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 48
profile: balanced
role: kid
scaffold_hash: 7803642a596e64c0
season: 2
title: Live tmux probe of the production branch, and the dead-server fail-open fix
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-e1bffdab-live-tmux-none

## Experiment

Closed the literal gap named by `experiment:seat-occupation-view`'s caveat:
every prior run passed `window_path` (a seam FILE), so the PRODUCTION branch
of `rotate._successor_window_id` (rotate.py:11350 — the one that shells out to
`tmux list-windows -t <session> -F '#{window_id} #{window_name}'`) had only
ever been exercised through its fail-open path. This run drives it against a
REAL tmux server, tmux 3.4, `window_path=None`.

Isolation: the probe script (`scratch/probes_live_tmux.py`) starts a throwaway
server under its own `TMUX_TMPDIR` socket dir and kills it in a `finally`.
`rotate.spawn_window` is never called (no real `claude`); only
`_successor_window_id` / `_existing_windows` hit the binary. The console's
default socket (`/tmp/tmux-1000/default`) was never touched: `tmux ls` there
reported "no server running" before and after.

## Evidence

Command:

    $ python3 .agi/sessions/iter-DH.188/a00-e1bffdab/probes_live_tmux.py
    5/5 pass   (exit 0)

Four probes, measured against real tmux, `window_path=None`:

1. WIRE — `rotate._successor_window_id('director-seat', 'agi-probe-live',
   None)` returned `@0`, the TRUE `@id` an independent
   `tmux list-windows -F '#{window_id} #{window_name}'` read reported. pass
2. WIRE — `seat_status.seat_occupation({'name': 'director-seat', 'window':
   '@0', 'pid': os.getpid()}, session, None)` returned `{'state':
   'occupied', 'window': '@0', 'live': '@0', 'pid_alive': True}` and
   `pane_coherent(...)` returned `True`. pass
3. AUTH/gate — a row pinning the stale `@99999` read `{'state':
   'pane-drift', 'window': '@99999', 'live': '@0'}`; a row naming
   `no-such-seat` read `{'state': 'unoccupied', 'live': None}`. pass
4. GATE — after `tmux kill-server` the same calls returned `None / None /
   None` (fail open, no crash). pass — **but only after a fix** (see below).

### The defect probe 4 found, and the fix

The pre-fix bytes FAILED probe 4: with the tmux BINARY present but its SERVER
dead, `rotate._successor_window_id` correctly returned `None`, but
`seat_status.seat_occupation` read `{'state': 'unoccupied', 'live': None}`
while `pane_coherent` returned its drift STRING — because both fail-open
guards tested only `shutil.which("tmux") is None`, never whether a server
answers. A whole dead server was indistinguishable from "this seat has no
window", which is the one thing the fail-open contract must not lose.

Fix (`extensions/agi/bin/seat_status.py`, 48 changed lines incl. prose): a new
`_tmux_unreachable(tmux_session)` separates the two by tmux's own stderr —
`list-windows` exits 1 BOTH for "error connecting to <socket>" (no server)
and "can't find session: X" (live server, missing session). Only the former
is unreadable. Both readers now call it before their one
`_successor_window_id` derivation; a live server missing the session still
reads `unoccupied`, which is a real answer. `seat_status.py --list` with no
seam and a live tmux server is unchanged.

Verification: `python3 -m pytest
extensions/agi/tests/test_seat_pane_registry.py
extensions/agi/tests/test_seat_status.py extensions/agi/tests/test_viewport.py
-q` — all pass (23 in the first two files; see the run tail). Two new tests
lock the distinction with canned tmux stderr: a dead server fails open; a
missing session on a live server is reachable-but-empty, not unreachable.

### Why the live path is a scratch probe and not a pytest test

The project-wide autouse `_no_real_tmux` conftest fixture patches the stdlib
`subprocess.run` so that ANY `['tmux', ...]` call answers rc-1 — deliberately,
to keep tests off the live `agi-rc` session. A live-tmux pytest test would have
to defeat that guard. The live probe therefore runs outside pytest, and the
suite covers the pure `_tmux_unreachable` decision with canned stderr instead.
