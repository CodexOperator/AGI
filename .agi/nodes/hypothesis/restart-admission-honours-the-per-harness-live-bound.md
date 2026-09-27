---
id: hypothesis:restart-admission-honours-the-per-harness-live-bound
mint_id: c6668f79502e407cb952714808e392cf
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: a00-64458239
scaffold_hash: d0744759c88e7ee6
season: 2
testable_claim: the restart path counts against harnesses.<h>.max_live exactly as dispatch does (pi-local max_live 1); a committed test restarts a kid while the bound is full and sees the refusal.
title: "A restart is admitted under the same per-harness live bound as a spawn (assigned: director-engine)"
town: core
---
# hypothesis:restart-admission-honours-the-per-harness-live-bound

# A restart is admitted under the same per-harness live bound as a spawn

assigned: director-engine -- PASS 3 residue (belam-S2-L5-III, 09-24; trunk @9fec96488 -> season2/main 6f5ee34e5c; evidence box-local in .agi/sessions/workflows/runs/mur-chunkNof22/); source round engine-delta-3 (verify: missed, demote).

**Testable claim.** the restart path counts against harnesses.<h>.max_live exactly as dispatch does (pi-local max_live 1); a committed test restarts a kid while the bound is full and sees the refusal.

## Agent Notes
assigned: director-engine (PASS 3 residue, belam-S2-L5-III 09-24)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
build order: the restart lease is the same admission call as the spawn, so the fix is one kwarg; a falsifier must pass a cfg carrying spawn.max_live, because the reaper cap falls back to DEFAULT_MAX_LIVE=1 and would refuse a pre-fix run for the wrong reason
<!-- THOUGHT:END -->
