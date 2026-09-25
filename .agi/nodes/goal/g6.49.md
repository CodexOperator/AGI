---
id: goal:g6.49
mint_id: a9af1352a6624153836628bda0ebaf7c
type: goal
parents:
  - goal:g6
next_edges: []
confidence: 0.9
edited_by: belam
goal_id: G6.49
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: 60f69c4384f3b4f4
season: 2
seeds: []
status: active
tags:
  - goal
  - subgoal
thought_session: reaper-triage-2026-09-25
title: "G6.49: the reaper burns the box it is meant to tend — a per-spawn OOM probe, a sweep that re-derives a permanent refusal, and liveness that cannot see a live tree"
town: core
---
<!-- BODY:BEGIN -->
# goal:g6.49

## Agent Notes
Measured on encryption-town (belam-prime) 2026-09-25 14:2xZ, while local-town sat wedged with sshd not completing a banner exchange and its work frozen at 13:58:34Z. The reaper is the thing that was supposed to keep the box tidy; it was a top consumer of the box instead. Three independent defects, one subgoal each. (1) oom_kill 1784 since boot with 1422 failed run-*.scope units resident in systemd --user, one pair per spawn, because mem_cap's enforcement probe ran once per PROCESS and its whole contract is an observed SIGKILL. (2) 622 worktrees swept every 30s, removed=0 on all 2387 passes since 2026-09-23, about 5 git subprocesses per worktree per pass, roughly 3000 process spawns per pass to re-derive an unchanged refusal; the reaper log reached 48 MB in 6 days. (3) liveness read only the spawn-budget lease dir, which was EMPTY (kept-live=0) while 11 worktrees held running processes, three of them mid workflow.py run merge-up-review -- had the other four sweep conditions passed, a live round's tree would have been deleted under it. Fix landed on codex-town/reaper-fix-20260925 at 81c054e2a, merged to core/main at 4cdf601ff. Verified after restart: sweep refused=323 kept-live=6 (unchanged=312), and the backstop reported 7 leaseless trees held live by a running process.
