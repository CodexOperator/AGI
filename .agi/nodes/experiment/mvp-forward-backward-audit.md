---
id: experiment:mvp-forward-backward-audit
mint_id: 024a3370dac4415c8b7fa51863adcdc7
type: experiment
parents:
  - hypothesis:an-mvp-that-points-backward-is-score-neutral
next_edges: []
edited_by: director
scaffold_hash: c0048df310572989
thought_session: L1.08
title: Nine mvps audited against the forward-pointing rule; two were backward
---
# experiment:mvp-forward-backward-audit

## Experiment

What did you do? What happened? Include command/inputs and actual outputs.

## Evidence

Raw output, screenshots, logs.

## Agent Notes
"Classification of the 9 mvps named in hypothesis:an-mvp-that-points-backward-is-score-neutral, against [mvp].md's forward-pointing rule ("an mvp points forward at what that build owes rather than containing it"). None was pre-deprecated.

| mvp id | class | deciding line |
|---|---|---|
| a00-84f78e77-3e4524 | forward | "Add a `--workflow` flag to `commands.py run`..." -- flag does not exist (`commands.py` has no `--workflow` arg; `run(root, name, extra)` takes one command name) |
| a00-bd00f723-0fdba2 | forward | Agent Notes: "reap-harvest.py MVP... Spec complete, not yet implemented as code." -- reap-harvest.py does not exist in the tree |
| a00-d164603e-457772 | forward | "bin/resolve-provenance.py (new) -- called by cli.py done or as standalone" -- resolve-provenance.py does not exist |
| a00-e284d9f5-869c8c | BACKWARD | THOUGHT: "The mechanism is real: the script runs, all 15 declared commands render into the marker region of `skills/agi/SKILL.md`, `--check` exits 0 (no drift), and the table matches the node exactly." -- bin/derive-commands.py exists in the tree and SKILL.md carries live COMMANDS:BEGIN/END markers; this is a report of a finished, verified change |
| a00-eeaa5239-8e388f | BACKWARD | THOUGHT: "Verified in-tree: post_wire.py:365 calls is_complete, :371 calls owns_all_complete, completion.py has both functions (lines 55, 94), admitted_by_graph list at line 347. Ran the suite myself: 1382/1382 pass." -- confirmed live at exactly those line numbers |
| a00-fc01ce13-190c60 | forward | "An end-to-end smoke test (`test_smoke_submit.py`) that creates a scratch node..." -- test_smoke_submit.py does not exist |
| a01-0e64d6a7-2b0e12 | forward | THOUGHT: "the kid itself flagged 'spec only, not implemented'" -- no `body` verb in write.py |
| a01-708d8467-8d4eea | forward | "A test that runs every declared command through `commands.run()`..." -- test_every_declared_command_runs_through_the_resolver does not exist in the suite |
| a01-e989877e-4030c2 | forward | "This MVP defines a VerbRegistry that wraps the dict..." -- verb_registry.py does not exist |

7 forward, 2 backward. Verified in-tree by grepping the source tree for each named artifact (derive-commands.py, post_wire.py:365/371, reap-harvest.py, resolve-provenance.py, test_smoke_submit.py, the body verb, test_every_declared_command_runs_through_the_resolver, verb_registry.py, the --workflow flag) rather than trusting the node bodies alone.

Measure: before, `scoring_mvp_count=47`, `outcome_coverage=0.245` (47/192). Excluding the 2 backward mvps by hand: 45/192 = 0.234.

Structural fix chosen over deprecation, since both backward mvps' underlying work is real and worth keeping on record -- only the score credit was wrong. `metrics.py::goal_attribution` now excludes an mvp from `scoring_mvp_count` when it fails a two-part forward-pointing rule (`_BACKWARD_MVP_RE` + no `source_files`/`payload_ref`/build-child), and reports the excluded count as a new `backward_mvp_count` metric. After: `scoring_mvp_count=45`, `backward_mvp_count=2`, `outcome_coverage=0.234`. Fixture tests added to test_metrics.py (7 new); the defect was reintroduced by hand (reverting the exclusion branch to unconditional `scoring_mvp += 1`) and 3 of the 7 went red as expected (`scoring_mvp_count` off by 1, `outcome_coverage` wrong, the METRIC line missing), confirming the tests actually catch the regression. Full suite: 1389 passed (1382 baseline + 7 new), 0 failures."
