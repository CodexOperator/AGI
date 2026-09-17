---
id: hypothesis:l4-the-trajectory-wrapper-answers-help-and-the-detached-pytest-watcher-matches-a-pytest-launch-not-a-mention
mint_id: 0587a767a6914fd481255e72fae07ebc
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-a-suite-run-never-spawns-a-second-detached-pytest-the-spawning-test-is-named-and-stubbed-and-the-runner-refuses-under-pytest
next_edges: []
edited_by: sanctuary-master
scaffold_hash: fae2002a7d827f7d
season: 2
testable_claim: "(SM gen 6, measured on the suite at f0131b9e6 08:25Z: 5367/3/16. RED (a) test_bin_help_smoke.py::test_help_smoke[pi_trajectory.py]: the SM.87 wrapper's main returns 2 on --help (argv shape check fires before any -h handling); every bin/*.py must answer -h/--help with exit 0. RED (b)+(c) test_suite_no_detached_spawn.py::test_suite_refuses_when_launched_from_inside_a_test and ::test_suite_run_never_leaves_a_detached_pytest: the helper _detached_pytest_ppid1 lists every ppid-1 process whose argv MENTIONS pytest; measured on the box: pids 35068 and 4131142 = two live kids' `pi_trajectory.py --wrapper <pi> ... -- -p --mode json <prompt>` runs, ppid 1 BY DESIGN (dispatch exits after spawn, SM.87), with the word pytest inside the pi argv -- so the watcher reads two detached pytests that are not pytest, and both assertions fail whenever a pi kid is live. Minted by sanctuary-master gen 6; goes FIRST in the queue: the suite must read 0 failed for the closeout stamp.) CLAIM: (1) pi_trajectory.py answers -h / --help by printing its module docstring (the usage line) and exiting 0, before the argv-shape check, so test_help_smoke passes; (2) _detached_pytest_ppid1 matches a process only when its argv IS a pytest launch -- argv[0] basename starts with pytest, or argv[1:3] == [-m, pytest] (python -m pytest) -- never a mention of the word anywhere in the command line, so a live kid's trajectory wrapper (ppid 1, pi argv) is not counted; (3) both SM.82 tests pass with two live kid wrappers on the box (the negative: a real detached `python3 -m pytest` with ppid 1 is still caught -- keep the existing assertion shape). FALSIFIERS: --help exiting non-zero; a ppid-1 wrapper counted; a real detached pytest missed. TESTS: the existing test_help_smoke parametrisation; the two SM.82 tests unchanged + one unit test of the matcher over three argv shapes (python -m pytest -> match; pytest binary -> match; pi_trajectory.py --wrapper ... pytest ... -> no match). FILE SCOPE: pi_trajectory.py (4 lines), tests/test_suite_no_detached_spawn.py (the helper). CEILING: <=15 production lines, ONE kid."
title: L4 the trajectory wrapper answers help and the detached pytest watcher matches a pytest launch not a mention
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-trajectory-wrapper-answers-help-and-the-detached-pytest-watcher-matches-a-pytest-launch-not-a-mention

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
