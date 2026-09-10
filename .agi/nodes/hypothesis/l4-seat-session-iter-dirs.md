---
id: hypothesis:l4-seat-session-iter-dirs
mint_id: 0aa1eca066914ad4a1c38d25c4dc694b
type: hypothesis
parents:
  - idea:l4-seat-session-owns-its-iter-dirs
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 855480a2980faff5
season: 2
status: pending
tags:
  - l4
  - g15
  - seat-protocol
testable_claim: "TWO HALVES, both required. (a) RESOLUTION: an agent's `iter-<id>/` session dir resolves to the RUNNING WORKTREE's own `.agi/sessions/`, not the main checkout's. The line is `dispatch.py:1075` — `sess_root = locations.shared_project_root(root) or root` — which routes through the shared-state resolver. 🔴 `locations.git_common_root` (`locations.py:212-227`) must KEEP routing the spawn budget, the comms root and the meter pins to the main checkout: a tree-wide concurrency bound that splits per worktree is not a bound. Only the iteration dirs move. Proved by: dispatching from a seat worktree puts the agent dirs under that worktree's `.agi/sessions/iter-<id>/`, while `spawn_budget.py status` still reports ONE budget across every worktree. (b) SESSION-COMPLETE: a command (a `worktree.py` or `rotate.py` subcommand) that REFUSES unless the seat branch is already an ancestor of its parent branch, then COPIES the worktree's `iter-*` dirs into the main checkout's `.agi/sessions/` — an explicit copy, because `sessions/` is gitignored so a merge carries nothing — and only then removes the worktree and the branch. Proved by: it refuses on a non-ancestor branch and removes nothing; on an ancestor branch the iter dirs appear in main and the worktree and branch are gone; and an existing dir of the same name in main is NEVER overwritten. NO node is deleted. The code lands under goal:g15 by the owner's relevance rule. HARD CEILING: 3 kids. 🔴 Do NOT run the full pytest suite — run the targeted test files only and say which. A whole-directory run collides with the other seat and the prime."
thought_session: sanctuary-director-genVI-L4
title: Agent iteration dirs land in the main checkout instead of the seat worktree that made them, so a seat cannot harvest its own round
---
<!-- BODY:BEGIN -->
# hypothesis:l4-seat-session-iter-dirs

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
