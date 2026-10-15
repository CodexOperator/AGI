---
id: hypothesis:g73319-g15-fallback-test-picks-its-target-from-the-live-graph
mint_id: 8285ea88fce94dbd89791d7c5e94e687
type: hypothesis
parents:
  - hypothesis:l4-the-must-implement-rule-is-g15-lineage-gated
  - goal:g7.33.19
next_edges: []
scaffold_hash: a3901615410b9bd5
season: 2
testable_claim: test_g15_rule_with_no_project_root_keeps_the_current_fallback resolves its target at test time as a live node whose parents list goal:g15, is green on the trunk, goes red or skips-with-reason when the fallback root is wrong, and brief.py production code is unchanged
title: the no-project-root g15-rule test picks a live goal:g15 child from the repo graph, never a hard-coded id a re-parent can break
town: core
---

# hypothesis:g73319-g15-fallback-test-picks-its-target-from-the-live-graph

## Measured
- trunk HEAD 34cb1ce460: test_brief.py::test_g15_rule_with_no_project_root_keeps_the_current_fallback RED ("THIS KID MUST IMPLEMENT THE FIX" absent), alone; reproduced by DG4 14:4xZ 09-30 (1 failed, 1 passed on -k g15_rule).
- cause is a GRAPH read, not brief.py: the test hard-codes target hypothesis:parent-brief-derives-wait-exit-codes-from-cli-constants -> goal:g15.29.19 -> goal:g15.29 -> goal:g15; goal:g15.29 was re-parented goal:g15 -> goal:g1 at eedb0b2b1f (belam [decision] 00:xZ 09-30, retired-designation rule), so the walk in brief.py `_is_g15_lineage` never reaches goal:g15. The docstring already records the SAME break once before (the previous target was re-parented to goal:g6.11).
- `_is_g15_lineage` returns True for target == goal:g15 before any graph read, so targeting goal:g15 itself would pass without exercising the no-project-root fallback walk.
- live direct children of goal:g15 still exist in .agi/nodes/hypothesis/ (e.g. core-sync-0923-residues, grid-old-namespace-refilled-and-forked): the rule is still live for them.
- DG4.17 (g1.31.1.1 3rd pass, tip 7c1da7497) touches brief.py but not this test or `_is_g15_lineage` -> not folded there.

## CLAIM
The no-project-root fallback test no longer breaks when one node is re-parented: it picks its target FROM the repo graph at test time (a live, non-deprecated node whose `parents:` lists goal:g15, found through brief.py's own resolver `_resolve_graph_root(None)` + `_parents_of`, never a hard-coded id) and asserts the rule renders; when the repo holds no such node it skips with the reason named, never passes vacuously. brief.py production code is unchanged.

## Dispatch line
config-max: none (a test target is not a cell). template-max: none. code: the test's target resolver only -- test-only.

## FALSIFIERS
1. The test still names a fixed hypothesis id.
2. The test passes when brief.py's fallback walk is broken (mutate `_resolve_graph_root(None)` to a wrong root: it must go red or skip-with-reason, never green).
3. Any production line in brief.py changes.

## TESTS
test_brief.py (full file) + test_brief_render.py + test_bin_help_smoke.py, --basetemp under /tmp.

## FILE SCOPE
extensions/agi/tests/test_brief.py only.

## CEILING
1 parent (pi-free, ladder tier 0) · 1 kid · 0 production lines · tests <= 25 lines · 0 USD lane.
