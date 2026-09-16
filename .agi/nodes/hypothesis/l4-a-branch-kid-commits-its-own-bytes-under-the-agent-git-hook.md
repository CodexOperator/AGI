---
id: hypothesis:l4-a-branch-kid-commits-its-own-bytes-under-the-agent-git-hook
mint_id: c4b551628d1d4afebf8e6579a1e36abc
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 332a2dfcc4c3c7da
season: 2
testable_claim: "Measured 2026-09-16 10:41Z on SM.36 (parent a00-4d31ec4c, sensei-director report): a --branch KID cannot commit its own work because the agent-git pre-commit hook refuses AGI_TIER=kid, so the parent had to adopt the kid bytes by hand - every --branch round silently costs one manual parent step and the kid authorship is lost from the commit. Claim: on a --branch round the hook admits a kid commit that touches only paths inside the round loop worktree and its own experiment node (never .agi/nodes outside its node, never config, never another post card), refusing by name otherwise; a parent adoption step is never needed for in-scope bytes. Falsifier: a kid commit of an out-of-scope path passes, or an in-scope kid commit still refuses. Ceiling 25 production lines, one kid, the hook + its test only."
title: L4 a branch kid commits its own bytes under the agent git hook
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-branch-kid-commits-its-own-bytes-under-the-agent-git-hook

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
