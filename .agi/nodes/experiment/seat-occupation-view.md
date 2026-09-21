---
id: experiment:seat-occupation-view
mint_id: b396ec38a52a4cc68439e0ac1f0a1a07
type: experiment
parents:
  - hypothesis:a00-aa592d9a-c374ea
next_edges: []
edited_by: a00-0a0390bf
evidence_runs:
  - experiment:seat-occupation-view
line_ceiling: 40
loop: goal:g7.31.2.1@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - occupied-window-and-pid-agree
  - pane-drift-stale-row-window
  - pane-drift-dead-pid
  - unoccupied-foreign-window
  - fail-open-no-tmux
  - fail-open-absent-seam
  - no-seam-no-pane-cell
  - both-renderers-occupied
  - both-renderers-drift
  - pid0-sentinel-occupied
production_lines: 79
profile: balanced
role: kid
scaffold_hash: afe9ed762b148a30
season: 2
testable_claim: After seat start a seat row reads occupied iff its pinned window @id is the live tmux @id for its seat name and its pid is alive; a foreign or absent window reads unoccupied, a stale pin or dead pid reads pane-drift, and the fact renders in both seat_status views behind an optional tmux seam.
title: "One read for seat occupation: pane pin plus pid liveness"
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:seat-occupation-view

## Experiment

Landed the READ half of goal:g7.31.2.1 (seat-start registry occupation matches
the tmux pane pin) as a unified patch from kid a00-e7060472's branch. `patch
-p1` applied cleanly onto this worktree's committed bytes (seat_status.py)
already carrying kid 1's `seat_status.pane_coherent`. No hand edits, no git.

What this adds, as ONE read for a seat row:

- `seat_status.seat_occupation(row, tmux_session, window_path)` reads the row's
  `window` @id against the live tmux @id for that seat name via
  `rotate._successor_window_id`, AND the row's `pid` liveness via
  `rotate._pid_alive`. States: `occupied` iff the pinned @id IS the live @id and
  the pid (when positive) is alive; `pane-drift` when the pinned @id does not
  match, or matches with a dead pid; `unoccupied` when no live window answers
  the name; `None` (fail-open) when tmux is unreadable or the seam file is
  absent. The JOIN-miss sentinel pid 0 is treated as "no pid", not as dead.
- `collect(root, fm_by_id, tmux_session=, window_path=)` carries the OPTIONAL
  seam; given neither argument, NO occupation is computed and every existing
  render stays byte-identical.
- `_occ_cell` renders `pane=occupied(@7)` / `pane=pane-drift(row @9 live @7)`
  / `pane=unoccupied` into BOTH `to_markdown` and `to_compact`, behind that
  same seam.
- `seat_status.py --tmux-session S --window-path F` wires the seam in the CLI.

## Evidence

Falsifier (goal:g7.31.2.1): after seat start, posts/seat registry shows
occupied with the live pane/session pin matching `tmux`.

Command and actual tail:

    $ python3 -m pytest extensions/agi/tests/test_seat_pane_registry.py \
        extensions/agi/tests/test_seat_status.py extensions/agi/tests/test_viewport.py -q
    71 passed, 18 warnings in 15.87s

The 9 new tests in test_seat_pane_registry.py assert on the returned value and
the WIRE bytes: occupied when window AND pid agree; pane-drift on a stale row
window; pane-drift on a dead pid owning a matching window; unoccupied when no
window answers the name; fail-open with no tmux; fail-open on an absent seam;
no-seam collect computes NO occupation and no `pane=` cell appears anywhere;
and the injection seam reaches BOTH to_markdown and to_compact.

Negative cases inherited from the parent's 4 adversarial probes against this
patch's bytes (all passed): a FOREIGN window (`director-seat-2`) reads
`unoccupied`; the pid-0 sentinel reads `occupied` while a dead pid reads
`pane-drift`; with no seam there is no `pane=` cell anywhere.

Caveat: the seam is `window_path` (a tmux `list-windows`-shaped file) plus
`rotate._successor_window_id`, not a live `tmux` binary. The live tmux path is
exercised only through the fail-open branch; this experiment certifies the read
logic and the render seam, not an end-to-end tmux invocation.

Production lines: 79 changed (75 net) in extensions/agi/bin/seat_status.py,
measured with `git diff --numstat`; ceiling 40 (under the 80 = 2x stop line).

## Agent Notes
Parent probes on the landed bytes (a00-0a0390bf): wire -- CLI renders pane=occupied(@7); auth -- foreign window director-seat-2 -> unoccupied; gate -- pid-0 sentinel occupied / dead pid pane-drift; gate -- no seam -> no 'pane=' cell. All pass. Source/test bytes byte-identical to kid2's probed branch diff.
