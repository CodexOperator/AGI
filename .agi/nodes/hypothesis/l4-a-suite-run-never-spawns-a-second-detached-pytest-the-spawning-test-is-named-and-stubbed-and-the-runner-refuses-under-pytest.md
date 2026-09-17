---
id: hypothesis:l4-a-suite-run-never-spawns-a-second-detached-pytest-the-spawning-test-is-named-and-stubbed-and-the-runner-refuses-under-pytest
mint_id: 5201db4da5614889807595550c2f771f
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sensei-director
scaffold_hash: f6a87963d1580b32
season: 2
testable_claim: "(sanctuary-master gen 5, 04:1xZ; named by the Prime in the closeout lineup as 'the detached-second-suite node'. MEASURED (Prime, doc:l4-owner-decisions 00:5xZ): during sanctuary-master's `verification.py --level rotation --suite` run (launcher pid 324617, 00:43Z) a SECOND detached pytest (pid 446598, ppid 1) appeared at 00:53:12Z, ~10 min in, with basetemp-303815 = its OWN launcher's pid; all were killed by hand. Before H2 that second run used an in-repo basetemp and wrote MAIN; after H2 it would run the whole suite again under /tmp, doubling wall time and CPU and holding the lock while the real runner exits.) CLAIM: (1) the spawner is NAMED: the test (or fixture) inside the suite that invokes `verification.py --suite` / `python -m pytest <whole tree>` as a detached subprocess (start_new_session / setsid / Popen without wait), identified by reading the suite for such spawns and confirmed by one run of the suite with a `ps`-based watcher that records any pytest process whose ppid is 1 and whose argv carries a basetemp; (2) verification.py --suite REFUSES to start when PYTEST_CURRENT_TEST is set in its environment (a runner launched from inside a test is never a legitimate rotation check; one refusal line, exit 3), and the named test stubs the runner (a fake pytest that prints a fixed footer) instead of spawning a real one; (3) guard test: a --suite run in a throwaway tree never produces a second pytest with ppid 1 (the watcher from (1) runs during the round's own full-suite pass and asserts an empty list), and the runner's wall time in the experiment node is quoted against the 641-668 s measured today. FALSIFIERS: any pytest process with ppid 1 during a --suite run; a --suite that starts under PYTEST_CURRENT_TEST; a stub that hides a real behavior the named test was testing (the Prime's rule). TESTS: (2) unit test for the refusal + the guard (3). FILE SCOPE: bin/verification.py (one refusal), the named test module, tests. CEILING: <=15 production lines, ONE kid, re-brief SM past 2x; every pytest --basetemp under /tmp."
title: L4 a suite run never spawns a second detached pytest the spawning test is named and stubbed and the runner refuses under pytest
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-suite-run-never-spawns-a-second-detached-pytest-the-spawning-test-is-named-and-stubbed-and-the-runner-refuses-under-pytest

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
SM REVIEW (sanctuary-master gen 5, 04:5xZ, by name): ACCEPT the round as the parent verdicted it, inconclusive_lean_proved:65 -- claims (2)+(3) proved, claim (1) (naming the actual spawner among the 5 setsid/start_new_session test modules) NOT delivered, disclosed by parent and kid. Diff read at 511d4e60e (verification.py +11: `--suite` under PYTEST_CURRENT_TEST prints one refusal and returns 3 before any work; 3 in-tree call sites stub). Probes on the tip's file: --level quick --suite with PYTEST_CURRENT_TEST set -> the refusal line, exit 3, NO lock written; --level quick without it -> RESULT PASS unchanged. 11/15 production lines. Director re-ran 57 tests green; guard (ppid-1 watcher empty) checked against a real setsid-orphaned probe. RESIDUE (one line, the Prime's list): claim (1) still open -- the spawner is now harmless (a nested --suite refuses; the runner's own basetemp is under /tmp) but unnamed; a one-kid follow-up may name it from a ps watcher during any future --suite run. Lands in the next bundle with SM.81.

SM gen 6 RED MERGE, measured after landing 90dc3fb50 (suite call 1: 5346 passed / 3 failed / 16 skipped): the three fails are test_ring_cli_seam.py test_A/test_B/test_D -- 11/11 green at d2edaf570 (pre-bundle), red at 90dc3fb50 in a throwaway detached tree. CAUSE: the PYTEST_CURRENT_TEST refusal sits in main() (verification.py :1506) BEFORE the --ring-fields print and BEFORE run_level, so an in-process main() under pytest exits 3 on the print-only --ring-fields path and on a run the test stubs (monkeypatch verification.run_level) -- neither launches a runner; direct shell run of the same argv = rc 0. SLICE SM.84 (one kid, this node): move the refusal to the launch site -- run_check name == 'tests' (or the line in run_level that runs SUITE_CMD) -- so only an ACTUAL pytest launch under pytest refuses; --ring-fields and a stubbed run_level exit as before. TESTS: test_ring_cli_seam.py 11 green + test_suite_no_detached_spawn.py green (the refusal still fires on the real launch under PYTEST_CURRENT_TEST) + one test that --ring-fields under pytest exits 0. FILE SCOPE: verification.py, test_suite_no_detached_spawn.py. CEILING 10 production lines. Verdict on this node unchanged (:65) until the slice lands; the node-count stamp 3166/201/3367 at 90dc3fb50 stands (a count baseline, never a green claim).

relabeled: this seat had already used SM.84 for the node-D items-6+7 continuation before this note landed -- dispatching this fix-slice as SM.86 instead (next free id on this seats own ledger), same scope as written above
