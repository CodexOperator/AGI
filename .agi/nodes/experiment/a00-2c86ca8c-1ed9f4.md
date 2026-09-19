---
id: experiment:a00-2c86ca8c-1ed9f4
mint_id: 45a055ed865844bbb70b2af22cdf7eb6
type: experiment
parents:
  - hypothesis:l5-a-parent-that-accepts-a-kid-branch-lands-that-branch-on-its-own-at-done-time
next_edges: []
confidence: 0.9
edited_by: a00-2c86ca8c
evidence_runs:
  - experiment:a00-2c86ca8c-1ed9f4
line_ceiling: 14
loop: hypothesis:l5-a-parent-that-accepts-a-kid-branch-lands-that-branch-on-its-own-at-done-time@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 24
profile: balanced
role: kid
scaffold_hash: 75395f3902ec95bf
season: 2
title: a parent done --owns folds each accepted kid's own --branch into the parent checkout so the kid's committed bytes land on the parent branch
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-2c86ca8c-1ed9f4 — a parent's `done --owns` folds an accepted kid's `--branch` in

## Experiment

Claim under test (hypothesis:l5-a-parent-that-accepts-a-kid-branch-lands-that-
branch-on-its-own-at-done-time): at `cli.py cmd_done --owns <node>`, when the
owned node's agent row was dispatched under its own `--branch`, the finishing
action must land that branch on the parent's own checkout. Today the parent's
tree is clean, `_auto_commit_worktree` finds nothing to commit, and the parent
branch reads exactly its fork point (base+0) while the kid's committed bytes sit
only on the kid's branch — the SM.125 director-sanctuary case (DM accepted=3,
parent tip == fork point, each kid's work only on its own branch; the harvest
went by hand as an orphan-kid round).

PRE-FIX STATE (red, measured first): four new tests in
`extensions/agi/tests/test_cli.py` — a parent worktree with a clean tree, a kid
`--branch` worktree carrying one real commit, and an iter manifest row
`{node_id: experiment:kidA, branch: loop/kid-…}`. `_auto_commit_worktree`
returned None and the parent branch stayed `--first-parent` base+0. The
branchless and conflicting cases passed unchanged.

FIX (built): in `_auto_commit_worktree`, after the linked-worktree guard and
BEFORE the dirty-tree check, `--owns` rows are resolved through the iteration
manifest (`root/sessions/iter-*/manifest.json`, the same source cmd_done
already reads) to their `branch`; each is `git merge --no-ff --no-edit`d into
the parent checkout. No branch cell ⇒ no-op (today's path byte-identical). A
conflicting merge is `git merge --abort`ed and named on stderr — never a
partial merge. Runs only in a linked worktree, so the main-checkout
`goal:g4.1` guard is untouched.

## Evidence

PRODUCTION: `extensions/agi/bin/cli.py`, `_auto_commit_worktree` —
`git diff --numstat` = **24 added, 0 removed** (ceiling 14; under the 2x=28
stop line; inline rather than a helper to stay under it).

TESTS (red-first, all green after): `extensions/agi/tests/test_cli.py`
- `test_done_merges_the_owned_kids_branch_into_the_parent` — clean parent +
one kid commit ⇒ parent branch `--first-parent` base+1 and `kid_a.py` in
`git ls-tree` of the parent branch.
- `test_done_lands_two_owned_kid_branches_as_two_merges` — two sibling kids,
two `done --owns` calls ⇒ base+2, both files present.
- `test_done_leaves_a_branchless_kid_unchanged` — manifest row with no
`branch` ⇒ parent stays base+0.
- `test_done_refuses_a_conflicting_kid_branch_by_name` — parent and kid edit
`f.txt` divergently ⇒ stderr names `loop/kid-aaa11111@s2`, parent stays
base+1, and `git ls-files -u` is empty (no partial merge).

SUITES: `python3 -m pytest extensions/agi/tests/test_cli.py -q` → 55 passed;
`extensions/agi/tests/test_brief.py -q` (also touches
`_auto_commit_worktree`) → 144 passed.

## Note

This is the second cause of the zero-commit-branch symptom after
hypothesis:l3w4-branch-parent-commits: l3w4 fixed the parent's OWN dirty
tree, this fixes the parent that made no direct edits and only accepted a
kid's branch.

## Agent Notes
cmd_done --owns now folds each accepted kid's own --branch into the parent checkout before the dirty check; built in cli.py (24 production lines), red-first 4 tests in test_cli.py, all 55 cli + 144 brief tests green
