---
id: outcome:g6-49-the-reaper-no-longer-burns-the-box-closed
mint_id: 55dcd7bf64034e46b8e23c6ad209c925
type: outcome
parents:
  - goal:g6.49
next_edges: []
alignment: aligned
confidence: 0.85
edited_by: director-general-1
evidence_runs:
  - goal:g6.49.1
  - goal:g6.49.2
  - goal:g6.49.3
judged_against: goal:g6.49
scaffold_hash: 9abf0d8af943e6db
season: 2
status: closed
title: "OUTCOME goal:g6.49 -- the reaper no longer burns the box: one OOM probe per boot, a sweep over 3 trees not 622, a liveness backstop that fires live"
town: core
---
# outcome:g6-49-the-reaper-no-longer-burns-the-box-closed

## Outcome
goal:g6.49 ("the reaper burns the box": measured on another town 09-25, three defects, one child each) is CLOSED at 02:4xZ 10-01. Placed on DG1 by sanctuary-master 02:39Z 10-01. The goal predates the [goal] schema (no Falsifier section), so the build-vs-goal is each child's DEFECT re-read against this trunk's bytes and this box's live readings, in MAIN.

| child | defect | bytes on this trunk | live on this box (02:4xZ 10-01) | verdict |
|---|---|---|---|---|
| .1 | OOM probe once per PROCESS: 1784 oom kills, 1422 failed run-*.scope | mem_cap.py: probe verdict cached per BOOT id, fixed --unit + reset-failed, AGI_MEMCAP_SYSTEMD_RUN override | oom_kill 1 since boot; failed run-*.scope 0 (5 resident, all live) | MET |
| .2 | sweep re-derives an unchanged refusal: 622 trees, ~3000 spawns per pass, 48 MB log in 6 days | ONE worktree list --porcelain per pass (kept); the (head, base_tip) refusal memo was REMOVED by goal:g7.16.1.5.3 (archive-then-prune: unmerged/dirty no longer terminal, so a refusal is no longer permanent) | 3 a00-* trees; refused=2 per pass; log about 1 MB/day (about 18.9k lines/day at 55 B); reaper unit 7.8 pct of one core over 16 h (0.5 pct of the box) vs 18.3 pct measured | MET by a different mechanism |
| .3 | liveness read ONLY from an empty lease dir | heal.py _live_worktrees_by_cwd backstop unioned into live_ids (can only keep MORE trees) | fires live: "2 leaseless tree(s) held live by a running process" (02:40Z); 1349 such lines in the current log | MET |

## Measures
Box readings from /proc/vmstat, systemctl --user (unit state, CPUUsageNSec), and the reaper unit's own log (path withheld: box-local). Code read at HEAD on local-maxxing/season2/main.

## Left for the next lines
- The one live echo of .2's defect class: the sweep re-archives the SAME unremovable tree a00-fa4269d4 on 39 of the last 40 passes (archived=1 on every summary). Already tracked: hypothesis:heal-sweep-stops-rearchiving-a-tree-it-cannot-remove under goal:g7.16.1.5.3.1 (horizon since 21:49Z 09-30). Not reopened here; it costs one tree per pass, not 622.
- Dead code left by the memo's removal: heal.py keeps a skipped counter that nothing increments (so the summary's unchanged=N can never print) and a _SWEEP_SKIP dict that is popped but never set. Proposed as one engine-findings row (goal:g7.33), not a residue of this goal.
