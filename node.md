---
id: goal:g6.49.2
mint_id: 6244727b05db4032958587f7100faee8
type: goal
parents:
  - goal:g6.49
next_edges: []
confidence: 0.9
edited_by: belam
goal_id: G6.49.2
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: 0eb1357dfb581e61
season: 2
seeds: []
status: complete
tags:
  - goal
  - subgoal
thought_session: reaper-triage-2026-09-25
title: "G6.49.2: the worktree sweep re-derives a permanent refusal every pass, at full subprocess cost, and logs it every time"
town: core
---
<!-- BODY:BEGIN -->
# goal:g6.49.2

## Agent Notes
DEFECT: _sweep_finished_worktrees re-evaluated every worktree from scratch on every pass. A refusal is a pure function of (HEAD, base tip) -- while neither moves, the verdict cannot change -- but the sweep re-ran rev-parse twice, merge-base, git status and the bring-home probe anyway, and logged an identical refusal line each time. MEASURED on encryption-town: 622 worktrees, removed=0 on all 2387 passes since 2026-09-23T07:31Z, about 82.6s per pass against a 30s poll (so roughly 53s of work per cycle), ~5 git subprocesses per worktree per pass, i.e. on the order of 3000 process spawns per pass to reach an answer that had not changed in two days. heal.py watch held 18.3 pct CPU average over 2d 6h on a 4-thread box. The reaper log reached 48 MB in 6 days; the log, not the work, is what grew. FIX: memoize the refusal per process keyed on (head, base_tip) and skip both the subprocesses and the per-pass log line while it holds; replace the two per-worktree rev-parse calls with ONE git worktree list --porcelain for the whole pass; report the skipped count as (unchanged=N) on the summary line so the saving is visible rather than silent. VERIFIED after restart: sweep refused=323 kept-live=6 (unchanged=312).
