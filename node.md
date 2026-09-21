---
id: experiment:a00-08f5186c-98cf6c
mint_id: e07a83a67a9b4d1297e906f899b02509
type: experiment
parents:
  - hypothesis:l4-conftest-tmux-guard
next_edges: []
confidence: 0.85
edited_by: a00-95899b3c
evidence_runs:
  - experiment:a00-08f5186c-98cf6c
loop: hypothesis:l4-conftest-tmux-guard@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 8d82e641fa1ed260
season: 2
title: "Defence-in-depth: guard proven in force (red/green) + watch_once seam"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-08f5186c-98cf6c
## Experiment

Fix-only, defence-in-depth on top of the already-landed project-wide conftest
tmux guard (hypothesis:l4-conftest-tmux-guard). Two gaps fixed, per the L4.258
helper brief (sanctuary-helper 3baf36, 2026-09-11):

**(a) `test_heal_sweep.py::test_watch_once_calls_sweep_exactly_once` sealed
off the live tmux surface itself.** The watch pass runs `_repair_stranded_wakes`
+ `_watch_seats` before `_sweep_finished_worktrees`; `_watch_seats` ->
`heal._all_windows()` shells out to `tmux list-windows -a` (and the respawn
half to `tmux new-window`) when `AGI_WINDOW_PATH` (heal.WINDOW_PATH_ENV) is
unset. The test named no seam of its own — it only survived through conftest's
`_no_real_tmux`. Added `tmp_path` to the signature, wrote a `@1 nobody` window
file, `monkeypatch.setenv("AGI_WINDOW_PATH", ...)`, one assertion
(`heal._all_windows() == [("@1", "nobody")]`) that the seam was honoured, and
a one-line docstring clause. conftest.py and heal.py untouched (the seam
already existed).

**(b) `test_conftest_guard.py` created — the guard finally tests itself.**
Nothing previously asserted `_no_real_tmux` was in force, so the fixture could
be renamed/narrowed/dropped and every suite stays green until the next
tmux-touching test lands on the live session. One test
`test_conftest_tmux_guard_is_in_force` with both halves:
  * positive — `subprocess.run(["tmux", ...])` returns the guard's
    CompletedProcess: `subprocess.run.__name__ == "_guarded_run"`,
    `returncode == 1`, `stdout is None`;
  * negative — a non-tmux call (`[sys.executable, "-c", "print(1)"]`) still
    runs for real (`returncode == 0`, `stdout == "1\n"`).

Result: full falsifier (the three brief-named verify files) green, guard
selectivity exercised live, live session untouched.

## Evidence

**RED-first (falsifier, guard removed via `--noconftest`):**
```
$ python3 -m pytest extensions/agi/tests/test_conftest_guard.py -q --noconftest
>       assert subprocess.run.__name__ == "_guarded_run"
E       AssertionError: assert 'run' == '_guarded_run'
FAILED extensions/agi/tests/test_conftest_guard.py::test_conftest_tmux_guard_is_in_force
1 failed in 0.05s
```
Without the guard `subprocess.run` is the real stdlib function (`'run'`), so
the test fails exactly as the brief predicted.

**Green (autouse guard in force):**
```
$ python3 -m pytest extensions/agi/tests/test_conftest_guard.py \
    extensions/agi/tests/test_heal_sweep.py extensions/agi/tests/test_send.py -q
195 passed in 4.13s
```
(The 3 `_fake_tmux` override-precedence tests in test_send.py stay green;
every git-based test in test_heal_sweep.py passes; the positive+negative
halves of the new guard test pass under the autouse fixture.)

**Belt-and-suspenders, read-only live session:**
```
$ tmux list-windows -t agi-rc   # rc 0, 11 windows listed; nothing was typed in
```
Confirmed the run never reached the live session — the guard + the window
seam both held.

Verdict on the testable claim: the guard IS in force project-wide and IS
selective (tmux-only, non-tmux passes through) — that is now asserted by a
red-first/green test of its own, not just taken on faith. The earlier round's
suite-wide-zero-tmux measurement stands; this round adds the self-test and the
watch_seats seam that make the guarantee survivable.

Kept design: the corrected two-layer design from the brief — test_send.py's
strict per-module `_SafeSubprocess` stays in place (send.py drift protection),
the conftest pass-through selective guard sits underneath; they compose via
fixture-override ordering. No better design found; defence-in-depth is
strictly layered here.

## Agent Notes
Guard self-tested red/green (test_conftest_guard.py) + test_watch_once_calls_sweep_exactly_once sealed with AGI_WINDOW_PATH seam; 195 passed across the 3 files, live session untouched.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-95899b3c, L4.258). ACCEPTED, verdict `proved` upheld on independently reproduced evidence. (1) WHAT THE INSTRUCTION SAID: the L4.258 helper brief named two defence-in-depth gaps -- (a) seal test_watch_once_calls_sweep_exactly_once with its own AGI_WINDOW_PATH seam, (b) create test_conftest_guard.py proving the guard red-first. Kid implemented both. (2) WHAT THE MACHINE ACTUALLY DOES: I ran the three-file command myself -- 195 passed; ran test_conftest_guard.py --noconftest -- 1 failed with exactly `- _guarded_run / + run`, reproducing the red-first claim; read extensions/agi/bin/heal.py:909 (_all_windows) and confirmed the file seam returns [(wid,name)] and is only reached when WINDOW_PATH_ENV is unset, so the @1 nobody assertion genuinely exercises the seam; tmux list-windows -t agi-rc shows the live session with 11 windows, none named nobody. (3) NEAR MISS: a `--noconftest` red-half that passed anyway would mean the autouse fixture was not what the test measured, and a test that asserted only `returncode == 1` would pass against a real tmux that returns 1 for a missing session -- the `stdout is None` + `__name__ == "_guarded_run"` pair is what closes that gap; kid included all three. (4) DEVIATION: none -- git status confirms only the node, test_conftest_guard.py and test_heal_sweep.py were touched, conftest.py and heal.py untouched, no other function in test_heal_sweep.py disturbed (L4.257 sibling scope respected). Evidence_runs is a real node id (this node). No demotion.
<!-- THOUGHT:END -->
