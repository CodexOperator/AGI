---
id: goal:g4.9
mint_id: 1a1b4c80eb2742bfba091b4966178236
type: goal
parents:
  - goal:g4
next_edges: []
edited_by: director
goal_id: G4.9
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: de70a8566f2ad9c4
status: active
thought_session: L1.12
title: "G4.9: A parent that outlives its timeout is a bug, not a lease"
---
# goal:g4.9

## Agent Notes
"Owner ask, 2026-09-04. Measured in loop L1: iter-1075 parents outlived agent_timeout_mins=20 by more than an hour (leases live 10:59 to past 12:10 EDT); the reaper reported 15 stale parents killed in wave 6; _reap_one restarts a kid with harness={} so a restarted kid runs on the CLI default model; manifest.json still says running after agent.json says done. Commit to: (1) a hung or restarted process is visible in spawn_budget status with its age and restart count; (2) a lease older than its timeout is reaped or explained, never silent; (3) restarts carry the original model and tier; (4) manifest and agent.json agree. Each with a red-on-purpose test. Falsifier: hold a fake pi process past the timeout in a fixture project and assert the reaper reports and bounds it."

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
"Minted by the L1.08 director at the owner request to make waves robust; sits under G4 because it is harness behaviour."
<!-- THOUGHT:END -->
