---
id: hypothesis:a00-bff3bc1d-202939
mint_id: d2adab7204934dd89fd54f900b016cd1
type: hypothesis
parents:
  - goal:g4.7
next_edges: []
confidence: 0.0
scaffold_hash: 1c149d5d5f94b93e
title: A00 bff3bc1d 202939
verdict: pending
---
# hypothesis:a00-bff3bc1d-202939

## Hypothesis

**Testable claim:** The inline reaper's `_reap_one()` path, when triggered by a **real** pi harness agent dying mid-iteration (not a fake/mock adapter), detects the dead pid via `adapter.is_alive()`, restarts the agent via `adapter.restart()` in the same session directory with the original context intact, and the restarted agent produces the same output the original would have — proving the restart path that `verdict:the-reaper-can-heal-now` (0.88) explicitly marked as untested.

The existing chain proves the decision table (`is_complete` gate, spawn budget, restart count bound) and the adapter seam. What it does NOT test is that `subprocess.Popen(...)` inside `pi_adapter.restart()` actually launches a new pi process that reads the same context, writes to the same session dir, and survives long enough to complete its node. Every test in the current suite uses a `FakeAdapter` whose `restart()` returns a synthetic pid; no real pi process has ever been spawned by the reaper.

### What would prove it

1. An integration test that:
   a. Spawns a real pi agent via `dispatch.py` against a synthetic scaffold (a trivial "write the node and exit" goal, e.g. `demo` harness or a test-only entry point that exits after touching its node).
   b. Captures the agent's pid from the manifest.
   c. Kills the pid externally (`os.kill(pid, 9)`).
   d. The reaper (triggered either inline or via a short reaper poll) detects the dead pid, calls `pi_adapter.restart()`, and a new pid appears in the manifest.
   e. The restarted agent finds its session directory and context intact, completes the trivial goal, and `completion.is_complete` returns True for the target node.

2. The manifest after restart records: `restart_count == 1`, `restarted_at` set, `pid` updated to the new process id. No duplicate entry is created — the original agent record is mutated, not appended.

3. The test passes on its own without a full dispatch loop (can call `_reap_one` directly with a real adapter, real process, and real session dir), AND as part of the full `driver.sh` run — because the real gap is whether `driver.sh` harvests the restarted agent's completion.

4. All existing 1335+ tests remain green.

### What would disprove it

1. **The restarted agent fails to start.** `pi_adapter.restart()` calls `subprocess.Popen` with the same argv as `build_command`, but the session directory already has partial output, stale agent.json, or a consumed context file — the restart produces an immediate crash or hangs. The fake adapter never exercises this because it returns `pid=9999` regardless.

2. **`driver.sh` loses the restarted pid.** The reaper writes the new pid into the manifest, but `driver.sh`'s wait loop was built around the pids it got at spawn time. A pid that changes mid-run is a pid `driver.sh` never hears from — the restarted agent completes, writes its node, and `driver.sh` exits without harvesting because it was waiting on the original pid. The full-loop integration test (3) catches this; the unit test (1) does not.

3. **Agent.json is in an inconsistent state on restart.** The original agent was `running`, the reaper sets it back to `running` with a new pid — but `post_wire` or the completion pipeline reads `status: running` and treats the restarted agent as a fresh one, skipping the completion it already holds from the original run's partial output.

4. **The reaper races with a normal completion.** The reaper detects a dead pid and starts a restart while the original agent's final output (node write + report) was in-flight to the filesystem but not yet flushed. The restart creates a second agent working on the same scaffolded node — the collision `is_complete` was designed to prevent, but a race means `is_complete` returns False even though the node is about to be written. This is the one edge case the filesystem-before-restart ordering cannot close.

5. **The reaper test harness itself is fragile.** A genuine process spawn + kill + re-spawn test depends on timing (the process must die before the reaper runs, the re-spawn must complete before the test asserts) and on process state (the spawned pi child must not outlive the test). A flaky test is a disprover: if the real restart path cannot be tested reliably, it cannot be shipped reliably.

### Relation to existing chain

The existing chain under `goal:g4.7` has proved two things:

| Claim | Verdict | Evidence |
|---|---|---|
| Adapter seam works, detection via `is_alive()` detects dead pids | 0.55, `inconclusive_lean_proved` | 1221 tests, adapter `REQUIRED` tuple, `_reaper_phase` in dispatch.py |
| Restart wired with decision table (`is_complete` gate, budget, count) | 0.88, `proved` | 1335 tests, `_reap_one` calls `adapter.restart()`, suite green |

Both verdicts say the same thing: **the mechanism is proved against a fake adapter.** The hypothesis here is about the real process that fake adapter was standing in for — `goal:g4.7`'s falsifier ("kill a kid mid-run, it is detected and restarted with its context intact") has never been executed once. This hypothesis proposes an experiment that closes that gap.

<!-- THOUGHT:BEGIN -->
Parent review (a00-9af7c320, iter 1018): accepted as pending. The real-agent restart
gap is the one `verdict:the-reaper-can-heal-now` (0.88) explicitly flagged and the
kid identified it correctly. The falsifier points are well-reasoned, especially
the race condition (point 4) and the driver.sh pipeline question (point 2).

Two corrections noted: (1) the test suite is 1382 tests, not "1335+"; (2) the
driver.sh "wait loop" framing is imprecise — driver.sh has no pid-wait; it runs
dispatch.py → heal.py → post_wire sequentially, and pids are tracked via
manifest.json/agent.json files, not shell-level wait. The underlying concern is
still valid: if the reaper updates the pid in agent.json, heal.py and post_wire
read it from the file, so the pipeline does see the new pid. But the 30s reaper
window means a restart at second 29 leaves only heal.py's 30s poll interval to
catch a second death.

The agent.json inconsistency point (3) is the sharpest observation: pi_adapter.restart()
appends to output.log but does not reset agent.json status, unlike heal.py's
healer path. If post_wire reads a stale status, the restarted agent's completion
could be skipped.
<!-- THOUGHT:END -->

## Agent Notes
Real-agent restart hypothesis: the inline reaper (proved at 0.88 against fake adapters) has never restarted a real pi process. This hypothesis proposes an integration test that kills a pi agent mid-run and asserts the reaper detects, restarts via adapter.restart(), and completes the restarted agent's work. Covers 5 falsifier points: process start failure, driver.sh pid loss, agent.json inconsistency, filesystem-before-restart race, and test flakiness.
