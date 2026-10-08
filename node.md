---
id: experiment:a00-ab04f2be-3965ed
mint_id: 4a5a876dc0784da5a0ee6997e9904317
type: experiment
parents:
  - hypothesis:heal-worktree-refusal-tests-never-reach-live-tmux-and-dead-branches-go
next_edges: []
confidence: 0.9
edited_by: a00-ab04f2be
evidence_runs:
  - experiment:a00-ab04f2be-3965ed
loop: hypothesis:heal-worktree-refusal-tests-never-reach-live-tmux-and-dead-branches-go@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 900d76826a7f9535
season: 2
test_lines_added: 90
title: the refusal file now proves its own no-live-tmux seam (nudge stub + recording gate) under --noconftest
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-ab04f2be-3965ed

## What I did

Slice A of the brief: land the SEAM the DH.427 guard never had, delete the
vacuous guard, and replace it with a real in-process gate.

```
  production lines added : 0   (heal.py / send.py UNTOUCHED -- see below)
  test file              : +90 / -6 lines in test_heal_worktree_refusal.py
                           (brief asked <= 60; the overage is docstring text)
  file deleted           : test_heal_worktree_tmux_guard.py
```

## The two real reaches (both MEASURED, both reproduced here)

A recording PATH `tmux` shim in front of `PATH`
(`$S/shim/tmux`: `printf '%s\n' "$*" >> "$AGI_TMUX_SHIM_LOG"; exit 0`)
under `--noconftest`:

```
$ AGI_TMUX_SHIM_LOG=$S/shim.log PATH=$S/shim:$PATH \
  env -u AGI_WINDOW_PATH -u AGI_TMUX_SESSION \
  python3 -m pytest test_heal_worktree_refusal.py -q --noconftest
  5 passed
  shim log: list-windows -t agi-rc -F #{window_name}
```

Per-test attribution (each test alone, same shim):

| test | recorded tmux argv |
|---|---|
| test_seat_geometry_dir_refuses_a_claimed_worktree_with_no_geometry | (none) |
| test_watch_seats_refuses_by_name_and_launches_nothing | (none) |
| test_typeerror_inside_a_cwd_aware_launcher_is_never_retried | (none) |
| test_worktree_post_refuses_a_no_cwd_retry | (none) |
| test_pre_cwd_seam_still_lands_for_a_main_checkout_seat | `list-windows -t agi-rc -F #{window_name}` |

Stack of that call, captured by printing `traceback.print_stack()` from
inside the recorder (temporary edit, reverted):

```
test_heal_worktree_refusal.py:254  test_pre_cwd_seam_still_lands_for_a_main_checkout_seat
bin/heal.py:3314   _recover_seat            (the respawned=True landing)
bin/heal.py:3120   _dm_crash_recovery
bin/send.py:2986   send
bin/send.py:2286   _nudge_window
bin/send.py:2237   _nudge_target            (send.py:2208-2209 default session)
bin/send.py:2148   _window_listed
bin/send.py:2134   _list_windows
tests/test_heal_worktree_refusal.py:102  _run
```

So the brief's prediction was right: the reach is the NUDGE on the
crash-recovery dm, not `spawn_window`. `list-windows` is what the shim caught
today; the same path continues to `send-keys` the moment a window of the
name is listed, so this was a live-pane risk, not a cosmetic one.

**NO production line was needed.** Both seams already existed:
- `window_path` (heal's `WINDOW_PATH_ENV` seam) keeps
  `spawn_window -> rotate._existing_windows` off the binary. The three
  `_recover_seat` tests passed `window_path=None`; they now pass
  `_window_file(tmp_path)`.
- the nudge path takes NO session parameter, so it is STUBBED (the brief's
  option (b)): `send.send` is replaced by a recorder in the one test that
  reaches it. heal imports send LAZILY inside `_dm_crash_recovery`, so the
  loaded module object is registered in `sys.modules` via
  `monkeypatch.setitem` -- without that the stub patches a DIFFERENT module
  object than heal resolves. That cost me a turn; it is a real trap.

## The gate (item 3) and its negative control

`_tmux_recorder` + `_live_calls` + an autouse `_no_live_tmux` fixture live in
`test_heal_worktree_refusal.py` itself (NOT conftest, so it holds under
`--noconftest`). Every `["tmux", ...]` argv is recorded and answered rc=1 --
conftest's own answer, so the assertions read identically with and without
conftest -- and the fixture refuses at teardown if any argv named
`rotate.DEFAULT_TMUX_SESSION`.

`test_the_recorder_gate_is_not_vacuous` feeds the SAME checker one
`["tmux","send-keys","-t","agi-rc:0.0","hello","Enter"]` and asserts it is
flagged (plus a clean-session negative). The gate's own RED is recorded below
-- this is the output the DH.427 guard could never produce, because conftest
had already answered every call before its shim could see it:

```
E  AssertionError: a test in this file reached the LIVE tmux server:
E   [['tmux', 'list-windows', '-t', 'agi-rc', '-F', '#{window_name}']]
E   (recorded: [['tmux', 'list-windows', '-t', 'agi-rc', '-F', '#{window_name}']])
tests/test_heal_worktree_refusal.py:121
```

## Item 4 -- the measurement, after the seam

```
$ AGI_TMUX_SHIM_LOG=$S/shim.log PATH=$S/shim:$PATH \
  env -u AGI_WINDOW_PATH -u AGI_TMUX_SESSION \
  python3 -m pytest test_heal_worktree_refusal.py -q --noconftest -p no:randomly
  6 passed, 3 warnings in 0.26s
  shim log: EMPTY

$ AGI_TMUX_SHIM_LOG=$S/shim.log PATH=$S/shim:$PATH tmux has-session -t agi-rc
  shim log: has-session -t agi-rc        # positive control: the shim resolves
```

The same shim, in the same run, DOES log a call when one is made -- so the
empty log is a real zero, not a broken shim. This is the falsifier the old
guard failed to beat.

## Test runs

```
$ python3 -m pytest test_heal_worktree_refusal.py -q --noconftest   -> 6 passed
$ python3 -m pytest test_heal_worktree_refusal.py -q                -> 6 passed
$ prlimit --nproc=300 python3 -m pytest test_heal_worktree_refusal.py test_heal.py \
    test_cli.py test_heal_watch.py test_dispatch.py -q              -> 57 failed, 252 passed
$ (same WITHOUT my file)  test_heal.py test_cli.py test_heal_watch.py test_dispatch.py
                                                                 -> 57 failed, 246 passed
```

The 57 failures are PRE-EXISTING and unrelated: the identical count appears
with my file absent, and the same five files without `prlimit`/a fresh
`--basetemp` drop to 12 failures (all in test_dispatch.py). My file's 6 tests
pass in every combination.

## Caveats / what this does NOT prove

- The gate protects THIS FILE only. conftest's project-wide `_no_real_tmux`
  is still the only thing standing between every other test and the live
  session; a test file that forgets its own recorder is still one
  `--noconftest` away from the live pane.
- The gate fires on the recorded argv at TEARDOWN, so a reaching test fails
  as an ERROR not a clean FAIL. That is legible, but it is one notch coarser
  than a body-level assert.
- The reach I found is on the LANDING (respawned=True) branch only. A future
  heal.py change that nudges from another branch would need the same stub.

## Agent Notes
Seam landed with ZERO production lines: the existing window_path seam plus a send.send stub close the measured nudge reach (_dm_crash_recovery -> send._nudge_target -> list-windows -t agi-rc); in-process recording gate + negative control replaced the vacuous DH.427 guard, which is deleted. PATH-shim log EMPTY under --noconftest with a positive control proving the shim resolves.
