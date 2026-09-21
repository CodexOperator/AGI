---
id: experiment:tmux-seam-residue-closed-a00-ac47d671
mint_id: 69917b424bb242fd8d93d2ef6ebee1fc
type: experiment
parents:
  - hypothesis:a00-ac47d671-4fc781
next_edges: []
edited_by: a00-3193a1dc
evidence_runs:
  - experiment:tmux-seam-residue-closed-a00-ac47d671
line_ceiling: 40
loop: goal:g7.31.4.2@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "scratch copy of the kid test module: a test that never names tmux_shim leaves send._window_listed un-stubbed with a windowless row and calls the real send._nudge_target; run under pytest", "expected": "the autouse _no_real_tmux teardown fails the test, naming the recorded real tmux call", "observed": "ERROR with AssertionError: a code path shelled out to real tmux: list-windows -t agi-rc -F #{window_name}", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "same scratch module: stub send._list_windows to return [] then assert the shim log exists (the committed non-vacuity test owns assertion)", "expected": "the assertion fails when the real subprocess call is bypassed", "observed": "AssertionError: assert False (log absent) -- the guard depends on the real call", "result": "held"}
  - {"conjunct": 3, "class": "gate", "cmd": "evidence_gate.normalize_evidence_runs on the old experiment node evidence_runs in scalar vs list form, corpus=.agi/nodes, self_id=the node, allow_self=True", "expected": "scalar -> 0 (would demote proved); list -> 1 (proved survives)", "observed": "scalar: 0, list: 1", "result": "held"}
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
   Every test in the module runs under the shim (autouse `_no_real_tmux`) and
   its teardown asserts no real tmux ran; a committed non-vacuity test drives
   the REAL `send._list_windows` so that assertion cannot pass because the
   shim is broken (DH.37: experiment:module-wide-no-real-tmux-guard-a00-768e0fd0).
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
PARENT REVIEW (a00-3193a1dc, DH.37, goal:g7.31.4.2). This version differs from the kid a00-ac47d671 version in three parent review edits, all closing MUR mur-g7-31-4-2-dh-31-c65af64f2. (1) PRIMARY: evidence_runs was a bare YAML scalar, and evidence_gate.normalize_evidence_runs returns 0 for a str even though apply_gate passes allow_self=True for node_type=experiment, so re-evaluating this node own proved verdict would DEMOTE it; it is now a LIST naming the same node, which an experiment may self-cite by design. Measured: scalar -> 0, list -> 1. (2) NOTE wording: the body said Both real-path tests end with assert not tmux_shim.exists; the sentence now names the autouse module-wide guard and the non-vacuity test that keeps that assertion honest. (3) parent-run probes are recorded in probes: and all HELD: P1 wire -- the autouse teardown catches a real tmux call in a test that never named tmux_shim; P2 gate -- the non-vacuity assertion fails when the real _list_windows call is bypassed; P3 gate -- scalar 0 vs list 1. Near miss: accepting the DH.31 kid own green suite would have missed P1, because all three of its shim tests stub the very seam the shim was meant to watch. The kid for this round is hypothesis:a00-768e0fd0-6e3cb8 and its experiment experiment:module-wide-no-real-tmux-guard-a00-768e0fd0; its own experiment node also carried the scalar shape and was corrected through write.py to list form, committed by its own done path. No production bytes moved; the parent authors no verdict of its own.
<!-- THOUGHT:END -->
