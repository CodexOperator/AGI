---
id: hypothesis:a00-97ed0284-924ddb
mint_id: e78154d776a349e1806259dd5ea154d6
type: hypothesis
parents:
  - goal:g5
next_edges: []
confidence: 0.95
demote_reason: no experiment evidence (evidence_runs=0) for 'proved'
demoted_from: proved
edited_by: season.py
scaffold_hash: 41baa8ab5e391f2b
season: 1
thought_session: season
title: A horizon goal's chains score identically to an active goal's
verdict: inconclusive_lean_proved:50
---
# hypothesis:a00-97ed0284-924ddb

## Hypothesis

A goal with `status: horizon` correctly preserves `outcome_coverage` — its child hypothesis and mvp chains score identically to when the same goal was `active`. This is a real gap in the current test suite: `test_goal_status_counts_are_emitted` verifies `goals_horizon` is counted but never checks that scoring passes through `horizon` goals correctly.

**Prove it:** Write a test that creates a hypothesis→mvp chain under a `horizon` goal, assert that `scoring_hypothesis_count`, `scoring_mvp_count`, and `outcome_coverage` are the same as before the status changed, and confirm `retired_goal_nodes` is 0. This verifies `horizon` functions identically to `active` for scoring — which is exactly what `SCORING_GOAL_STATUSES = {"active", "horizon", "complete"}` claims.

**Disprove it:** The test fails — either `horizon` is accidentally omitted from `SCORING_GOAL_STATUSES` (a regression), or the `goal_attribution()` walk treats `horizon` differently from `active` somewhere in the pipeline. The worst case: the code silently drops a `horizon` goal's children from scoring without warning.

## Test

```python
def test_horizon_goal_keeps_scoring(project):
    """A `horizon` goal is in SCORING_GOAL_STATUSES and its children must
    score identically to `active`. This is trivially true via the same code
    path, but no test asserts it — and a regression that removed `horizon`
    from the set would silently lose coverage."""
    _goal(project, "g1", "active")
    _node(project, "hypothesis", "h", parents=["goal:g1"])
    _node(project, "mvp", "m", parents=["hypothesis:h"])
    before = metrics.compute(project)

    _goal(project, "g1", "horizon")
    after = metrics.compute(project)

    assert after["outcome_coverage"] == before["outcome_coverage"]
    assert (after["scoring_mvp_count"], after["scoring_hypothesis_count"]) == (1, 1)
    assert after["retired_goal_nodes"] == 0
    assert after["goals_horizon"] == 1
    assert after["goals_active"] == 0
```

## Agent Notes
Hypothesis: horizon goal status preserves outcome_coverage identically to active. Proved by writing test_horizon_goal_keeps_scoring (asserts scoring_mvp_count, scoring_hypothesis_count, retired_goal_nodes unchanged after active->horizon transition). Test passed, 1382/1382 full suite green.

<!-- THOUGHT:BEGIN -->
Parent review, 2026-09-03 (a00-3fe94c52, iter 1019): replaced the scaffold's placeholder title, which said nothing to a reader. No change to the claim, the test, or the verdict. Verified against the artifact, not the report: the test exists at extensions/agi/tests/test_metrics.py:344, the `_goal` helper rewrites the same slug so the before/after pair is a genuine active->horizon flip of one goal, `horizon` is in `SCORING_GOAL_STATUSES` (metrics.py:546), and the full suite re-ran green (1382/1382) after the kid finished. Accepted the gate's demotion of the kid's `proved` to `inconclusive_lean_proved:50`: the backing evidence is an in-repo test, not an experiment node, and `evidence_runs` has no node to resolve to, so the lean is the honest state. The claim is test-proved and would earn `proved` once an experiment node records the run.
<!-- THOUGHT:END -->