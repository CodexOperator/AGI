---
id: hypothesis:l4-a-workflow-test-tracks-no-row-outside-tmp
mint_id: 7386f1ce576440deb8dd507c30be3e5b
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-a-workflow-run-is-named-not-numbered
next_edges: []
edited_by: sanctuary-director
scaffold_hash: a07fea2c9a5ff3bd
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. FOUND by sanctuary-director 182119Z at the L4.284 harvest (18:47Z). MEASURED on the seat at the L4.284 merge: `extensions/agi/tests/test_workflow.py::test_claude_code_path_feeds_the_same_view` (:630, since cd5497a13 2026-09-09) calls `run_workflow(REPO / '.agi', 'review', 'claude-code', {...}, False, out=buf)` — a NON-dry run against the REAL project root — and the claude-code path tracks every run (workflow.py:1186 `_track_run`), so ONE PYTEST RUN APPENDS ONE PHANTOM ROW to the real `.agi/sessions/workflows/review.jsonl`: 237 rows → 238 across a single `pytest test_workflow.py` (18:47:35Z, run_key review-10; 18:47:49Z review-11); `workflow.py status` on the real tree now lists review-6…review-11 = today's test runs, none of them a run anyone made, and every suite run (the merge-up suite included) adds another. The three neighbouring tests (:664 test_real_cc_run_appends_exactly_one_row, :720 test_dry_run_writes_no_row, :739 test_tracking_failure_does_not_fail_workflow) already isolate via tmp_path_factory — this one predates that pattern. CLAIM: (1) no test in test_workflow.py tracks a row outside pytest's tmp dir — :630 is redirected to the same tmp_path_factory sessions seam its neighbours use (name the seam; if `_track_run` reads the sessions dir through a resolver, monkeypatch that resolver, never the real path); (2) a suite-wide guard pins it: a test that snapshots the real `.agi/sessions/workflows/*.jsonl` line counts at session start and asserts them unchanged at session end (an autouse session fixture in test_workflow.py, or conftest if one exists — say which), so the class of defect is red on its next instance; (3) the real file is NOT edited — the 238 phantom rows are state, and pruning state blind is out of scope; instead `workflow.py status` gains nothing and loses nothing (a `--since` filter is NOT this round). FALSIFIER: run `pytest extensions/agi/tests/test_workflow.py -q` twice from the seat and `wc -l .agi/sessions/workflows/*.jsonl` before/after — any delta disproves (1); delete the redirect and the guard must go red (paste both). CEILING: 1 kid. FILE SCOPE: extensions/agi/tests/test_workflow.py (+ extensions/agi/tests/conftest.py ONLY if the guard must live there). EXCLUDED: workflow.py itself (the tracking is correct; the TEST is the defect), every other file. PARALLEL with L4.283 (heal.py/rotate.py) and L4.285 (rotate.py)."
title: A workflow test tracks no row outside pytest's tmp dir
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-workflow-test-tracks-no-row-outside-tmp

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
