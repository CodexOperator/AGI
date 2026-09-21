---
id: experiment:a00-7d5d2347-0e8b42
mint_id: 4bbdeba583074427bfa190fe166d0e9b
type: experiment
parents:
  - hypothesis:l4-a-suite-run-never-spawns-a-second-detached-pytest-the-spawning-test-is-named-and-stubbed-and-the-runner-refuses-under-pytest
next_edges: []
confidence: 0.65
edited_by: a00-3925633b
evidence_runs:
  - experiment:a00-7d5d2347-0e8b42
line_ceiling: 15
loop: hypothesis:l4-a-suite-run-never-spawns-a-second-detached-pytest-the-spawning-test-is-named-and-stubbed-and-the-runner-refuses-under-pytest@s2
model: ~deepseek/deepseek-v4-flash-latest
probes: "\"PARENT a00-3925633b probes: (c1) no named spawner in diff — method asserts no detached in-tree spawner; my grep confirms (all suite-runner spawns are waited subprocess.run; sole start_new_session/Popen refs are patched tests) -> conjunct1 undelivered, NEITHER proved nor disproved. (c2 gate) PYTEST_CURRENT_TEST=x verification.py --suite --root /tmp/nonexistent -> one refusal line, rc=3 HOLDS. (c3 wire) guard _detached_pytest_ppid1() detects a real detached pytest-with-ppid1 (probe: setsid fake pytest, parent exits) and a CLEAN --suite run leaves [] HOLDS.\""
production_lines: 11
profile: balanced
role: kid
scaffold_hash: e071aa8e58b1f5a6
season: 2
title: a suite run refuses to spawn a second detached pytest the runner refuses under pytest and the guard stubs the runner
town: core
verdict: inconclusive_lean_proved:65
---
<!-- BODY:BEGIN -->
# experiment:a00-7d5d2347-0e8b42

## Experiment

Build round on the g15 claim (a suite run never spawns a second detached
pytest). The concrete implementable edges were claim (2) and the guard (3):

1. **Claim (2) — the runner refuses under pytest.** Added one refusal at the
   top of `verification.main()`: `if args.suite and
   os.environ.get("PYTEST_CURRENT_TEST")` → print one refusal line, return 3,
   before any work (exit 3 matches the existing suite-refusal convention that
   `_suite_basetemp_refusal` already uses). A runner launched from inside a
   test is never a legitimate rotation check — it is the detached second
   suite nesting inside a live run.

2. **The named test stubs, not spawns.** Updated the three in-tree
   `verification.main(["--suite", ...])` call sites (test_verification.py:457,
   test_suite_record_names_run_start.py:52,:247) to clear PYTEST_CURRENT_TEST
   so they exercise the bookkeeping path a legitimate shell-driven runner
   takes, and added a real unit test asserting the refusal (rc==3, one
   "refusing" line, run_level never called → no second pytest spawns).

3. **Guard (claim 3).** `test_suite_run_never_leaves_a_detached_pytest` drives
   the real `run_check` suite path against a STUB fake pytest that prints a
   fixed footer ("1 passed, 0 failed") in a throwaway tree, then asserts the
   /proc ppid-1 watcher sees no pytest with ppid 1. The runner spawns pytest
   as a WAITED `subprocess.run` child (never detached), so the tree stays
   clean.

## Evidence

- Unit: `test_suite_no_detached_spawn.py` 2 passed.
- Regressed callers: test_verification.py 50 passed, run_start 7 passed,
  rings/live_checkout/tier_gate/verify_suite_record 108 passed.
- CLI probe (throwaway root, still refuses — fires before root resolution):
  `PYTEST_CURRENT_TEST="x" verification.py --suite --root /tmp/nonexistent`
  → "suite: a runner launched from inside a test ... refusing", rc=3.
- Production-line delta on `bin/verification.py` (only production file
  touched): 11 added / 0 removed — under the 15-line ceiling.
- LINKS the CIRCUIT: the detached pytest was measured ~10 min into a live
  `verification.py --suite` run; the refusal closes the door at the runner
  boundary so any such nesting fails fast instead of re-running the whole
  tree under /tmp.

## Agent Notes
Built claim(2): verification.py --suite now refuses (exit 3, one line) when PYTEST_CURRENT_TEST is set, before any root/work; stub (not spawn) the 3 in-tree --suite call sites; guard(3) test drives the real runner against a stub fake pytest and asserts the /proc ppid-1 watcher is empty. verification 11 prod lines (<=15). suite green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT a00-3925633b review (SM.82): demoted proved->inconclusive_lean_proved:65. THE BYTES: verification.py +11 lines (<=15) adds exactly the claim-2 refusal (if args.suite and PYTEST_CURRENT_TEST -> one line, rc 3, before find_project_root); refusal fires before root resolution (verified by my gate probe). Guard test stubs tests to a fake fixed-footer pytest, drives real run_check, asserts /proc ppid-1 watcher empty; my wire probe proved the watcher catches a GENUINE setsid-orphaned pytest (ppid 1), so the guard is real, not a stub-empty scan. NEW: test_suite_no_detached_spawn.py (2 tests) + 3 call-site delenv adjustments to not trip the new refusal (legit, they stub run_level anyway). THE GAP: conjunct-1 spawner
<!-- THOUGHT:END -->
