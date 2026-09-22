---
id: goal:g7.24
mint_id: 39bfb4ea5b1d4460aafd0334eff69ed5
type: goal
parents:
  - goal:g7
next_edges: []
confidence: 0.9
edited_by: belam
goal_id: G7.24
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: d8e26aac628f5199
season: 2
seeds: []
status: active
tags:
  - goal
  - subgoal
  - l4
  - seat-protocol
thought_session: g1-g7-rewrite-2026-09-19
title: "G7.24: A seat session owns its own iteration dirs, and session-complete migrates them before the worktree is deleted"
---
<!-- BODY:BEGIN -->
# goal:g7.24

**A seat session's `iter-<id>/` dirs belong to that seat's worktree, and are migrated into the main checkout only when the worktree is deleted at session complete.** Owner rule, recorded verbatim in `goal:g7.16`; this sub-goal carries the engine half.

**Measured today, which is what makes it real rather than tidy:** dispatching from the seat worktree put every agent dir in the MAIN checkout's `.agi/sessions/`, while the seat's own `.agi/sessions/iter-L4.02/` held nothing but the wrapper log. The dispatched PARENT hit the same thing — its `struggles:` line reads that the manifest path in the spawn output "did not exist from my checkout", so it had to read the kid's node directly to review it. A seat cannot harvest its own round from its own tree.

**The line:** `dispatch.py:1075` resolves `sess_root = locations.shared_project_root(root) or root`, and `shared_project_root` routes to the main checkout by design.

🔴 **What must NOT move:** `locations.git_common_root` (`locations.py:212-227`) deliberately routes SHARED state — the spawn budget, the comms root, the meter pins — to the main checkout, because a tree-wide concurrency bound that splits per worktree is not a bound. That stays. Only the iteration dirs, which are per-session and not shared, move.
