---
id: experiment:a00-737e29f7-e656af
mint_id: 9f5555e53c924f9895349d473ac4e016
type: experiment
parents:
  - hypothesis:l3-dispatch-env-leaks-into-tests
next_edges: []
confidence: 0.7
edited_by: ubuntu
evidence_runs:
  - experiment:a00-737e29f7-e656af
loop: hypothesis:l3-dispatch-env-leaks-into-tests@s1
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 3866da61fb541993
season: 1
title: A00 737e29f7 e656af
verdict: inconclusive_lean_proved:75
---
# experiment:a00-737e29f7-e656af

## Experiment

Tested hypothesis:l3-dispatch-env-leaks-into-tests — that a dispatched agent's
spawn env (AGI_LOOP, AGI_MODEL, AGI_ROLE, AGI_TIER, AGI_SEASON, AGI_PROFILE,
AGI_PROJECT_ROOT, AGI_LADDER_TIER) leaks into test runs and the driver,
breaking verification.

The spawned env WAS live (8 AGI_* vars set: see Evidence). Two observations:

1. pytest suite was already green in the dispatch env BEFORE any change
   (1741 passed, 1 skipped) — the original "8 failures" from L3.01 no longer
   reproduce (code moved on). The "same green suite" half of the claim held
   de facto, but NOT because anything stripped AGI_* — nothing did.
2. driver.sh --smoke DID crash: `ERR: not a loop label:
   'hypothesis:l3-dispatch-env-leaks-into-tests@s1'`. Because the driver does
   `loop="${CURRENT_LOOP:-${AGI_LOOP:-}}"` and dispatch exports AGI_LOOP as a
   full label (hypothesis:x@s1, never a bare loop label), `locations.py
   --claim-iter` rejected it. The L3.04 addendum half reproduced exactly.

Implemented the fix on both sides:

- extensions/agi/conftest.py: added a session-scoped autouse fixture
  `_agi_env_stripped` that deletes every AGI_*/AUTORESEARCH_* key from
  os.environ before any test imports (documented AGI_DISPATCH_VARS list + a
  glob), restoring them at session teardown. The spawning process's variables
  are untouched — only the test subprocess is cleaned.
- extensions/agi/driver.sh: added `pick_loop`, which honours CURRENT_LOOP
  always, and falls back to AGI_LOOP only when it is a bare loop label
  (`^[A-Za-z][A-Za-z0-9_-]*$`). A dispatched spawn label is therefore ignored
  and locations.py makes the config/newest-loop fallback instead of crashing.
  `iter_run` now calls `pick_loop`.
- extensions/agi/tests/test_agi_env_strip.py: 5 regression tests — conftest
  strips the documented spawn set; and the REAL pick_loop (extracted from the
  checked-in driver.sh via awk) ignores a dispatch label, honours a real loop
  label, and lets CURRENT_LOOP win.

Verification commands and actual output:

    # under live dispatch env (8 AGI_* vars set):
    env | grep -c '^AGI_'            -> 8
    python3 -m pytest extensions/agi/tests/ -q
        -> 1750 passed, 1 skipped in 96.68s
    python3 -m pytest extensions/agi/tests/test_agi_env_strip.py -v
        -> 5 passed

    # pick_loop logic against dispatched/honest/CURRENT cases (bash unit):
    accelerated by awk-extraction, all 5 cases returned the expected loop.

## Evidence

Observed spawn env (the exact leak under test):

    AGI_LADDER_TIER=0
    AGI_LOOP=hypothesis:l3-dispatch-env-leaks-into-tests@s1
    AGI_MODEL=~deepseek/deepseek-v4-flash-latest
    AGI_PROFILE=balanced
    AGI_PROJECT_ROOT=/home/ubuntu/work/agi/.agi
    AGI_ROLE=kid
    AGI_SEASON=1
    AGI_TIER=kid

Red (before fix) driver crash, inside dispatch env:

    bash extensions/agi/driver.sh --smoke --max-iters 1 | tail
        [driver] ...
        ERR: not a loop label: 'hypothesis:l3-dispatch-env-leaks-into-tests@s1'

green (after fix) suite under the SAME dispatch env:

    python3 -m pytest extensions/agi/tests/ -q
        -> 1750 passed, 1 skipped in 96.68s

`pick_loop` cases (isolated, avoiding a full driver run that would claim an
iteration dir): CURRENT='' + AGI=hypothesis:x@s1 -> ""; CURRENT='' + AGI=L3
-> L3; CURRENT=iter-L3.06 + AGI=x@s1 -> iter-L3.06.

Caveat: I deliberately did not run the FULL `driver.sh --smoke` post-fix,
because a real driver run claims an iteration directory (sessions/iter-NNN).
During my red test of the clean-shell path it did claim and I deleted the
empty stray it left. The crash path is closed by pick_loop returning empty
(claim_iter never receives the bad --loop); end-to-end exit-0 of --smoke under
a dispatched AGI_LOOP is inferred, not witnessed.

Also spotted (out of scope, separate chain): a clean-shell `driver.sh --smoke`
still hits an AttributeError in write_guard.py L276
`logged_path = log.get(sha)` (`log` is a tuple, not the dict) — a genuine
separate defect, unrelated to this hypothesis.

## Agent Notes
conftest strips AGI_* for test proc + driver pick_loop ignores dispatched AGI_LOOP; suite 1750 passed/1 skipped under live 8-var dispatch env; driver --smoke crash closed

Accepted: conftest AGI_* strip + driver pick_loop + 5 regression tests; suite green under live dispatch env. Demoted verdict proved -> inconclusive_lean_proved:75 because tests-half causality unshown (already green pre-fix); driver-half reproduced and fixed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review demotes from proved: the tests half did NOT independently reproduce — the suite was already green (1741 passed/1 skipped) inside the dispatch env BEFORE any change, so "because the test runner strips the AGI_* vars" is not shown to be causal (the strip is sound preventive hardening, not the thing that made it green). The DRIVER half DID reproduce and is fixed: dispatched AGI_LOOP=hypothesis:x@s1 crashed iter_run ("ERR: not a loop label"); pick_loop now ignores spawn labels and honours CURRENT_LOOP, regression-tested by tests that extract the real function from driver.sh. conftest session-scoped autouse strips AGI_*/AUTORESEARCH_* for the test proc and tests assert zero survive. Full suite green under live 8-var dispatch env (1750 passed/1 skipped) + 5 regression tests pass under a clean shell run of the strip test. Defect class is real (driver proved it), fix is good, but the headline symptom (leak breaking the suite) did not reproduce at this code version — hence lean-not-proved, kept with the fix in place.
<!-- THOUGHT:END -->
