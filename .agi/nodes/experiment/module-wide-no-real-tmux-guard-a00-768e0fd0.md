---
id: experiment:module-wide-no-real-tmux-guard-a00-768e0fd0
mint_id: 2f078229f6334af186bb321019a16ed4
type: experiment
parents:
  - hypothesis:a00-768e0fd0-6e3cb8
next_edges: []
edited_by: a00-3193a1dc
evidence_runs:
  - experiment:module-wide-no-real-tmux-guard-a00-768e0fd0
line_ceiling: 40
loop: goal:g7.31.4.2@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 28a06e38fdab47db
season: 2
testable_claim: An autouse recording-tmux fixture makes the no-real-tmux property global to test_send_surface_ssh_or_not.py, and a committed non-vacuity test drives the REAL _list_windows to prove the shim can record a genuine tmux call.
title: "Module-wide no-real-tmux guard: autouse shim + non-vacuity proof"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:module-wide-no-real-tmux-guard-a00-768e0fd0

## Experiment

Close MUR residue #2 on `goal:g7.31.4.2`: the `tmux_shim` assert was per-test
and vacuous. Production bytes in `extensions/agi/bin/send.py` were NOT touched
— this is a test gap, not a production defect.

Three changes, all in `extensions/agi/tests/test_send_surface_ssh_or_not.py`:

1. `tmux_shim` now returns a `_TmuxShim` handle (`.log`, `.exists()`,
   `.text()`, `.expect_clean`), so the same shim object is shared by the
   requesting test and the new module-wide guard.
2. A new `autouse=True` fixture `_no_real_tmux` REQUESTS `tmux_shim`, so EVERY
   test in the module runs with the recording PATH `tmux` installed —
   including `test_transport_decision_is_engine_internal`, which previously
   had no shim at all. At teardown it asserts the log does not exist: any
   future un-stubbed seam that shells out fails the test that opened it.
   `test_transport_decision_is_engine_internal` now also stubs
   `send._window_listed`, so no test in the module carries an un-stubbed tmux
   seam.
3. Non-vacuity guard `test_tmux_shim_records_a_real_list_windows_call`: drives
   the REAL `send._list_windows("some-session")` with the shim on PATH and
   requires the log to exist and to name `list-windows`. It sets
   `expect_clean = False` (the ONLY such test), so the teardown guard does not
   contradict the very call it proves. Without this guard, `assert not
   log.exists()` could pass because the shim never works.

`pid` liveness: NOT load-bearing for the nudge surface. `_nudge_target`
resolves the address from `window`/name and never consults a pid;
`_registry_status` (`send.py:1940`) is a FILE lookup of
`~/.claude/sessions/<pid>.json` (busy/idle hint), not a liveness probe, and
the real-path tests stub it to None. `send.py` contains no `_pid_alive`. The
`_LIVE_PID = os.getpid()` idiom in `test_seat_pane_registry.py:43` is about
`rotate._pid_alive`, a different function. No pid change made.

Wording repair (item 3 of the residue): the module now has SEVEN tests, and
"Both real-path tests" was imprecise. The shim-covered tests are
`test_real_path_refuses_foreign_box_and_reaches_local`,
`test_windowless_row_by_name_fallback_reaches_pane`,
`test_windowless_row_unlisted_is_a_named_no_op`, and
`test_tmux_shim_records_a_real_list_windows_call`.

## Evidence

`python3 -m pytest extensions/agi/tests/test_send_surface_ssh_or_not.py -q`:

```
.......                                                                  [100%]
7 passed in 3.26s
```

(7 tests: 6 pre-existing + the new non-vacuity guard.)

Direct transcript proving the shim records a genuine `_list_windows` call:

```
_list_windows -> []
log exists: True
log text: 'list-windows -t some-session -F #{window_name}\n'
```

Non-vacuity test alone:

```
$ python3 -m pytest extensions/agi/tests/test_send_surface_ssh_or_not.py -q -k tmux_shim
.                                                                        [100%]
1 passed, 6 deselected in 0.77s
```

production_lines: 0 (only the test file changed; `send.py` untouched).

<!-- BODY:END -->
