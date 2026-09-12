---
id: hypothesis:l4-the-button-down-legal-hint-consults-is-legal-branch
mint_id: 7c1193dd1ba24c288a54bba764905f74
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-commit-all-is-legal-on-the-season-main-only
next_edges: []
edited_by: sensei-director
scaffold_hash: 2d6f6c55490ff8d4
season: 2
testable_claim: "goal:g15 FIX-ONLY node, mur-SL2.17 (Prime XV 10:22Z, by name, wf_2144282d-658; g17.1 note bf7881ad1) line (8) — L4.311 residue (point round; sensei-director lane by mechanism). Cite at 6afa8c186; re-measure on your base. MEASURED: rotate.py:6447-6459 (6462 on the seat) _button_down_legal_hint reads the checked-out branch with git rev-parse --abbrev-ref HEAD and prints legal on <branch> for ANY branch name, never consulting branches.is_legal_branch (branches.py:74 — True only for master or the season MAIN in either spelling) which L4.311 made the one rule for grid commit --all; a rotate-self --dry-run on a post branch (season2/posts/x or seat/x@s2) therefore promises a grid commit that the real run refuses. CLAIM: the hint calls branches.is_legal_branch on the resolved name and prints legal on <branch> only when it returns True, else NOT legal on <branch> (grid commit would be SKIPPED — season main or master only), keeping the no-repo line as is. FALSIFIERS: a dry-run in a worktree on a post/loop/town branch still reads legal; the season main or master reads NOT legal. TESTS: the hint driven with a fake git returning a post branch, a loop branch, season2/main, season/s2 and master — asserting the exact line each way; the existing dry-run tests unchanged. FILE SCOPE: extensions/agi/bin/rotate.py (_button_down_legal_hint only), tests. EXCLUDED: branches.py, the grid commit itself, the dry-run's other lines. CEILING: one predicate; no new output shape beyond the NOT legal line."
thought_session: sensei-director-genX-L10
title: _button_down_legal_hint reports legal only when branches.is_legal_branch says so, and names the refusal for a post, loop or town branch
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-button-down-legal-hint-consults-is-legal-branch

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
