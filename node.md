---
id: hypothesis:l3-dispatch-env-leaks-into-tests
mint_id: 493b9647049f4ec7bfacdbf7a93fdf3b
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: ubuntu
scaffold_hash: 4b11c345902a1248
season: 1
testable_claim: A kid or parent running the engine suite from inside a dispatched environment sees the same green suite as a clean shell, because the test runner strips the AGI_* spawn variables (AGI_LOOP, AGI_MODEL, AGI_ROLE, AGI_TIER and siblings) that dispatch exports
title: L3 dispatch env leaks into tests
---
# hypothesis:l3-dispatch-env-leaks-into-tests

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OBSERVED L3.01 (kid a00-e34d54e1 and parent a00-346c6028): the full suite shows 8 failures when run inside the dispatched environment because dispatch exports AGI_LOOP, AGI_MODEL and siblings into the kid's env; the kid had to discover env -u to get 1685 green. Same class as hypothesis:l2-commit-guard-scope (trap k: AGI_TIER=kid broke 99 tests until the commit guard was scoped). FILES: extensions/agi/bin/commands.py (run tests), extensions/agi/tests/conftest.py, tests. FIX: the tests command and a session-scoped autouse fixture in conftest.py clear every AGI_* variable for the test process (monkeypatch.delenv on a documented list, plus a glob), so a kid's verification never depends on its spawn env; keep the variables in the spawning process untouched. VERIFY: red-first test that sets AGI_LOOP and AGI_MODEL and asserts a subprocess suite slice is green; run the suite with AGI_LOOP=x AGI_MODEL=y exported and show 1685 passed. REPORT: one experiment node under this hypothesis, verdict, evidence_runs as a list (pass --evidence-runs), every verify command with its actual output in the body. Do not commit, push, or run grid.py commit.

ADDENDUM L3.04 (belam): the same leak reaches driver.sh: the goals-active kid reported bash driver.sh --smoke exits 1 inside its dispatched env with a dispatcher loop-label error (dispatch exports AGI_LOOP as L3.04@s1 and the driver's loop-label parsing rejects it) while the same command exits 0 from a clean shell. Fix in the same pass: the driver and the test runner both clear or ignore the spawn-time AGI_* variables, with a red-first test for the driver path too.

STRAY FOLDED 2026-09-07 (belam): a kid left .agi/autoresearch.ideas.md again (pi-autoresearch scratch, deleted as in L2.12; this note is the durable copy): # Autoresearch ideas (deferred, not lost) ## Env-leak into tests — lane (L3.06) — now CLOSED, all three layers - LAYER 1 test-runner: conftest.py session autouse strips AGI_*/AUTORESEARCH_* for the pytest process (documented list + glob, restore at teardown). - LAYER 2 driver: `pick_loop` in driver.sh honors CURRENT_LOOP, and falls back to AGI_LOOP only when it is a bare loop label, so a dispatched spawn label is ignored. - LAYER 3 source: `loop_label()` in locations.py now *skips* a dispatch-spawn AGI_LOOP (falls through to config/disk) instead of raising, for every caller; an invalid EXPLICIT flag still raises. - Verified: suite green (1754 passed / 1 skipped) under the live 8-var dispatch env; driver --smoke crash closed; 9 regression tests total (5 in test_agi_env_strip.py, 4 in test_locations.py). Lane exhausted; do not re-mint. ## STALE — do not re-mint - write_guard.py L276 `log.get(sha)` AttributeError: resolved to EXIT=0; was a transient from a parallel kid's in-flight edit of write_guard.py (uncommitted, theirs). - The ORIGINAL "8 failures" from L3.01: already gone before any fix; only the driver crash half was ever live.
