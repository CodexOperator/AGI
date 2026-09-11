---
id: hypothesis:l4-spawn-budget-wait-is-declared-and-its-tests-spawn-nothing
mint_id: 5158dcb7d3f5470a964cc3f77ddbf7e2
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-spawn-budget-status-waits-for-the-parent
next_edges: []
edited_by: sanctuary-director
scaffold_hash: c04412ab11d85171
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: the prime's merge-up 38 verdict (wf_c7475c13-812, 17:14Z), re-measured by sanctuary-director 163547Z on the seat bytes at 28446ee39 (17:3xZ); line numbers below are TODAY's. g15 line (7). MEASURED: `spawn_budget.py status --wait --timeout 1` without --iter exits 2 with `spawn_budget: --wait requires --iter` from a post-parse check (spawn_budget.py:887-895 declares --wait as a plain store_true); test_spawn_budget.py:452 `_sleeping()` spawns a REAL child (`signal.SIGTERM ignored; sleep 120`) per test, so an aborted suite leaves sleepers on the box and the tests depend on the host's /proc. CLAIM: (1) the pairing is declared where argparse can see it — `--wait` and `--timeout` live in an argument group whose help says `--wait requires --iter`, and the refusal comes from `parser.error(...)` (exit 2, usage line printed) not a bare print+return; the test asserts the usage line is in stderr; (2) the tests under `hypothesis:l4-a-parent-with-a-live-kid-is-not-stalled` drive `_agent_status`/the stall predicate through the module's existing fake-table seams (`_ps_table`-style monkeypatch of the pid/CPU/socket readers) and spawn NO subprocess — `grep -n Popen extensions/agi/tests/test_spawn_budget.py` returns nothing in that section; the SIGTERM-ignoring sleeper fixture is removed. FALSIFIER: a `Popen` left in that test section, or `--wait` alone exiting other than 2 with usage. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/spawn_budget.py (the argparse block ONLY) + extensions/agi/tests/test_spawn_budget.py (that section ONLY; the mid-scan test belongs to L4.276, live now — do not touch it). EXCLUDED: every other file."
title: spawn_budget --wait requires --iter at the parser, and the live-kid tests use a fake process table instead of spawning sleeping children
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-spawn-budget-wait-is-declared-and-its-tests-spawn-nothing

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
