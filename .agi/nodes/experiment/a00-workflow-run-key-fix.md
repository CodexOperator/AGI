---
id: experiment:a00-workflow-run-key-fix
mint_id: 413c3aa547074c74be6edaa8bf6e5a59
type: experiment
parents:
  - hypothesis:lm-workflow-run-key-overflows-path-max
next_edges: []
confidence: 0.95
edited_by: director-thought
evidence_runs:
  - experiment:a00-workflow-run-key-fix
scaffold_hash: f6cc9b70f378ddcc
season: 2
testable_claim: See parent hypothesis.
title: "Fixed: added _run_key_path_component() bounding the mkdir path component to 200 bytes with a sha256 digest suffix; _persist_stage_value now writes its stage JSON even when the descriptive run_key is long. Two regression tests added and green, plus the full pre-existing test_workflow.py suite (86 tests) green."
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-workflow-run-key-fix

## Experiment

What did you do? What happened? Include command/inputs and actual outputs.

## Evidence

Raw output, screenshots, logs.

## Agent Notes
"Commit ede3b96bf on local-maxxing/season1/posts/director-thought/main (pushed to refs/agi/posts/director-thought @6287bcac6). Diff: extensions/agi/bin/workflow.py (+hashlib import, +_run_key_path_component, one call-site change in _persist_stage_value) and extensions/agi/tests/test_workflow.py (+test_run_key_path_component_bounds_long_keys, +test_persist_stage_value_survives_a_long_run_key). Verified: (1) short keys unchanged byte for byte; (2) a 350-byte key truncates to <=200 bytes encoded; (3) two long keys sharing a 51-byte prefix produce different truncated directories (no digest collision); (4) _persist_stage_value with a 350-byte key actually writes runs/<truncated>/brainstorm.json and it round-trips through json.loads; (5) full extensions/agi/tests/test_workflow.py suite (86 tests) plus test_workflow_result_file.py, test_workflow_slice_isolation.py, test_workflow_claude_code_branch_names_itself.py, test_workflow_review_under_load.py all green. No formal mur run for this one -- it is a director self-authored engine fix with its own passing tests, not a dispatched kid round; reported to sanctuary-master directly (real cross-session message, owner-instructed) and to thought-master via merge-up DM (tip 6287bcac6)."

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
"This experiment IS the fix, authored directly by the director rather than a dispatched kid, because it was found while reviewing the gen-6 jev brainstorm delivery, was small (one function, one call site), and sanctuary-master said do not hold. Verdict proved on: the mechanism reproduces (a synthetic long key throws before the fix, per the docstring reasoning verified by reading the code path), the fix compiles and both new tests pass, and the pre-existing suite has zero regressions."
<!-- THOUGHT:END -->
