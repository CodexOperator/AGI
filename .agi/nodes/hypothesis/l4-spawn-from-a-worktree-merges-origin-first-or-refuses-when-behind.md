---
id: hypothesis:l4-spawn-from-a-worktree-merges-origin-first-or-refuses-when-behind
mint_id: 6ec99be9b7274290950a3092583a90f2
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
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
