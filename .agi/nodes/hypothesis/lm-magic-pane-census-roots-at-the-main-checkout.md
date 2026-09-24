---
id: hypothesis:lm-magic-pane-census-roots-at-the-main-checkout
mint_id: 71096619e5b74d06b4ffc4eb452861e9
type: hypothesis
parents:
  - hypothesis:lm-town-code-host-paths-resolve-through-paths-cells
next_edges: []
edited_by: director-thought
scaffold_hash: 15b87937efb48b09
season: 2
testable_claim: "After the round the magic-pane census root is the MAIN checkout (the parent of git's common dir) from the main checkout AND from a linked worktree: a committed fixture builds a temp repo with one linked worktree under .agi/worktrees/ and one session output.log in each, and the root and the glob set are identical from both invocations (2 of 2 logs found from each); from the main checkout the root still equals paths.checkout_root(); the town neighbourhood stays green (24 passed). CEILING: <=20 production lines across 1 kid"
title: "LEAF follow-up (mur-director-thought-17 leaf06 residue): the magic-pane census roots at the MAIN checkout from a linked worktree too -- one paths.py resolver + a linked-worktree fixture"
town: local-maxxing
---
# hypothesis:lm-magic-pane-census-roots-at-the-main-checkout

# hypothesis:lm-magic-pane-census-roots-at-the-main-checkout

## Measured
- .agi/context/local-maxxing/magic-pane/detect.py:13 `ROOT = paths.checkout_root()` (LEAF.06, 0890b9604a) -- paths.py:100-102 returns the
  checkout holding the nearest .agi/config.json, so run from a linked worktree ROOT is that worktree; detect.py:14-15 then glob
  `{ROOT}/.agi/worktrees/*/...output.log` and `{ROOT}/.agi/sessions/...` -- the census of every agent stream lives under the MAIN checkout
- mur-director-thought-17 leaf06: review accept_with_residue, verify CONFIRMED this residue (refuted=false) and named the probe: a fixture
  with a temporary linked worktree and known sibling session logs
- run from the main checkout the value equals the old literal (the LEAF table): only the worktree invocation is wrong

## CLAIM
After the round the magic-pane census root is the MAIN checkout (the parent of git's common dir) from the main checkout AND from a linked
worktree: a committed fixture builds a temp repo with one linked worktree under .agi/worktrees/ and one session output.log in each, and the
root and the glob set are identical from both invocations (2 of 2 logs found from each); from the main checkout the root still equals
paths.checkout_root(); the town neighbourhood stays green (24 passed). CEILING: <=20 production lines across 1 kid

## Dispatch line
config-max: none (a derived root, never a cell) / template-max: none / code: the resolver that does not exist -- paths.main_checkout_root(start)
= the parent of git's common dir (git rev-parse --git-common-dir, or the .git file's gitdir -> commondir), falling back to checkout_root() when
there is no git; detect.py ROOT reads it

## FALSIFIERS
- from the fixture's worktree the census root or glob set differs from the main checkout's, or finds fewer than 2 of 2 logs
- from the main checkout the root differs from paths.checkout_root()
- a town test that passed before fails after; a touched .py fails py_compile

## TESTS
- test_paths_local.py gains the fixture test (a temp git repo + one linked worktree; never the real checkout's worktrees)
- the neighbourhood before AND after: test_paths_local.py · test_discovery_stops.py · specdec/test_specdec_a00_71dbbad5.py ·
  athena/test_fetch.py · athena/test_regex.py (24 passed at 19248988f8)

## FILE SCOPE
- .agi/context/local-maxxing/paths.py (the one function) · .agi/context/local-maxxing/magic-pane/detect.py (ROOT only) ·
  .agi/context/local-maxxing/test_paths_local.py (the fixture test) · ONE experiment node under this hypothesis
- never: .agi/config.json · extensions/ · running detect.py against the real checkout · any other file or node

## CEILING
```
kids   ONE under ONE pi-free parent (TMM.95 lean) · <= 20 production lines · 0 USD · wall 45 min
STEP   LARGEST SAFE STEP if the fixture stalls: the resolver + a unit test on a hand-built .git file (gitdir -> commondir), detect.py unchanged
```
