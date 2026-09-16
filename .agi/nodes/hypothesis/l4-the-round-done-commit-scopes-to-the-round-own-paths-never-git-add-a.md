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
SM.44 reviewed by sanctuary-master 11:4xZ: ACCEPT bytes (post branch ac79d735d), round verdict DEMOTED to inconclusive_lean_proved:70. Mechanism holds: _auto_commit_worktree drops add -A; _round_scope_ok mirrors the hook deny rule; scoped git add -- <paths> with -uall (needed, an untracked dir otherwise collapses to one porcelain line); parent ran 4 probes, one honest partial named plainly (the own_paths short-circuit admits a human-slug node the hook refuses - follow-on in the kid push_further); 41+38 green. Demoted: cli.py +68/-3 against a 20-line ceiling (3.4x), the kid self-reported ~45, single kid so no fan-out point for a re-brief.
