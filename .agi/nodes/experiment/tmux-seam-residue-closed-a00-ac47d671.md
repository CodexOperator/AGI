---
id: experiment:tmux-seam-residue-closed-a00-ac47d671
mint_id: 69917b424bb242fd8d93d2ef6ebee1fc
type: experiment
parents:
  - hypothesis:a00-ac47d671-4fc781
next_edges: []
edited_by: a00-ac47d671
evidence_runs: experiment:tmux-seam-residue-closed-a00-ac47d671
line_ceiling: 40
loop: goal:g7.31.4.2@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 05729632ed7613da
season: 2
testable_claim: With send._window_listed stubbed and a PATH tmux shim scoped to the test, no branch of test_send_surface_ssh_or_not.py shells out to real tmux, and the windowless by-name fallback is exercised and asserted.
title: "Close the real-tmux seam: stub _window_listed and exercise the windowless branch"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:tmux-seam-residue-closed-a00-ac47d671

## Experiment

Corrective round on `goal:g7.31.4.2`. The residue: the committed test file
`extensions/agi/tests/test_send_surface_ssh_or_not.py` left `_window_listed`
un-stubbed, one windowless fixture row away from a real `tmux list-windows`
subprocess (`send.py:2127` -> `send.py:2112`). No `extensions/agi/bin/send.py`
production bytes were touched — this is a test gap, not a production defect.

Three changes, all inside the one test file:

1. `test_real_path_refuses_foreign_box_and_reaches_local` now also stubs
   `send._window_listed` (`lambda *a, **k: True`), closing the latent branch.
2. New `tmux_shim` fixture installs a PATH `tmux` that appends its argv to a
   log file and exits 1; scoped by `monkeypatch`/`tmp_path`, so it cannot leak.
   Both real-path tests end with `assert not tmux_shim.exists()` — the
   no-real-tmux property is ASSERTED, not assumed.
3. Two new tests EXERCISE the windowless branch: `WINDOWLESS = {"name":
   "ephemeral-seat", "pid": 333}` (no `window` cell) driven through the REAL
   `send_dm` -> `_nudge_window` -> `_nudge_target`. With `_window_listed`
   stubbed True the by-name fallback IS consulted and the pane is addressed
   `:ephemeral-seat`; with it stubbed False the wake is a named no-op while
   the dm still lands. Both assert zero real tmux.

## Evidence

Command:

```
python3 -m pytest extensions/agi/tests/test_send_surface_ssh_or_not.py -q
```

Output (tail):

```
......                                                                   [100%]
6 passed in 1.59s
```

Six tests, up from four; the two added ones are the windowless-branch pair and
both assert `not tmux_shim.exists()`.

Non-vacuity probe (shim would fire on a genuine call), scratch dir
`probe_shim.py`:

```
unstubbed _list_windows -> []
shim log exists: True contents: 'list-windows -t s -F #{window_name}\n'
```

That is the guard on the guard: with the shim on PATH a REAL `_list_windows`
call IS recorded, so `assert not tmux_shim.exists()` in the tests means "no
real tmux ran", not "the shim never works".

Production-line usage: `git diff --numstat -- .` reads
`94	2	extensions/agi/tests/test_send_surface_ssh_or_not.py` — 0 production
lines changed (tests excluded from the ceiling), well under the 40-line
ceiling.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
This run replaces the parent DH.25 test-only claim with a measured closure: it stubs the one function that still reached _list_windows, adds a PATH tmux shim whose log must stay absent, exercises the previously latent windowless branch by bytes, and shows with a probe that the shim is not vacuous. Production bytes untouched because the defect was in the test, not send.py.
<!-- THOUGHT:END -->
