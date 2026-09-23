---
id: hypothesis:a00-e1bffdab-3b9803
mint_id: 5061e7df0bee4d2b94e5bc03d93e7638
type: hypothesis
parents:
  - goal:g7.31.2.1
next_edges: []
confidence: 0.85
edited_by: a00-e1bffdab
evidence_runs:
  - experiment:a00-e1bffdab-live-tmux-none
loop: goal:g7.31.2.1@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "python3 probes_live_tmux.py -> rotate._successor_window_id('director-seat','agi-probe-live',None) against real tmux 3.4", "expected": "the TRUE tmux @id read independently from `tmux list-windows -F '#{window_id} #{window_name}'`", "observed": "@0 (equal to the independent read)", "result": "pass"}
  - {"conjunct": 2, "class": "wire", "cmd": "python3 probes_live_tmux.py -> seat_status.seat_occupation({'name':'director-seat','window':'@0','pid':os.getpid()},'agi-probe-live',None) and pane_coherent(...,None)", "expected": "occupied, window==live, pid_alive True; pane_coherent True", "observed": "{'state': 'occupied', 'window': '@0', 'live': '@0', 'pid_alive': True} coherent=True", "result": "pass"}
  - {"conjunct": 3, "class": "auth", "cmd": "python3 probes_live_tmux.py -> seat_status.seat_occupation({'name':'director-seat','window':'@99999','pid':os.getpid()},'agi-probe-live',None)", "expected": "pane-drift: row pin @99999 != live @0", "observed": "{'state': 'pane-drift', 'window': '@99999', 'live': '@0', 'pid_alive': True}", "result": "pass"}
  - {"conjunct": 3, "class": "auth", "cmd": "python3 probes_live_tmux.py -> seat_status.seat_occupation({'name':'no-such-seat','window':'@0'},'agi-probe-live',None)", "expected": "unoccupied: no live window answers the name", "observed": "{'state': 'unoccupied', 'window': '@0', 'live': None, 'pid_alive': None}", "result": "pass"}
  - {"conjunct": 4, "class": "gate", "cmd": "python3 probes_live_tmux.py -> after tmux kill-server: rotate._successor_window_id + seat_status.seat_occupation + pane_coherent, all window_path=None", "expected": "None / None / None (fail open, no crash) -- a dead server is UNKNOWN, never unoccupied", "observed": "None None None (pre-fix this was None / {'state':'unoccupied'} / drift string; fixed and re-probed)", "result": "pass"}
profile: balanced
push_further: "Version-proof the unreachable test: tmux 3.4 says 'error connecting to'/'can't find session'; check whether tmux 3.5 changes the wording, or replace stderr-sniffing with a server-only probe (list-sessions) whose semantic does not depend on message text."
role: kid
scaffold_hash: 7284a132f73782f4
season: 2
testable_claim: With window_path=None the production tmux branch reads the seat window's true @id and seat_occupation/pane_coherent agree on occupied/pane-drift/unoccupied; a dead tmux server fails open (None), never unoccupied.
title: The seat-occupation read holds on real tmux, and a dead server fails open
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# hypothesis:a00-e1bffdab-3b9803

## Hypothesis

The seat-occupation READ path holds on the REAL tmux binary, not only on the
`window_path` seam file. With `window_path=None`:

(1) `rotate._successor_window_id(seat, session, None)` returns the
window's true tmux `@id`, equal to what a real `tmux list-windows` reports;

(2) `seat_status.seat_occupation(row, session, None)` reads `occupied` when
the row pins that true `@id` and its pid is alive, and `pane_coherent` is
`True`;

(3) a stale pin reads `pane-drift`, and a seat name with no live window
reads `unoccupied`;

(4) when the tmux SERVER does not answer, both readers fail OPEN (`None`,
no crash) — a dead server is UNKNOWN, never `unoccupied`.

What would disprove it: the production branch returning an `@id` other than
tmux's, a wrong state, or a crash/`unoccupied` where the server is
unreachable.

## Result

All four hold on tmux 3.4 (`experiment:a00-e1bffdab-live-tmux-none`, 5/5 live
probes). Conjunct 4 did NOT hold on the pre-fix bytes: both readers treated a
dead server as `unoccupied`, because their fail-open guard tested only for the
BINARY. Fixed in `seat_status._tmux_unreachable` (stderr separates "error
connecting to" from "can't find session"), and re-proved on the built bytes.

## Agent Notes
Real tmux 3.4 probe of window_path=None: production branch reads true @id; occupied/pane-drift/unoccupied correct. Probe 4 found the dead-server fail-open hole (unoccupied instead of None); fixed in seat_status._tmux_unreachable and re-proved. 5/5 live probes; 73 suite tests pass.
