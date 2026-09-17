---
id: hypothesis:l4-a-suite-run-never-spawns-a-second-detached-pytest-the-spawning-test-is-named-and-stubbed-and-the-runner-refuses-under-pytest
mint_id: 5201db4da5614889807595550c2f771f
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
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
