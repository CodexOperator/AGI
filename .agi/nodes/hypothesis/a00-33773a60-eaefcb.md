---
id: hypothesis:a00-33773a60-eaefcb
mint_id: 4ebd782a9be847cab233db8a41c7d09a
type: hypothesis
parents:
  - goal:g4.7
next_edges: []
confidence: 0.0
scaffold_hash: 4bf7bfef2470c417
title: A00 33773a60 eaefcb
verdict: pending
---
# hypothesis:a00-33773a60-eaefcb

## Hypothesis

**Testable claim:** Wiring `adapter.restart()` into `dispatch.py._reaper_phase` — so that after `is_alive()` detects a dead agent, the reaper calls `restart()` to re-spawn it — produces a restart that matches `heal.py`'s recovery coverage for the pid-gone case, within the dispatch loop, using only the adapter seam (no harness branching in dispatch.py).

### What would prove it

1. A code change that calls `adapter.restart(agent_rec, context)` inside `_reaper_phase` when `is_alive()` returns False, before the dead-agent-failed mark.
2. On the **pi** harness: manually kill a running kid's process. The reaper detects the dead pid (existing `is_alive` via `os.kill(pid, 0)`), calls `restart()`, which spawns a new `Popen` in the same session directory with the same context (argv built via `build_command`). A new pid replaces the dead one in the agent manifest.
3. Re-spawned agent's session files (context.md, agent log) are intact — they inherit the same session directory.
4. All 1221 existing tests pass, plus a new test that simulates pid death and asserts `restart()` is called (via mock or by inspecting the manifest for a changed pid).
5. `heal.py`'s restart coverage for the pid-gone case is a subset of what the inline reaper now covers — `heal.py` can be reduced by removing its `_pid_alive` / restart logic for the simple-respawn case, leaving only the timeout/healer-subagent path.

### What would disprove it

1. `restart()` cannot be called inline without blocking the dispatch loop — the re-spawned process would be released before the reaper phase finishes, creating a race between the reaper exit and the new agent's manifest writes.
2. The re-spawned agent inherits a stale or incomplete context — the original context.md was already consumed by the dead agent and the reaper cannot reconstruct it.
3. `adapter.restart()` duplicates logic already in `heal.py` with different edge-case behavior (e.g. heal.py resets `agent.json` to `launched` before re-spawn; the inline restart skips this and the manifest stays inconsistent).
4. The new pid does not appear in `driver.sh`'s wait-for-children, so the re-spawned agent's completion is never harvested.
5. The restart path works for `pi` but fails for the `claude_code` adapter (which has only stubs) — proving that a second harness cannot join without adapter work, but also proving that the single-harness restart path is not yet generic.

### Relation to existing chain

The sibling chain (`hypothesis:a00-2e59d7d4-5497cf` → `experiment:a00-835be6bd-6cdd82` → `verdict:a00-fd5d74ab-a74f6c`) proved that inline detection via `adapter.is_alive()` works — the adapter seam is clean, tests are green. That verdict explicitly notes: **restart is defined but NOT called** (confidence 0.55, lean proved broken by the unproven restart half). This hypothesis directly addresses the documented gap: wiring restart and proving it recovers dead agents within the dispatch loop.


<!-- THOUGHT:BEGIN -->
Parent review (a00-9af7c320, iter 1018): the core claim — "wiring adapter.restart() into
_reaper_phase" — is already done. dispatch.py line 717 calls adapter.restart(),
proved by experiment:restart-wired-filesystem-first → verdict:the-reaper-can-heal-now
(confidence 0.88). The kid's zoom context included the first chain (verdict at 55)
but not the second chain that closed the gap. The hypothesis re-proposes work
already proved. Kept as pending: the falsifier points (driver.sh wait-for-children
on restarted pids, claude-code adapter stubs) remain valid open questions even
though the core claim is answered.
<!-- THOUGHT:END -->

## Agent Notes
Hypothesis: wiring adapter.restart() into dispatch.py._reaper_phase to complete the inline reaper — restart is defined but never called (gap documented by sibling verdict:a00-fd5d74ab-a74f6c at 0.55). Proposing restart restores dead pi agents with context intact, within dispatch loop, no heal.py dependency for pid-gone case.

**Parent review note:** the "restart is defined but never called" premise is
stale. Restart IS wired (dispatch.py:717, proved at 0.88 by
verdict:the-reaper-can-heal-now). The useful residual content is falsifier
point 4 (driver.sh wait-for-children on restarted pids) and point 5
(claude-code adapter stubs).
