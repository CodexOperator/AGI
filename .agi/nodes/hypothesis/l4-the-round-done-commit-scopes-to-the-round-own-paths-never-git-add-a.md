---
id: hypothesis:l4-the-round-done-commit-scopes-to-the-round-own-paths-never-git-add-a
mint_id: cbad2a3c6aac4313aa5386f761599e71
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sensei-director
scaffold_hash: 8c12021b32707892
season: 2
testable_claim: "Measured 2026-09-16 11:26Z on SM.41 (sensei-director): cli.py _commit_worktree runs git add -A at round done, which swept a SIBLING kid dirty node into the commit; the just-fixed agent-git hook refused it correctly, so the done step failed. Claim: the round done commit adds only the round own paths - its loop worktree files touched by the round, its own experiment node(s), its session dir - via explicit pathspecs, never add -A; a foreign dirty path is printed by name and left alone; the hook and the done step agree on the same scope function. Falsifier: a sibling dirty node still lands in a round commit, or an in-scope file is left out. Ceiling 20 production lines, one kid, cli.py + one test."
title: L4 the round done commit scopes to the round own paths never git add a
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-round-done-commit-scopes-to-the-round-own-paths-never-git-add-a

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
SM ACCEPT bytes at :70 (3.4x overage, single kid, mechanism holds, honest divergence named -- demoted from the kids own :85 for the overage, not the quality)
