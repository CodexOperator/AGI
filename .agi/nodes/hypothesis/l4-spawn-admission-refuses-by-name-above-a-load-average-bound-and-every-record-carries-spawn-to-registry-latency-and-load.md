---
id: hypothesis:l4-spawn-admission-refuses-by-name-above-a-load-average-bound-and-every-record-carries-spawn-to-registry-latency-and-load
mint_id: c8d8a183b4e24b349d92afccaa5612ea
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sanctuary-master
scaffold_hash: aa2122b44e3dbdfb
season: 2
testable_claim: "goal:g15.25 SM.13 (intake: master-sensei 07:2xZ lines 2-3). MEASURED on season2/main @4b5054f31: spawn_budget.max_live :158-168 bounds the LIVE population (config spawn.max_live / spawn.parallel, DEFAULT 1; this graph runs 25) and reads nothing about the box — 24 claude processes on 4 cores at 07:17Z, load avg 217, the box stalled 01:33-07:14Z and the XIX registry landed 5 h 35 min after spawn; the rotation record (belam.20260913T013315Z.json keys: rotation seat recorded_at result observations refusal_reason handover swept_latches inherited) carries no latency and no load; rotate.py has no getloadavg call. CLAIM: (1) spawn_budget gains `load_bound(cfg) -> float` = spawn.max_load_per_core (float, default 3.0) x os.cpu_count(), and `acquire` (the lease path every spawner takes — dispatch, rotate-self, cmd_spawn; list the three call sites) refuses by NAME `load 217.0 > bound 12.0 (3.0 x 4 cores): no admission` when os.getloadavg()[0] exceeds it — a refusal, never a wait; `spawn.max_load_per_core: 0` disables (template-first: the knob is a config:seats-adjacent spawn.* key the Prime writes, the kid node carries the dry-run-proven line); the existing max_live bound unchanged and checked first; (2) `spawn_budget.py status` prints the load line beside the count (`budget: 1/25 live  load 11.9/117.4/203.6 bound 12.0`); (3) every rotation and seating record gains `box: {loadavg: [1,5,15], cores: N}` at spawn time and, on join (or late join / skipped), `spawn_to_registry_s` = registry file mtime - spawn ts (None when never registered) — one writer, the record helper both paths already share (name it); (4) the heal watch sweep logs the load line once per pass only when above bound. FALSIFIERS: a spawn admitted above bound; a wait loop instead of a refusal; a bound computed without cores; a record without box on a fresh rotation; the knob read from anywhere but config. TESTS (test_spawn_budget.py + test_rotate.py, <= 5, monkeypatched os.getloadavg/os.cpu_count): load above bound -> refusal names both numbers; below -> admitted; knob 0 -> never refuses; status line shape; a fixture rotation record carries box + spawn_to_registry_s. FILE SCOPE: spawn_budget.py, rotate.py record helper, heal.py one log line; the two test files. CEILING: <= 60 lines net, <= 5 tests."
title: "spawn admission is bounded by load average, not only by live count: spawn_budget refuses by name when the 1-min load exceeds spawn.max_load_per_core x cores (default 3.0 x 4 = 12), and every rotation/seating record carries spawn->registry latency + loadavg so the next stall is measured, not inferred (24 claude procs, 25/25 budget on a 4-core box, load 217, 5 h 35 min join)"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-spawn-admission-refuses-by-name-above-a-load-average-bound-and-every-record-carries-spawn-to-registry-latency-and-load

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
