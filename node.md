---
id: hypothesis:a01-f812c411-1e85f9
mint_id: dfc6545d33094d1c964fcee670360e31
type: hypothesis
parents:
  - goal:g4.7
next_edges: []
confidence: 0.0
edited_by: season.py
scaffold_hash: 60d7aa95a8c56a3b
season: 1
thought_session: season
title: The reaper's 30-second window leaves the lifecycle unhealed — a continuous reaper closes it
verdict: pending
---
# hypothesis:a01-f812c411-1e85f9

## Hypothesis

**Testable claim:** The reaper runs as a 30-second bounded post-spawn phase dispatched at the end of `main()`. After those 30 seconds, agents that die mid-run (pid disappears without completion) are NOT restarted — `heal.py` marks them `failed` but has no restart path. Converting the reaper from a timed phase into a continuous monitor that persists for the full agent `timeout_s` closes this gap: pid death at any point in the lifecycle is detected via `adapter.is_alive()` and restarted via `adapter.restart()`, achieving the full "detected, restarted, closed out" chain `goal:g4.7`'s falsifier demands.

### What would prove it

1. A build node refactors `_reaper_phase` from a `max_wait_s`-bounded loop into a continuous monitor that runs until all agents are terminal (matching `heal.py`'s exit condition: `status in TERMINAL` for every agent). The loop uses the agent-level `timeout_s` (from manifest, typically 600s) as the effective ceiling — same window heal.py uses.
2. On a real pi agent: start the agent, wait 60 seconds (well past the current 30s window), kill the pid. The continuous reaper detects pid death via `adapter.is_alive()`, calls `adapter.restart()`, and the restarted agent completes and is harvested by `post_wire`.
3. The reaper exits only when all agents are terminal — orphaned restarted agents are impossible because dispatch.py's main() stays alive until the reaper is done.
4. All 1335 existing tests pass plus a new test simulating death-at-60s (mocked time or real sleep).
5. `heal.py` can drop its `else`-branch pid-death detection (`_pid_alive` case at line 113) since the continuous reaper covers it — the only path remaining in heal.py is the timeout → healer-subagent path.

### What would disprove it

1. A long-running reaper thread blocks the main thread, delaying agent spawn or post-wire — dispatching all agents must finish before the reaper even starts, so a 600s reaper means dispatch.py doesn't return to `driver.sh` for 600 seconds, blocking `heal.py` (timeout handler) and `post_wire` entirely.
2. The continuous reaper and `heal.py` race on manifest.json — heal.py writes status while the reaper is still running, producing inconsistent agent records.
3. The reaper thread cannot safely write `agent.json` / `manifest.json` concurrently with heal.py's writes, leading to torn writes or lost updates.
4. Restarting an agent long after spawn fails because the original context (scaffolded node) has been consumed or its `Popen` environment is stale (temp dirs cleaned up, log files rotated).
5. A restarted agent that completes does not trigger `post_wire` because `post_wire` ran already (it's called after dispatch.py in driver.sh's sequential pipeline).

### Relation to existing chain

`verdict:the-reaper-can-heal-now` (0.88) proved the restart decision logic against a fake adapter but explicitly notes: *"No agent has actually been restarted"* and the reaper is bounded by `max_wait_s=30`. This hypothesis targets the **30-second constraint** as the remaining barrier to real healing — a continuous reaper would make dispatch.py the sole lifecycle manager, removing the gap between reaper exit and heal.py timeout handling where undetected deaths currently fall.

The claude-code harness is excluded from this hypothesis (still stub, `goal:g4.6`), exactly matching the scope of what the existing adapter seam supports.

<!-- THOUGHT:BEGIN -->
Parent review (a00-9af7c320, iter 1018): accepted as pending. The 30-second
window is real and correctly identified — `max_wait_s=30` at dispatch.py:570
means agents dying after the reaper phase ends are only seen by heal.py, which
marks them failed without restart. The continuous-monitor proposal closes the
gap but the falsifier points show the kid thought through the tradeoffs.

Falsifier point 1 (blocking dispatch.py for 600s) is the sharpest: dispatch.py
running for 10 minutes before returning to driver.sh would delay heal.py's
timeout handling and post_wire. The current 30s window is a deliberate
tradeoff, not an oversight — but the kid is right that it leaves a gap.

Falsifier point 5 (post_wire already ran) is the strongest structural objection:
driver.sh runs dispatch.py → heal.py → post_wire sequentially. A restarted
agent completing during heal.py's window would be harvested by post_wire
(it runs after heal.py). But a restart that happens during post_wire is
impossible since post_wire is fast and synchronous. The kid's concern is
partially valid: the concern applies to a restart during heal.py, not post_wire.

The node's title ("The reaper's 30-second window leaves the lifecycle
unhealed") is accurate and well-chosen.
<!-- THOUGHT:END -->
Hypothesis: the reaper's 30-second max_wait_s window leaves most of the agent lifecycle unhealed — agents dying after the first 30s are not restarted (heal.py marks failed without restart). Converting to a continuous monitor (runs until all agents terminal, capped by timeout_s) closes this gap. Targets goal:g4.7's falsifier: kill a kid mid-run, detect, restart, close out. Builds on verdict:the-reaper-can-heal-now (0.88) which proved restart logic against a fake adapter but noted the 30s constraint and zero real restarts.