---
id: hypothesis:l5-the-reaper-sweep-terminally-resolves-merged-kid-worktree-leftovers
mint_id: cd987ec5f2614652a7a9703275d968d0
type: hypothesis
parents:
  - goal:g6.11
next_edges: []
confidence: 0.6
edited_by: belam
scaffold_hash: 2cb888cf6d6e3677
season: 2
testable_claim: "the reaper sweep's refusals on MERGED kid worktrees (109 dirs measured at L5 open) are made terminal: dirty leftovers in a merged round are parked under sessions/<iter>/leftovers/ then the worktree is removed; session dirs are brought home via cli.py session-complete first; an UNMERGED kid worktree is always kept and listed by name, never swept."
thought_session: dissolve-legacy-2026-09-19
title: L5 the reaper sweep terminally resolves merged kid worktree leftovers
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-the-reaper-sweep-terminally-resolves-merged-kid-worktree-leftovers

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
