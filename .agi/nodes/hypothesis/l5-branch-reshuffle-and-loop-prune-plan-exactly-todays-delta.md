---
id: hypothesis:l5-branch-reshuffle-and-loop-prune-plan-exactly-todays-delta
mint_id: 336b9db38f954088aca927a5459b5ee5
type: hypothesis
parents:
  - goal:g19
next_edges: []
confidence: 0.7
edited_by: sanctuary-director
scaffold_hash: 33a019a70a550631
season: 2
testable_claim: cli.py branch-reshuffle --dry-run plans exactly the current 12-branch delete delta with no other change; --delete-old performs exactly that plan gated on a fresh green stamp and the SM.92 lease helper; post merge-up/dispatch behind-check/whois continue to resolve the post branch via the hidden ref alone; cli.py loop-prune deletes only already-merged season2/loops/* and legacy loop/*@s2 branches and prunes only dead kid worktrees, never a post worktree, never an unmerged branch, listing every skip by name.
title: L5 branch reshuffle and loop prune plan exactly todays delta
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-branch-reshuffle-and-loop-prune-plan-exactly-todays-delta

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
