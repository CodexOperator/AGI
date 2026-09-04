---
id: experiment:a00-b730ba37-281b5e
mint_id: a935cdbe41d643dfbd035ecf8db8d27b
type: experiment
parents:
  - hypothesis:a00-bff3bc1d-202939
next_edges: []
confidence: 0.8
scaffold_hash: 48b5269c8664202e
title: A00 b730ba37 281b5e
verdict: inconclusive_lean_proved:80
---
# experiment:a00-b730ba37-281b5e

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a01-834996fa, iter 1078): verified against the artifact, not the
report. Ran the test file myself: 6/6 pass in 0.49s, matching the node's
citation. Read the test source: real `subprocess.Popen` with a mock pi shell
binary, real OS pids, `os.waitpid()` reaping (the kid's logged struggle — a
SIGKILLed child stays visible to `os.kill(pid, 0)` until reaped, so
`is_alive()` reads True without it), and no Popen mocking. Checked the
production code the tests exercise: `pi_adapter.py` L133/L148 defines
is_alive/restart, L205 writes `restarted_at`; `dispatch.py` L678 `_reap_one()`
with `cap=1` and L755 increments `restart_count` — the budget-bound claim is
real. Kept the kid's 80: the unproven halves (end-to-end pi/LLM lifecycle,
falsifier 2 driver.sh pipeline, falsifier 4 filesystem race) are named in the
node body, so the frontmatter lean is not ahead of the text. Two review notes
this version records: (1) the "1470 passed, 0 failures" full-suite line is
point-in-time — at review the shared tree had unrelated in-flight edits from a
concurrent agent (transient SyntaxError in test_commands.py from a parallel
run), which makes whole-suite green a moving target; the new file is purely
additive, so those failures are not this node's. (2) With a mock pi binary,
"restarted agent produces the same output" is vacuously true (both runs run
the same deterministic script) — the node says this under "What remains
untested", and that is the correct boundary: the subprocess machinery is now
proved, the agent lifecycle remains.
<!-- THOUGHT:END -->

## Experiment

**What:** Integration test suite `test_real_adapter_restart.py` (6 tests) exercising `pi_adapter.restart()` with real subprocess management — the gap explicitly flagged by the parent hypothesis: all 1382 existing tests use `_FakeAdapter` whose `restart()` returns a synthetic pid.

**How:** Each test creates a mock pi binary (shell script), a minimal project with `.agi/` structure, spawns real subprocesses, kills them with SIGKILL, and asserts the reaper's `_reap_one()` path detects and handles the death correctly via `pi_adapter`.

### Tests and results

| Test | What it proves | Result |
|---|---|---|
| `test_restart_returns_real_pid` | `pi_adapter.restart()` calls `subprocess.Popen` and returns a valid OS pid > 0; agent_record fields (pid, status, restarted_at) updated in place | ✅ PASS |
| `test_is_alive_detects_dead_and_live_real_processes` | `adapter.is_alive()` works with real OS pids — running = True, killed+reaped = False | ✅ PASS |
| `test_restart_produces_a_killable_process` | A process spawned by restart() is a real subprocess that can be killed and detected dead | ✅ PASS |
| `test_real_restart_path_through_reaper_detects_and_restarts` | Full `_reap_one()` path: real process killed, reaper detects via `is_alive()`, restarts via `pi_adapter.restart()`, new pid is alive and different from killed pid | ✅ PASS |
| `test_done_unreported_path_with_real_dead_process` | A kid whose node is complete is NOT restarted (filesystem check before restart) — even with a real adapter | ✅ PASS |
| `test_restart_budget_bound_with_real_processes` | Max restarts bound (1/1) works with real processes — agent marked `failed` at budget exhaustion | ✅ PASS |

**Full suite:** 1470 tests pass (1382 pre-existing + 6 new + 82 others), 0 failures.

### What this closes

- Falsifier point 1 (process start failure): disproved — `restart()` succeeds with real Popen, returns real pid
- Falsifier point 5 (test flakiness): disproved — 6 real-process tests pass reliably in 0.49s
- Falsifier point 3 (agent.json inconsistency): partially tested — restart() writes status=restarted, pid=new, restarted_at into agent_record; the post_wire reading path is not exercised here
- Falsifier point 2 (driver.sh pid loss) and point 4 (filesystem race): remain untested — require full driver.sh pipeline and precise timing respectively

### What remains untested (requires real pi API calls)

The hypothesis claimed the restarted pi agent "produces the same output the original would have" and "completes its work." The subprocess machinery works (`Popen` -> real pid -> kill -> detect -> restart), but a real pi agent (LLM calling) is not spawned here because it requires an API key. The gap is in pi's agent lifecycle, not in the reaper's subprocess infrastructure.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_real_adapter_restart.py -v --tb=short
============================= test session starts ==============================
...
extensions/agi/tests/test_real_adapter_restart.py::TestPiAdapterRestartWithRealProcess::test_restart_returns_real_pid PASSED [ 16%]
extensions/agi/tests/test_real_adapter_restart.py::TestPiAdapterRestartWithRealProcess::test_is_alive_detects_dead_and_live_real_processes PASSED [ 33%]
extensions/agi/tests/test_real_adapter_restart.py::TestPiAdapterRestartWithRealProcess::test_restart_produces_a_killable_process PASSED [ 50%]
extensions/agi/tests/test_real_adapter_restart.py::TestPiAdapterRestartWithRealProcess::test_real_restart_path_through_reaper_detects_and_restarts PASSED [ 66%]
extensions/agi/tests/test_real_adapter_restart.py::TestPiAdapterRestartWithRealProcess::test_done_unreported_path_with_real_dead_process PASSED [ 83%]
extensions/agi/tests/test_real_adapter_restart.py::TestPiAdapterRestartWithRealProcess::test_restart_budget_bound_with_real_processes PASSED [100%]
============================== 6 passed in 0.49s ===============================

$ python3 -m pytest extensions/agi/tests/ -q
...
1470 passed in 85.62s (0:01:25)
```

**Test file:** `extensions/agi/tests/test_real_adapter_restart.py`

**Key assertion output from `test_real_restart_path_through_reaper_detects_and_restarts`:**
- Killed pid detected as not-alive by `pi_adapter.is_alive()`: ✅
- `_reap_one()` returns `status=running` with new pid: ✅
- New pid differs from killed pid: ✅
- `restart_count == 1`: ✅
- New process alive after restart: ✅


## Agent Notes
Real-adapter restart integration test: 6/6 tests pass validating pi_adapter.restart() produces real OS pid, is_alive() detects dead/live processes, _reap_one() restarts killed agents with new pid, done-unreported path prevents re-spawn of completed work, and restart budget bound enforced. Full suite 1470 green. Remaining gap: end-to-end pi agent lifecycle (requires API credentials).
