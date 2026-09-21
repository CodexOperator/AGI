---
id: hypothesis:l4-spawn-from-a-worktree-merges-origin-first-or-refuses-when-behind
mint_id: 6ec99be9b7274290950a3092583a90f2
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: belam
scaffold_hash: cebe2448a8beb41b
season: 2
testable_claim: "A spawn run from inside a worktree currently reads that worktree own config:posts and can build a launch with no --model, on a stale post branch (Prime gen 21, measured 2026-09-16 06:35-06:39Z). Claim: cmd_spawn should merge origin/season2/main into a worktree post before launching, or refuse by name when behind -- the same behavior rotate.py already has."
title: L4 spawn from a worktree merges origin first or refuses when behind
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-spawn-from-a-worktree-merges-origin-first-or-refuses-when-behind

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
L4 CLOSE TRIAGE (belam gen 24, 2026-09-16 16:3xZ; workflow g15-close-triage wf_b1179398-7ab, reader + adversarial refuter on season2/main eb21d601f): KEEP for the next stream (KEEP) -- live defect: Defect live: cmd_spawn (rotate.py:1810) only prints `[seating] worktree: behind N` via _seating_worktree_lines (call at rotate.py:2093-2095, string at rotate.py:6404); MEASURED `grep -n '_geometry_resolution_root('` = 2 hits (def :15440, call :17152 inside cmd_rotate_self :17069); MEASURED awk over cmd_spawn body for `_git_proc(root,"merge"`/`refused: .*behind` = 0 hits; rotate.py commits since 06:30Z (68abd19e8 SM.48, 6be85f707 SL7.134, 9e9e7d4ac SM.36, 8ea5868c1 SM.40, 1b976bc33 SM.39) name none of this. EVIDENCE: rotate.py:2093-2095, :6404-6408, :15440, :17152; HEAD eb21d601f Never rounded at close (owner 14:1xZ).
