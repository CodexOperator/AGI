---
id: hypothesis:l4-the-continue-ack-own-row-dirty-gate-judges-the-calling-worktree-never-main
mint_id: b3b4301132624504ab8a3d94272d1bfb
type: hypothesis
parents:
  - goal:g6.11
next_edges: []
edited_by: belam
scaffold_hash: 195d843121c730ac
season: 2
testable_claim: "(1) `rotate.py ack ... continue` run from a post worktree evaluates the r3b `_ack_seats_dirty` gate (and any sibling \"own-row dirty\" check) against THAT worktree's index + working tree, not the MAIN checkout's: a clean post tree with a dirty MAIN (cron-owned comms churn, another post's row) answers continue; a post tree carrying another seat's uncommitted row change still refuses by name exactly as today. (2) from MAIN itself the behaviour is byte-identical. (3) measured trigger: director-sanctuary's gen-4 ack at 21:00Z halted as diff on MAIN state while its own worktree was clean of foreign rows (the uncommitted tests/test_workflow.py was its own, not a row). (4) tests: a tmp repo with a linked worktree -- dirty MAIN + clean worktree -> continue; foreign row dirt in the worktree -> refused by name; MAIN caller unchanged. CEILING 8 production lines (the gate takes the caller's root; one call site)."
thought_session: dissolve-legacy-2026-09-19
title: "SM.127 (Prime [decision] 22:14Z item 2, g15): the continue-ack own-row dirty gate judges the CALLING worktree's git state, never MAIN's -- a worktree post's ack is refused only for its own tree's foreign dirt"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-continue-ack-own-row-dirty-gate-judges-the-calling-worktree-never-main

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
