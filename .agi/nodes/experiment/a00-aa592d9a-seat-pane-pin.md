---
id: experiment:a00-aa592d9a-seat-pane-pin
mint_id: a7ae80f8b85e4dc8babc4905ce503d28
type: experiment
parents:
  - hypothesis:a00-aa592d9a-c374ea
next_edges: []
edited_by: a00-aa592d9a
evidence_runs: experiment:a00-aa592d9a-seat-pane-pin
line_ceiling: 40
loop: goal:g7.31.2.1@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "WIRE", "cmd": "cmd_spawn window_path @7 director-seat", "expected": "row window @7", "observed": "row window @7", "result": "pass"}
  - {"conjunct": 2, "class": "REFUSAL", "cmd": "cmd_spawn window_path @9 somebody-else", "expected": "row window empty", "observed": "row window empty", "result": "pass"}
production_lines: 50
profile: balanced
role: kid
scaffold_hash: 798385573d2b5f55
season: 2
testable_claim: At seat start the registry row window cell equals the live tmux @id; no live pane means no window claim; pane_coherent names drift and fails open
title: Seat-start registry pin matches the live tmux pane
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# Seat-start registry pin matches the live tmux pane

## Falsifier
After seat start: posts/seat registry shows occupied with the live pane/session pin matching `tmux`.

## What I did
Drove `rotate.cmd_spawn` end-to-end on a tmp `.agi` graph with NO live tmux:
the `window_path` seam file is EMPTY at the pre-spawn gate and carries
`@7 director-seat` after the launch (the fake `spawn_window` writes it), which
is exactly the real sequence.

Command:
  PYTHONPATH=/tmp/pt AGI_TIER=kid python3 -m pytest \
    extensions/agi/tests/test_seat_pane_registry.py -q -p no:warnings

Observed: `8 passed in 15.51s`.

## Measured (on the wire -- the committed row bytes)
- POSITIVE: after the seating, seats.md carries `window == "@7"` (the live
  tmux @id), `generation` present, `pid == 0`, `session_ref == ""` on a
  registry JOIN miss (empty registry_dir).
- JOIN-MISS: a row carrying stale `pid: 999999` / `session_ref: stale-ref` is
  OVERWRITTEN to pid 0 / empty session_ref -- never the predecessor's identity.
- NEGATIVE CONTROL: with `@9 somebody-else` after the launch, the row's
  `window` is EMPTY -- a seat start with no live pane claims no occupation.

So the WRITE side already holds; no `rotate.py` change was needed.

## Read side
No function answered "does this row's pane pin match live tmux?", so ONE
read-only helper was added to `seat_status.py`:
`pane_coherent(row, tmux_session, window_path=None) -> bool | str | None`
(reuses rotate's ONE `_successor_window_id`, never a second list-windows
parse). It returns True on a match, a drift STRING naming the seat otherwise,
and None (fail-open, no crash) when tmux cannot be read (no binary + no seam,
or a seam file that is absent). Surfaced as the last column of
`seat_status.py --list`, with new `--tmux-session` / `--window-path` flags.

## Testable claim
At seat start the registry row's `window` cell equals the live tmux @id for
that seat; when no live pane exists the row claims no window; and
`seat_status.pane_coherent` names drift by seat and fails open without tmux.

## Verdict
inconclusive_lean_proved:80 -- my own test is the claim; the parent's
adversarial probes judge it.

## Evidence
- extensions/agi/tests/test_seat_pane_registry.py (new) -- 8 passed.
- extensions/agi/bin/seat_status.py -- +pane_coherent, +--list coherence column.
- Regression: test_seat_status.py, test_rotate_spawn_worktree_cwd.py,
  test_town_rows_readers.py, test_geometry_config.py, test_seat_pane_registry.py
  -> 43 passed.

## Probes
- WIRE: window_path `@7 director-seat` -> row window `@7` (match).
- REFUSAL: window_path `@9 somebody-else` -> row window empty (no occupation).
- REFUSAL: pane_coherent row `@9` vs live `@7` -> drift naming the seat.
- FAIL-OPEN: pane_coherent with no tmux binary -> None.
