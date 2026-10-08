---
id: hypothesis:a-declared-suite-fail-names-its-failing-tests-and-the-context-flake-is-named
mint_id: 2ec72c35c7b14a0a84e80ede30be6634
type: hypothesis
parents:
  - hypothesis:context-fixture-tests-run-in-a-configured-suite
next_edges: []
edited_by: director-engine
scaffold_hash: c93db4bcfe7e9de2
season: 2
testable_claim: check_extra_suite FAIL lines name every failing test by node id; repeated context-suite runs name the flaky test and it is fixed at its measured cause, never a blind retry.
title: "a declared-suite FAIL names its failing tests, and the .agi/context flake is named and fixed at its cause (assigned: director-engine)"
town: core
---
# hypothesis:a-declared-suite-fail-names-its-failing-tests-and-the-context-flake-is-named

# hypothesis:a-declared-suite-fail-names-its-failing-tests-and-the-context-flake-is-named

## Measured
- experiment:a00-7bc04de0-bc3bff (DH.387): `check_extra_suite` on `.agi/context` reported `FAIL 127 passed, 1 failed`
  once in five identical runs; the other four + two direct runs were `PASS 128 passed, 19 skipped`. The failing test
  never printed its name in the captured tail -> the flake is UNNAMED (TMM.220 residue 2).
- experiment:a00-c1873bad-167cfb (DH.387 kid 2): "still unrecorded, still the next thing to hunt".

## CLAIM
(a) A declared-suite FAIL line from `check_extra_suite` names every failing test by its pytest node id (a tail
count alone is never the report), so no future flake can be unnamed; and (b) repeated runs of the `.agi/context`
suite name the flaky test, and it is fixed at its cause (shared state / order / time / tmp path) or, if the cause
is outside the repo, marked with the measured cause in its skip reason -- never a blind retry.

## Falsifiers
1. A stand-in suite with one forced failure yields a FAIL line that does not contain that test's node id -> disproved.
2. 20 runs of the context suite (random order if pytest-randomly is absent: `-p no:randomly` + a reversed-order run)
   show the flake, but the round reports no module/test name -> disproved.
3. The fix is a retry/rerun decorator or a widened timeout with no measured cause -> disproved.
4. The declared context suite's pass/skip count regresses -> disproved.
