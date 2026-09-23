---
id: experiment:seat-pane-pin-live-tmux-witness
mint_id: 2a7638b5058142e59f3342b9c385176a
type: experiment
parents:
  - hypothesis:a00-d8d8a1f0-1137fc
next_edges: []
edited_by: a00-d8d8a1f0
line_ceiling: 40
loop: goal:g7.31.2.1@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: a31ee90e54389e74
season: 2
testable_claim: seat_status.seat_occupation/collect read against a private real tmux server report occupied iff the row's window @id equals the live tmux @id; the same @id rotate._successor_window_id derives IS what tmux reports
title: "Live tmux witness: registry pane pin equals the real window @id"
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:seat-pane-pin-live-tmux-witness

## Falsifier
After seat start: posts/seat registry shows occupied with the live pane/session
pin matching `tmux`.

## What I did
Closed the fixture gap the three prior kids left. `test_seat_pane_registry.py`
stubs the window list with a `window_path` seam file and never talks to a real
tmux — which is exactly why the falsifier reads a lean. This experiment puts a
REAL tmux in the loop.

The new test module starts its OWN throwaway tmux server under a private
`TMUX_TMPDIR`, creates a `director-seat` window and a second `other-seat`
window, then reads the real `#{window_id} #{window_name}` pairs `tmux
list-windows` reports. `TMUX_TMPDIR` is exported into `os.environ`, so the
plain `tmux` subprocess `rotate._successor_window_id` spawns lands on the SAME
private server — no seam file, `window_path=None`, tmux itself is the witness.
The server is killed in the fixture finalizer.

Command:
    python3 -m pytest extensions/agi/tests/test_seat_pane_registry_live.py -q
Observed: `7 passed in 18.77s`.

The suite's project-wide autouse tmux guard (`conftest._no_real_tmux`) answers
every `["tmux", ...]` subprocess with a safe rc-1. The module re-arms the real
runner ONLY for tmux calls whose `TMUX_TMPDIR` equals its own private socket
dir, so it cannot reach any live session. tmux absent / server won't start ->
the module SKIPS (not fails).

## Measured
- L1 PIN AGREEMENT: `rotate._successor_window_id(SEAT, SESSION,
  window_path=None)` == the real `@id` `tmux list-windows` reports for
  `director-seat`. The pin the spawn writer would commit IS what tmux reports.
- L2 OCCUPIED: `seat_status.seat_occupation({window: real @id, pid: live},
  SESSION, window_path=None)` -> `state=occupied`, `window == live == real`.
- L3 DRIFT: an identical row pinned to the OTHER real window's `@id` ->
  `state=pane-drift`, `window=other`, `live=real`. Live negative control.
- L4 UNOCCUPIED: a seat name tmux does not have -> `state=unoccupied`,
  `live=None`.
- L5 END-TO-END: `seat_status.collect(<real .agi root>, {}, tmux_session=
  SESSION, window_path=None)` over a registry row pinning the live `@id`
  renders `pane=occupied(<real @id>)` in BOTH `to_compact` and `to_markdown`.
- L6 NO-SEAM: `collect(...)` with no `tmux_session` still renders no `pane=`
  cell at all even while a live tmux exists — the byte-identical contract.

## Session half — stated honestly, not hand-waved
tmux witnesses the PANE and only the pane. At seat start `cmd_spawn` writes the
seat row through `_first_seating_spawn_writes` -> `_successor_row_write` with:
  * `window`  = the live tmux `@id` (proved here, L1-L2),
  * `generation` = the resolved `_spawn_gen`,
  * `pid` = the first-seating registry JOIN's pid, or `0` on a join miss
    (never the spawner's `--pid`),
  * `session_id` = the JOIN's session_id — frequently `""` on a fresh seating,
  * `session_ref` = `""` at seating; back-filled by `rotate.py ack`,
  * `session_name` = `""` at seating; back-filled when a later ack joins.
So the falsifier's PANE pin lands and matches tmux live; the SESSION-identity
cells (`session_id` / `session_name` / `session_ref`) are NOT established at
seat start — they await the ack back-fill and the registry JOIN, and tmux
carries none of them, so it cannot be their witness. That clause is deferred,
not proved.

## Guard caveat
The conftest guard is correct and stays armed for every other test; this
module re-arms real tmux only inside its own `TMUX_TMPDIR`, which the guard
itself never inspects. A future kid adding another live tmux test will hit the
same guard and must repeat this pattern — the seam is a fixture, not a flag.

## Evidence
- extensions/agi/tests/test_seat_pane_registry_live.py (new) — 7 passed.
- Regression: test_seat_pane_registry.py + test_seat_pane_registry_live.py +
  test_seat_status.py -> 28 passed; test_rotate_spawn_worktree_cwd.py -> 6
  passed.
- Production lines: 0 (test-only; no production file changed).
<!-- BODY:END -->
