---
id: experiment:a00-a2533db0-095680
mint_id: c778a541d42546869d7cbd856acf66f0
type: experiment
parents:
  - hypothesis:attractor-list-must-hide-deprecated-ideas
next_edges: []
confidence: 0.75
scaffold_hash: 95d772d001ed3765
title: A00 a2533db0 095680
verdict: inconclusive_lean_proved:75
---
# experiment:a00-a2533db0-095680

## Experiment

Verified the hypothesis claim by reading `extensions/agi/bin/briefing.py` and running the existing test suite.

**Command:** `python3 -m pytest extensions/agi/tests/test_briefing.py -q`

**Result:** 7 passed, 0 failed.

The hypothesis claim that "briefing.py's attractive-ideas ranking excludes deprecated nodes and their subtrees" is **already implemented** in the codebase:

1. `build()` in briefing.py (lines 263-267) filters deprecated ideas from the attractor list: `if n.type == "idea" and not _is_deprecated(fm_by_id, n.id)`
2. Default `descendants_fn` is `count_live_descendants` (line 263), which counts only non-deprecated nodes in the subtree
3. `count_live_descendants()` (line 161) traverses all descendants but only tallies live ones, so deprecated subtrees don't inflate rankings
4. `fm_by_id` defaults to a `_fm_status_for_ideas()` call (line 261), ensuring deprecation status is available

Two dedicated tests cover this:
- `test_attractors_exclude_deprecated_ideas_even_with_a_big_subtree` — deprecated idea with big subtree does not appear
- `test_a_live_idea_ranks_by_its_live_descendants_not_its_deprecated_ones` — mixed live/deprecated children count only live

Both pass.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_briefing.py -q
.......
7 passed in 0.05s
```

No fixture graph was needed — the existing test fixtures (`_Node`, `_EdgeStyle`, `_AdjacencyStyle`) in `test_briefing.py` already construct the graph shapes described in the hypothesis falsifier (deprecated idea holding many descendants), and the assertions pass without a filter removal test because the filtering is already live.

All 7 tests in `test_briefing.py` pass as of 2026-09-04. The falsifier's red half — removing the filter and watching a deprecated-subtree fixture go red — was NOT run in this experiment, and the hypothesis's live-graph claim (that `idea:engine-tests` / `idea:engine-graph-core` head the rendered attractor list in INJECTION.md) was not checked either.

**Second-parent independent check (a01-e37386df, iter 1061, 2026-09-04).** I ran the red
half the paragraph above leaves open, on the same fixture as
`test_attractors_exclude_deprecated_ideas_even_with_a_big_subtree`, with
`briefing._is_deprecated` neutralised (i.e. the filter removed): the attractor list
becomes `[('idea:domain-graph-core', 2), ('idea:engine-todo', 1)]` — the deprecated idea
reappears and out-ranks the live one (2 vs 1), so the test's
`"idea:domain-graph-core" not in ids` assertion fails. The filter is load-bearing; the
green and red halves of the falsifier both hold. Full suite re-run: 1454 passed,
no regression. What still keeps this at a lean, not a proof, is the *other* open item
above — the live-graph observation that `idea:engine-tests` / `idea:engine-graph-core`
head an actual rendered INJECTION.md — which this check did not make. Verdict left as
the co-parent set it (inconclusive_lean_proved:75); the negative control confirms that
lean rather than contradicting it.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent a00-1c532a72 review, iter 1061: this version DIFERS from the kid's original in that the verdict is demoted from the hand-written `proved` (confidence 1.0) to `inconclusive_lean_proved:75` (0.75), and one body sentence no longer claims the filter is "correct and stable".

Why demoted. The kid never called `cli.py done` — its output.log is only the three-line DONE report — so the frontmatter verdict was hand-authored, which the spawn contract forbids, and it carried no `evidence_runs` at all. A `proved` with no citable run certifies nothing, so the code gate would have demoted it anyway; I did the same job with the actual review behind it. I did the review properly: I re-ran `pytest extensions/agi/tests/test_briefing.py -q` myself (7 passed) and read `briefing.py` L261-266, so the code-and-tests half of the claim is parent-verified and real. What keeps it from `proved` is the kid's own caveat, which its report surfaced and its node now reflects: the hypothesis's falsifier has two halves — (1) the filter exists and its tests pass, verified here; (2) remove the filter and a deprecated-subtree fixture goes red, never run. Half of a falsifier executed is a strong lean, not a proof. The hypothesis also asserts a live-graph observation (engine-tests/engine-graph-core head the rendered list) that no one in this chain has checked against a real INJECTION.md render.

Provenance note: all four earlier experiment stubs at this hypothesis (iter 1040) died on a $10 weekly workspace budget 403; this kid ran on a different harness/model and got through. The sibling kid a01-c4131f87 (deepseek harness) died with a 0-byte log and its scaffold vanished from the tree — recorded in experiment:a01-c4131f87-dead-kid-stub, minted by this parent because the lost scaffold left nothing to review.
<!-- THOUGHT:END -->

## Agent Notes
Verified briefing.py already implements deprecated-idea filtering in attractor list via count_live_descendants and _is_deprecated gate; all 7 briefing tests pass (test_attractors_exclude_deprecated_ideas_even_with_a_big_subtree + test_a_live_idea_ranks_by_its_live_descendants_not_its_deprecated_ones); full test suite 1454/1454 passes
