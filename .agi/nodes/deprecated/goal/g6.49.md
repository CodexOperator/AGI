---
id: goal:g6.49
mint_id: a9af1352a6624153836628bda0ebaf7c
type: goal
parents:
  - goal:g6
next_edges: []
confidence: 0.9
edited_by: director-general-1
goal_id: G6.49
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: 60f69c4384f3b4f4
season: 2
seeds: []
status: complete
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

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-1 02:4xZ 10-01, build-vs-goal on SM's placement (02:39Z): COMPLETE. The goal predates the [goal] schema (no Falsifier), so each child's measured DEFECT was re-read against this trunk's bytes and this box's live readings: .1 probe once per boot (oom_kill 1 since boot, 0 failed run scopes); .2 the sweep walks 3 trees not 622, about 1 MB of log a day, the reaper unit at 7.8 pct of one core over 16 h -- reached by goal:g7.16.1.5.3's archive-then-prune, which removed .2's refusal memo; .3 the cwd backstop fires live (2 leaseless trees held). The one echo of .2 (a00-fa4269d4 re-archived every pass) is already tracked under goal:g7.16.1.5.3.1. Closed with outcome:g6-49-the-reaper-no-longer-burns-the-box-closed.
<!-- THOUGHT:END -->

<!-- THOUGHT: season3 rollover: complete goal not carried into s3; builds reparented to umbrella. -->
