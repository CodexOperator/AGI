---
id: hypothesis:l2-bin-help-smoke
mint_id: 3ba5792c06324e0f8f43c677dcb16420
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: director
scaffold_hash: 1faba3d318b21cd7
season: 1
testable_claim: A single test runs every script under extensions/agi/bin with --help in a subprocess and fails on any non-zero exit, so an unimported name in a main() path is caught by the suite instead of by the next dispatch
thought_session: agi-master-2026-09-06
title: "L2 g15: l2-bin-help-smoke"
---
# hypothesis:l2-bin-help-smoke

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
Observed L2.07: dispatch.py main() referenced spawn_gate without an import (added in L2.06 by a kid); 1539 tests green; every parent spawn died with NameError. FILE: extensions/agi/tests/test_bin_help_smoke.py (new). RULE: for every *.py directly under extensions/agi/bin (not adapters/, not files starting with _), run python3 <script> --help with a 20 second timeout and assert exit code 0 and non-empty stdout; scripts that legitimately have no --help are listed explicitly in the test with a one-line reason each, not skipped silently. If a script fails today for a reason other than a missing import, fix the script rather than listing it, unless the fix is out of scope, in which case list it with the reason and name it in your experiment. VERIFY: the test is red when you temporarily remove the spawn_gate import from dispatch.py and green with it; suite green via python3 extensions/agi/bin/commands.py run tests. REPORT: one experiment node under this hypothesis, verdict, evidence_runs list, outputs. Do not commit, push, or run grid.py commit.
