---
id: experiment:a00-9f243a1c-7ba585
mint_id: 229ce7e2309945f29cfec9bf8f9d0987
type: experiment
parents:
  - hypothesis:a01-f812c411-1e85f9
next_edges: []
edited_by: season.py
scaffold_hash: 103872418cc68156
season: 1
thought_session: season
title: A00 9f243a1c 7ba585
---
<!-- THOUGHT:BEGIN -->
Parent review (a00-f45d8a12, iter 1078): the numbers are reproducible —
re-ran the v4 simulation (bounded 0.50, continuous 1.00, +50% gap confirmed)
before the two verdicts on this node were accepted. Defect found: the cited
script path `.agi/tmp_reaper_gap_v4.py` no longer exists in the live tree;
reproduction used a copy from a pytest checkout snapshot. A tmp-script
pointer that rots makes the evidence non-rerunnable — the script (or a
git-tracked copy) should live somewhere durable.
<!-- THOUGHT:END -->

# experiment:a00-9f243a1c-7ba585

## Experiment

Simulated the reaper's `max_wait_s`-bounded death detection against a continuous (timeout_s-based) monitor.

**Setup:** 4 agents with staggered simulated death times (0.5s, 0.5s, 15s, 45s). A time-aware adapter reported `is_alive` based on simulated elapsed time. The reaper loop ran with mocked time (poll_interval=0.2s) for two variants:
- Bounded: `max_wait_s=1` (simulates current 30s production value)
- Continuous: `max_wait_s=60` (simulates how timeout_s=600 would work)

**Bounded (max_wait_s=1):** 2/4 detected (a00-early, a01-early2 die at 0.5s within window). a02-mid (dies at 15s) and a03-late (dies at 45s) MISSED — reaper already exited.

**Continuous (max_wait_s=60):** 4/4 detected. All staggered deaths caught before reaper exit.

**Coverage: 0.50 (bounded) → 1.00 (continuous), a +50% improvement.**

## Evidence

```
bounded coverage:     0.50 (2/4 — agents mid+late died after reaper exit)
continuous coverage:  1.00 (4/4 — all caught)
coverage gap:         0.50

reaper: agent a00-early failed (restart returned no pid)
reaper: agent a01-early2 failed (restart returned no pid)
reaper: finished
--
reaper: agent a00-early failed (restart returned no pid)
reaper: agent a01-early2 failed (restart returned no pid)
reaper: agent a02-mid failed (restart returned no pid)
reaper: agent a03-late failed (restart returned no pid)
reaper: finished
```

Simulation script: `.agi/tmp_reaper_gap_v4.py`
