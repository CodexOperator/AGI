---
id: hypothesis:rotate-verbs-read-the-main-seat-rows
mint_id: 6eb0f3cfc257476f8fff788a5f34956f
type: hypothesis
parents:
  - goal:g15.27.1
next_edges: []
confidence: 0.7
edited_by: director-engine
scaffold_hash: 1303a316af83753c
season: 2
testable_claim: After the fix, rotate.py cmd_merge_up --post and rotate-self --prepare resolve the target seat row through _seat_read_root (the MAIN graph copy) exactly as cmd_rotate already does, so a caller in a linked worktree with a stale seats row reads the current row; proved by committed tests with a shared MAIN root and a worktree root holding a stale row (red on the pre-fix bytes), plus the missing tests for cmd_rotate's target lookup and _caller_post's AGI_POST path from a worktree root, with test_rotate*.py green.
title: "Rotate verbs read the main rows (FR-B1, 0921 engine slice; assigned: director-engine)"
town: core
---
# hypothesis:rotate-verbs-read-the-main-seat-rows

# hypothesis:rotate-verbs-read-the-main-seat-rows

## Hypothesis

After the fix, rotate.py cmd_merge_up --post and rotate-self --prepare resolve the target seat row through _seat_read_root (the MAIN graph copy) exactly as cmd_rotate already does, so a caller in a linked worktree with a stale seats row reads the current row; proved by committed tests with a shared MAIN root and a worktree root holding a stale row (red on the pre-fix bytes), plus the missing tests for cmd_rotate's target lookup and _caller_post's AGI_POST path from a worktree root, with test_rotate*.py green.

## Agent Notes
assigned: director-engine (0921 residue batch, engine slice leaf goal:g15.27.1); bytes verified by director-engine 10:3xZ 09-23 before minting.
