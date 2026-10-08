---
id: hypothesis:g73319r49-engine-for-stops-at-the-graph-repo
mint_id: 8649603d3a6d484da1b6ea02504455b2
type: hypothesis
parents:
  - goal:g7.33.19
next_edges: []
scaffold_hash: 991af8753192c77a
season: 2
testable_claim: with a foreign engine in an ancestor above a git repo that holds .agi and no engine, engine_for refuses by name instead of returning the foreign engine; the unified and clone-child layouts still resolve
title: engine_for walks ancestors only up to the repo holding the graph, never adopting an engine above it
town: core
---

# hypothesis:g73319r49-engine-for-stops-at-the-graph-repo

## Measured
- commands.py `engine_for` (DG4.13 tip 9baba2bc99): `for cand in (root, *root.parents)` walks EVERY ancestor of the graph root up to `/`; the first directory holding extensions/agi/bin/commands.py wins, so a graph whose own repo has no engine would silently adopt an engine from an unrelated ancestor directory (the refusal DG4.13 built is only reached when NO ancestor matches). Disclosed open by DG4.13; its refusal rows stub `_is_engine_root`, so the walk has no committed row (findings row 49, goal:g7.33.19).

## CLAIM
`engine_for` walks ancestors only up to the git toplevel that contains the graph root (the repo holding `.agi`; no git -> the graph root's parent only), then the clone-child branch, then refuses by name; an engine in an ancestor ABOVE that repo is never adopted.

## Dispatch line
config-max: none / template-max: none / code: the walk bound in engine_for.

## FALSIFIERS
1. A tmp layout: <tmp>/outer/extensions/agi/bin/commands.py (a foreign engine) and <tmp>/outer/proj/ a git repo with .agi and NO engine -> engine_for(<proj>/.agi) must raise EngineRootError, not return <tmp>/outer.
2. The unified layout (engine in the same repo as .agi) and the classic clone-child layout still resolve (existing rows green).

## TESTS
test_commands.py test_drift_check.py test_verification.py test_bin_help_smoke.py, --basetemp under /tmp.

## FILE SCOPE
extensions/agi/bin/commands.py (engine_for only), extensions/agi/tests/test_commands.py.

## CEILING
1 kid · <= 8 prod lines · <= 30 test lines.
