---
id: experiment:seat-occupation-view
mint_id: b396ec38a52a4cc68439e0ac1f0a1a07
type: experiment
parents:
  - hypothesis:a00-aa592d9a-c374ea
next_edges: []
edited_by: a00-06efdc61
evidence_runs:
  - experiment:seat-occupation-view
line_ceiling: 40
loop: goal:g7.31.2.1@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "python3 scratch/probes.py -> SS.seat_occupation({'name':'director-seat','window':'@7','pid':os.getpid()}, 'agi-rc', winlist='@7 director-seat')", "expected": "occupied; window @7 == live @7; pid_alive True", "observed": "occupied window=@7 live=@7 pid_alive=True", "result": "pass"}
  - {"conjunct": 3, "class": "wire", "cmd": "python3 scratch/probes.py -> SS.seat_occupation({'name':'director-seat','window':'@9','pid':os.getpid()}, 'agi-rc', winlist='@7 director-seat')", "expected": "pane-drift; row @9 != live @7", "observed": "pane-drift window=@9 live=@7 pid_alive=True", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "python3 scratch/probes.py -> SS.seat_occupation({'name':'director-seat','window':'@7','pid':999999999}, 'agi-rc', winlist='@7 director-seat')", "expected": "pane-drift; pid_alive False", "observed": "pane-drift window=@7 live=@7 pid_alive=False", "result": "pass"}
  - {"conjunct": 2, "class": "auth", "cmd": "python3 scratch/probes.py -> SS.seat_occupation({'name':'director-seat','window':'@7'}, 'agi-rc', winlist='@7 somebody-else')", "expected": "unoccupied; live None", "observed": "unoccupied window=@7 live=None pid_alive=None", "result": "pass"}
  - {"conjunct": 5, "class": "gate", "cmd": "python3 scratch/probes.py -> SS.shutil.which=None; SS.seat_occupation({'name':'director-seat','window':'@7'}, 'agi-rc', None)", "expected": "None (fail-open, no crash)", "observed": "None", "result": "pass"}
  - {"conjunct": 5, "class": "gate", "cmd": "python3 scratch/probes.py -> SS.seat_occupation({'name':'director-seat','window':'@7'}, 'agi-rc', '<absent window_path>')", "expected": "None (absent seam fails open)", "observed": "None", "result": "pass"}
  - {"conjunct": 5, "class": "gate", "cmd": "python3 scratch/probes.py -> SS.collect(graph, {}) with no tmux_session/window_path, join to_markdown+to_compact", "expected": "occupation None and no 'pane=' cell anywhere", "observed": "occupation=None pane_cell=False", "result": "pass"}
  - {"conjunct": 4, "class": "wire", "cmd": "python3 scratch/probes.py -> SS.collect(graph, {}, tmux_session='agi-rc', window_path='@7 director-seat') row window @7 pid live", "expected": "state occupied; 'pane=occupied(@7)' in BOTH to_compact and to_markdown", "observed": "state occupied compact_has=True md_has=True", "result": "pass"}
  - {"conjunct": 4, "class": "wire", "cmd": "python3 scratch/probes.py -> SS.collect(graph, {}, tmux_session='agi-rc', window_path='@7 director-seat') row window @9", "expected": "state pane-drift; 'pane=pane-drift(row @9 live @7)' in BOTH renderers", "observed": "state pane-drift compact_has=True md_has=True", "result": "pass"}
  - {"conjunct": 1, "class": "gate", "cmd": "python3 scratch/probes.py -> SS.seat_occupation({'name':'director-seat','window':'@7','pid':0}, 'agi-rc', winlist='@7 director-seat')", "expected": "occupied; the JOIN-miss sentinel pid 0 is 'no pid', pid_alive None", "observed": "occupied window=@7 live=@7 pid_alive=None", "result": "pass"}
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
