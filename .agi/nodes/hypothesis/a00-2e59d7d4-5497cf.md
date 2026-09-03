---
id: hypothesis:a00-2e59d7d4-5497cf
mint_id: 7e356fe1ea9a482cb4cb8e6a9521ea31
type: hypothesis
parents:
  - goal:g4.7
confidence: 0.0
scaffold_hash: 13b1acb9055a093f
title: A00 2e59d7d4 5497cf
verdict: pending
---

# hypothesis:a00-2e59d7d4-5497cf

## Hypothesis

**Testable claim:** A `dispatch.py` reaper phase — running inline after spawn, inside the same loop — that calls adapter methods `is_alive(pid)` and `restart(agent_record, context)` can detect dead/timed-out agents and restart them, matching `heal.py`'s detection and recovery coverage without a second program.

### What would prove it

1. A build node implementing `AdaptiveReaper` as a new phase in `dispatch.py`.
2. On **each** harness configured (`pi` first): kill a kid mid-run. The reaper detects pid death within one poll interval and restarts with the original context intact.
3. The same single code path (no harness-if/else) handles detection and restart; the only harness-specific logic lives in the adapter's `is_alive()` and `restart()` methods.
4. All edge cases currently covered by `heal.py` survive: pid-gone-without-status-update (→ mark failed), timeout (→ kill + spawn replacement), manifest sync on every pass.
5. `heal.py` can be reduced to a thin CLI entry point that imports and calls the reaper, or deleted outright.

### What would disprove it

1. The inline reaper misses an edge case `heal.py` covers (e.g. healer subagent spawning for deep diagnosis, or detecting a hung pi process whose pid is alive but unresponsive).
2. The reaper's inline poll blocks the dispatch loop from spawning new agents, producing a net throughput regression worse than the current out-of-process polling.
3. Adapter methods `is_alive` and `restart` cannot be made harness-generic — per-harness logic leaks into the dispatch loop despite the adapter seam.
4. Timeout detection in the inline model misses the window where `heal.py`'s separate process catches stragglers dispatch.py has already exited.



## Agent Notes
Filed hypothesis: inline reaper in dispatch.py via adapter methods is_alive/restart replaces heal.py for dead-agent detection and recovery. No experiments yet — pending.