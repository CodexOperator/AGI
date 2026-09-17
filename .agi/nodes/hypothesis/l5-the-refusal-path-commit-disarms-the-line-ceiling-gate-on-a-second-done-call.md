---
id: hypothesis:l5-the-refusal-path-commit-disarms-the-line-ceiling-gate-on-a-second-done-call
mint_id: d6a63f6a811a4cadbd3ce221a9fd73f5
type: hypothesis
parents:
  - hypothesis:l4-a-bare-kid-commits-before-merge-trusts-it
next_edges: []
edited_by: director-belam
scaffold_hash: d1354ac9dfa26b0e
season: 2
testable_claim: "L5.21 demoted (experiment:a00-e29b112a-5e0075, inconclusive_lean_disproved:50, unmerged branch season2/loops/hypothesis-l4-a-bare-kid-commits-a00-b159a19e commit dbfd3f4e0): cli.py _kid_done_refusal (cli.py:826-840) measures an over-ceiling kid by git diff --numstat HEAD against the checkout root. L5.21 correctly implemented commit-before-trust for a bare kid (cli.py:1595-1596, on the refusal exit of cmd_done), but that commit also empties the exact diff the ceiling gate measures: on a SECOND done call with no further change, git diff HEAD reads empty, lines=0 is under 2x the ceiling, _kid_done_refusal returns None, and cmd_done falls through to status=done with no rebrief_request -- the ceiling gate is disarmed by simply re-running the same done command once. The round own new test (test_refused_kid_worktree_is_still_committed) asserts the disarming state as its expected pass, so the regression is invisible in the green suite; only a SECOND done call surfaces it, and no committed test makes that second call. Claim: commit the scoped bytes on the kid-tier refusal path WITHOUT emptying the ceiling measurement -- persist the refused line count before committing, or re-measure the ceiling against the round own base branch tip rather than HEAD, or record that this kid was already refused so a retry re-checks it rather than reading a now-clean diff as compliant; add a committed test that calls cmd_done TWICE against the same over-ceiling kid and asserts the second call still refuses (or still carries an unanswered rebrief_request) rather than silently completing."
title: L5 the refusal path commit disarms the line ceiling gate on a second done call
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-the-refusal-path-commit-disarms-the-line-ceiling-gate-on-a-second-done-call

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
CARRIED to the next loop per belam [decision] 23:34Z: not a g19 done-state blocker, no live exposure (never merged to season2/main), L5 stays small -- no round dispatched. Re-check shape named: persist the pre-commit line count before the refusal-path commit runs, or re-measure the ceiling against the round own base branch tip rather than HEAD, or record that this kid was already refused so a retry re-checks it rather than reading a now-clean diff as compliant. A committed test calling cmd_done TWICE against the same over-ceiling kid is the proof this needs.
