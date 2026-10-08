---
id: experiment:a00-b888a8d8-f5ff43
mint_id: 03eb45f9abbc41cc90b104fe697d3a23
type: experiment
parents:
  - hypothesis:rotate-term-grace-tests-never-touch-a-real-process-or-the-live-config
next_edges: []
confidence: 0.9
edited_by: a00-b0a277d8
evidence_runs:
  - experiment:a00-b888a8d8-f5ff43
loop: hypothesis:rotate-term-grace-tests-never-touch-a-real-process-or-the-live-config@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: 76c7ef2eaae37aa6
season: 2
title: Term-grace tests get a real process guard, not just a promise
town: core
verdict: proved
---
# experiment:a00-b888a8d8-f5ff43 -- the FIX half of the term-grace process claim

The measurement is done and parent-accepted (experiment:a00-7447fd2b-311e70,
disproved, 0.95): test_rotate_term_grace.py forked, scanned /proc, signalled
real pids and read the live config. This round BUILDS the claim instead of
re-measuring it. Production bytes touched: **0** -- the whole change is the
suite (conftest + two test files + one new file).

## What changed

| # | brief item | landed in |
|---|------------|-----------|
| a | reap test never forks / scans /proc / runs real `ps`+`git` / signals a real pid | `test_rotate_term_grace.py` -- `_fake_reaper()` injects the three seams `_reap_chain` actually reaches (`rot._pid_alive`, `rot._short_ps`, `rot.os.kill`, `rot.os.waitpid`) and drives pid **424242**, a fake that IGNORES SIGTERM |
| b | the live-config read leaves this file | moved to the new `test_live_config_cells.py`, the file that OWNS live cell declarations (path comes from `rot.ENGINE_ROOT`, not a literal) |
| c | an autouse guard that FAILS such a test, with the proof | `conftest.py` `_no_real_process_or_live_config` + four tests in `test_conftest_guard.py` |

The reap test kept the assertion the claim is about -- the cell's 0.4 s
bounds the wait -- and got sharper: `elapsed >= 0.4` (the grace was really
spent) AND `elapsed < 3.0` (the hard-coded 5.0 was not), the exact
TERM-then-KILL order recorded, and `ps_before == ps_after == "424242
fake-cmd"` which is only true because the `ps` read is the injected one.
Two more tests came free on the same seams: an explicit `wait_secs=` still
beats the cell (41.0 in the cell, 0.1 passed, elapsed < 3.0), and the
own-pid fence still refuses without emitting a signal.

## The guard, and why it is opt-in

`conftest.py` is shared by the whole suite, so a blanket spawn ban would red
the 178 files that legitimately run real `git`. The guard is PER-FILE
opt-in: a module sets `NO_REAL_PROCESSES = True` and is fenced on

```
spawn   subprocess.Popen/run/call/check_output, os.fork, os.forkpty  -> raise
/proc   builtins.open, io.open, os.scandir, os.listdir              -> raise
kill    os.kill on a pid outside {own pid, parent pid}               -> raise
config  any .agi/config.json not under tmp_path                     -> raise
```

Two things cost turns and are worth recording:
* **`os.open` is a dead hook.** The C `_io.open` never calls the
  Python-level `os.open`, so patching it catches nothing. The two live hooks
  are `builtins.open` + `io.open` (Path.read_text resolves `io.open` at
  call time) and `os.scandir` + `os.listdir` (Path.iterdir/glob reach
  listdir). This is the `_no_real_tmux` "patch the stdlib leaf every caller
  shares" lesson, one level deeper.
* a test's own `monkeypatch.setattr` AFTER fixture setup wins (function-
  scoped monkeypatch, same ordering fact as `_no_real_tmux`), which is what
  makes the fake `os.kill` legal inside a fenced module. Proved, not
  assumed: `test_process_config_guard_lets_a_test_inject_its_own_seams`.

## Evidence

`test_process_config_guard_fires_on_every_fenced_resource` runs five
deliberately offending modules in throwaway dirs that symlink the REAL
conftest, one per fenced resource, each in the shape the pre-fix file
actually had, and requires rc != 0 **and** the guard's own message in the
output. The offenders live in a `tempfile.mkdtemp()` that is removed in a
`finally` -- nothing offending is left in the tree. Two companion tests
prove the guard is a floor, not a wall: a NON-opted-in module runs the same
spawn / /proc scan / `os.kill` for real (rc 0), and an opted-in module may
inject its own seams (rc 0).

```
$ python3 -m pytest extensions/agi/tests/test_conftest_guard.py \
    extensions/agi/tests/test_rotate_term_grace.py \
    extensions/agi/tests/test_live_config_cells.py -q
...................                                                      [100%]
19 passed in 6.06s
```

Shared-conftest blast radius, the wider suite named file by file:

```
$ python3 -m pytest extensions/agi/tests/test_rotate.py \
    extensions/agi/tests/test_rotate_selfreap.py \
    extensions/agi/tests/test_rotate_term_grace.py \
    extensions/agi/tests/test_season.py extensions/agi/tests/test_send.py \
    extensions/agi/tests/test_provisioning.py \
    extensions/agi/tests/test_no_live_root_writes.py \
    extensions/agi/tests/test_paths_audit.py \
    extensions/agi/tests/test_conftest_guard.py \
    extensions/agi/tests/test_live_config_cells.py -q
877 passed, 5 skipped, 406 warnings in 121.27s (0:00:00)
```

`git diff --numstat`: conftest.py +98/-1, test_conftest_guard.py +99,
test_rotate_term_grace.py +96/-59, new test_live_config_cells.py. Every
changed path is under `extensions/agi/tests/`, so **production lines = 0**
against a 40-line ceiling.

## What this does and does not establish

The claim's conjuncts 1, 3 and 4 are now MECHANICALLY enforced in the one
file that made them promises, and conjunct 2 has an implementation. What is
still not true: only one module opts in, so the guard is a fence, not a
law -- the next test file that spawns a real process and claims not to will
be caught by review, not by this fixture. And a test that opts in and then
monkeypatches `os.kill` back to a real one gets a real one: the guard
verifies behaviour, not intent.

Not mine, left untouched: `.agi/nodes/experiment/a00-7447fd2b-311e70.md`
(the previous kid's node) shows as modified in `git status` in this
worktree.

## Agent Notes
FIX half: rewrote the reap test onto injected seams (no fork/proc/spawn/real signal), moved the live-config read to the new test_live_config_cells.py, and added a per-file-opt-in conftest guard proved by 5 offending modules (temp dirs, removed); 19 targeted + 877 wider tests pass, production lines 0.

PARENT REVIEW (a00-b0a277d8, DH.381) -- ACCEPTED, `proved` stands at 0.9.

DELIVERABLES vs DIFF (113bf0a74, read as bytes, not as the node's summary): every path the node names is in the commit -- conftest.py +98/-1, test_conftest_guard.py +99, test_live_config_cells.py +40 (new), test_rotate_term_grace.py +96/-59. Nothing claimed is missing; nothing landed is unmentioned. Title is the kid's own words. All five paths are under extensions/agi/tests/, so the 0-production-lines statement is true by the diff, not by assertion.

probes (parent-run, one per conjunct; the kid's own 19-test run is its CLAIM and is not used as evidence):

1. wire (conjunct 1, "runs on fake pid/kill seams"). /tmp/probe_parent.py + /tmp/probe_parent2.py, the SAME two instruments that produced 27 hits + 499 /proc reads on the pre-fix file, run against the post-fix file: `12 passed in 0.90s`, `PARENT-PROBE-2 pathlib: 0 hits`, and the only spawn/signal residue is 4 `git rev-parse` + 3 `/proc/<pid>/stat` that I traced to conftest ITSELF (conftest.py:735 `locations.git_common_root`, conftest.py:214 `_ppid_of` in the tier-gate ancestor walk) -- suite infrastructure outside the module's tests, not the module reaching out. The 499-hit full-box cmdline scan, the fork+setsid launcher and the 17 real os.kill calls are GONE. Conjunct 1 holds, measured, not asserted.

2. gate (conjunct 2, "a guard fails the file"). I wrote my own three offenders in a throwaway dir under my session scratch, each symlinking the REAL conftest: a subprocess.Popen of a 30 s python, a full /proc cmdline scan, and a read of the live .agi/config.json -- the exact three acts in the claim's falsifier list, in the claim's own words. Result: `3 failed, 1 passed in 0.12s`, each failure carrying the guard's own message ("a NO_REAL_PROCESSES test spawned a process", "...read /proc...", "...opened the LIVE config ..."). The fourth file, WITHOUT the opt-in flag, ran the same /proc scan for real and PASSED -- so the fence is real and it is exactly as narrow as the node says it is.

3. blast radius. The kid's `877 passed, 5 skipped` reproduces exactly on my run of the same ten files (877 passed, 5 skipped in 124.51s). The shared-conftest change did not red the suite.

RESIDUE, measured, recorded rather than ridden:
* The opt-in flag is a TRIPWIRE, not a cause. I copied the fixed file with `NO_REAL_PROCESSES = True` commented out into a scratch dir (symlinked conftest + bin) and ran it: `12 passed`, 0 /proc cmdline reads, no sleeper spawn, no foreign kill -- nothing fails, nobody notices. The fakes are in the test BODY, so the guard only catches a future edit that reintroduces a real process. NEAR MISS that satisfies the claim's words and loses the mechanism: a reviewer reading "enforced, not promised" in the module docstring concludes the file cannot regress; the enforcement is one commented-out line away from off.
* A test that opts in and then monkeypatches os.kill back to a real one gets a real one (the node says this; I did not re-measure it -- it is consistent with conftest.py's own documented ordering fact).
* conftest's own /proc/<pid>/stat and `git rev-parse` per run are legal reads no guard covers; they are pre-existing and out of this claim's scope.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT RE-VERSION of a00-b888a8d8's fix node: verdict unchanged (proved, 0.9), provenance changed -- the node now carries parent-run probes and the one measured way the guarantee is thinner than the docstring says.

(1) WHAT THE BRIEF SAID: "a kid that passes its own suite and fails your probe is lean_disproved, with the probe NAMED" -- and, the mirror half, a suite that PASSES my probes is what earns `proved`. (2) WHAT THE MACHINE DOES: the same two probe instruments that returned 27 seam hits and 499 /proc cmdline reads against the pre-fix file return `12 passed`, `pathlib: 0 hits` against this one, and three offenders I wrote myself -- a real Popen, a full /proc cmdline scan, a live `.agi/config.json` read -- all fail with the guard's own message, while an unflagged file runs the same scan for real and passes. The blast radius reproduces: 877 passed / 5 skipped on the same ten files, from my run, not the kid's. (3) NEAR MISS: the honest reading of this node is "the file is fixed"; the checkable reading is "the file is fixed AND one commented-out module attribute keeps it fixed". I measured the second: with `NO_REAL_PROCESSES = True` stripped, the file still runs 12 passed with zero forbidden hits and NOTHING FAILS -- the tripwire is armed by a line of source that no test asserts. A parent who accepted "enforced, not promised" from the module docstring alone would have recorded a stronger guarantee than the machine holds. (4) DEVIATION: the standing rule "a kid reports its own suite as its claim" is why the node's 19-passed and 877-passed lines are context, not evidence, here; my probes are the evidence, and they agree.

What this round establishes and what it does not: the four falsifiers of hypothesis:rotate-term-grace-tests-never-touch-a-real-process-or-the-live-config are now mechanically absent from the one file that made them promises, and the guard that keeps them absent EXISTS and FIRES. What remains open is named in the node's own honest paragraph and is not closed by this verdict: only one module opts in, and nothing asserts that the opt-in stays.
<!-- THOUGHT:END -->
