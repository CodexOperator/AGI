---
id: verdict:a00-b66ee7eb-c97be4
mint_id: a2fac2a531ba453a9bb36900a1f5567b
type: verdict
parents:
  - experiment:a00-9f243a1c-7ba585
next_edges: []
confidence: 0.65
scaffold_hash: 2775aa5638f4f1d9
title: A00 b66ee7eb c97be4
verdict: inconclusive_lean_proved:70
---
# verdict:a00-b66ee7eb-c97be4

## Verdict

inconclusive_lean_proved:70

## Evidence

Simulation experiment `experiment:a00-9f243a1c-7ba585` compared bounded (`max_wait_s=1`, simulating current 30s production value) vs continuous (`max_wait_s=60`) reaper coverage against 4 agents with staggered simulated death times (0.5s, 0.5s, 15s, 45s).

- **Bounded:** 2/4 detected (0.50 coverage) — agents dying at 15s and 45s missed because the reaper already exited.
- **Continuous:** 4/4 detected (1.00 coverage) — all staggered deaths caught before reaper exit.
- **Coverage gain:** +50% (0.50 → 1.00).

The simulation confirms the hypothesis's core claim: the bounded `max_wait_s` window leaves agents dying mid-lifecycle undetected. A continuous reaper (one that runs until all agents are terminal) closes this detection gap.

**Why lean_proved rather than proved:** The experiment is a time-mocked simulation, not a real pi harness integration. Three falsifier concerns from the hypothesis remain untested:
1. A 600s continuous reaper blocks dispatch.py's return, delaying heal.py and post_wire.
2. Reaper thread vs heal.py race on manifest.json writes.
3. Restarting an agent long after spawn may fail due to stale context (consumed scaffolded node, cleaned temp dirs).
4. Post_wire has already run by the time a late restart completes.

These are structural concerns that only a production implementation can resolve. The core detection mechanism is sound; the deployment constraints are unaddressed.

## Confidence

0.65

Clean simulation, unambiguous signal (+50% coverage). But untested against real adapter race conditions, blocking, and stale-context concerns. Confidence reflects the gap between a simulated mechanism and a production implementation.


## Agent Notes
Simulation confirms continuous reaper closes detection gap (+50% coverage: 0.50→1.00). Lean proved because mechanism is sound but falsifier concerns about blocking, racing, stale context, and post_wire timing remain untested in production.
