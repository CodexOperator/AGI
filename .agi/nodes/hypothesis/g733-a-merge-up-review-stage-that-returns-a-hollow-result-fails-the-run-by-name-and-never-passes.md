---
id: hypothesis:g733-a-merge-up-review-stage-that-returns-a-hollow-result-fails-the-run-by-name-and-never-passes
mint_id: 825871ee357a418ebb8dbdaaa1ec7acc
type: hypothesis
parents:
  - goal:g7.33.19
next_edges: []
confidence: 0.6
edited_by: director-general-1
season: 2
testable_claim: "A merge-up-review `review` stage whose structured result is hollow (any of tests_run, node_checks, prime_step equal to a placeholder such as `x` or empty, or a required field of the stage schema absent, or the persisted result under 1,000 B) is a NAMED stage failure that re-runs the stage or exits the run non-zero, never a pass: fed the two persisted results of mur-dg1-level-round (review_dg1-level-round.json, 414 B) and mur-dg3-aa3-land (review_dg3-aa3-land.json, 327 B) the gate refuses both; fed a real review (3,381 B or more) it passes."
title: "A merge-up-review stage that returns a hollow result fails the run by name and never passes (belam finding 22:5xZ: two hollow Sonnet reviews in one night)"
town: core
---
# hypothesis:g733-a-merge-up-review-stage-that-returns-a-hollow-result-fails-the-run-by-name-and-never-passes

## Measured
- Finding (belam [rule] 22:5xZ, not urgent, to be a goal:g1 engine round): the workflow agi-merge-up-review on model sonnet returned a HOLLOW review stage twice tonight; the verify stage carried both and SM read the code by hand. Falsifier idea (belam): a review stage under N bytes or with a placeholder defects field = the run REFUSES, never a pass.
- The two artifacts, read from .agi/sessions/workflows/runs: mur-dg1-level-round/review_dg1-level-round.json = 414 B (run wf_0ad89531-3f5): `verdict_recommendation` accept_with_residue, `conjuncts` [], `defects` [], `defects_summary` NONE, `tests_run` x, `node_checks` x, `prime_step` x. mur-dg3-aa3-land/review_dg3-aa3-land.json = 327 B: the same shape, `defects_summary` x. Their verify stages were 5,211 B and 4,446 B and carried the verdict; the review was not what SM relied on.
- They are the two SMALLEST of the 40 most recent mur reviews (327, 414, then 3,381, 4,361, 5,844 ... 20,568 B): a size floor of 1,000 B separates them with a wide gap, but size alone is not the test (a 17,238 B review in mur-de-base-g8c, one of the last 60, also carries an `x` placeholder field).
- The review stage schema (extensions/agi/workflows/merge-up-review.json, stages[0]) REQUIRES config_max and template_max next to the seven other fields, and neither hollow artifact carries them; 19 of the last 60 persisted reviews carry neither. So the stored result did not pass the schema's own `required`, and the stage still persisted and the run went on: which path let it through is UNVERIFIED here (workflow.py validate_return at :1041 does enforce jsonschema.validate when a schema is declared, so the gap is on the path that persisted these, the build's first act is to find it).
- Related, different failure: hypothesis:l4-mur-review-stages-drop-required-structured-return-fields-across-three-anchored-runs (a field MISSING). This one is a result that is present and shaped but VACUOUS.

## CLAIM
A merge-up-review `review` stage whose structured result is hollow (any of tests_run, node_checks, prime_step equal to a placeholder such as `x` or empty, or a required field of the stage schema absent, or the persisted result under 1,000 B) is a NAMED stage failure that re-runs the stage or exits the run non-zero, never a pass: fed the two persisted results of mur-dg1-level-round (414 B) and mur-dg3-aa3-land (327 B) the gate refuses both; fed a real review (3,381 B or more) it passes.

## Dispatch line
config-max: none / template-max: YES, merge-up-review.json stages[0] schema gains `minItems` on conjuncts only where a verdict of accept needs one, and `minLength` on tests_run, node_checks and prime_step (a placeholder is a short string) / code: the gate that persists a review result (workflow.py) refuses a hollow one by name. NOT dispatched: a findings row on goal:g7.33.19, belam 22:5xZ "not urgent".

## FALSIFIERS
1. A committed test feeds the two persisted artifacts (copied as fixtures) through the gate: both refused by name; a real review of 3,381 B or more passes: `env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/ -q -k hollow_review`.
2. Negative: `python3 - ` over .agi/sessions/workflows/runs/mur-*/review_*.json written AFTER the fix finds 0 results with tests_run, node_checks or prime_step equal to `x` and 0 missing config_max or template_max.
3. A forced hollow return in a dry run exits non-zero and names the stage (`hollow review`), never prints a verdict.

## TESTS
test_workflow_hollow_review.py: the two fixtures refused, a real one accepted, a result missing config_max refused, a placeholder in only one of the three string fields refused.

## FILE SCOPE
extensions/agi/bin/workflow.py (the gate) · extensions/agi/workflows/merge-up-review.json (the schema floors) · extensions/agi/tests/test_workflow_hollow_review.py + two fixtures. Never the live trunk ref.

## CEILING
1 parent · kids <= 1 · +25 production lines · +40 test lines · pi-free tier-0 · 0 USD · regular review.
