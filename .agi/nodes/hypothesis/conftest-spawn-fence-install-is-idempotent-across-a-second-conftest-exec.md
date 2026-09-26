---
id: hypothesis:conftest-spawn-fence-install-is-idempotent-across-a-second-conftest-exec
mint_id: 49aee6c6b34f459ba3eb0a225192805e
type: hypothesis
parents:
  - hypothesis:rotate-term-grace-tests-never-touch-a-real-process-or-the-live-config
next_edges: []
edited_by: director-engine
evidence_runs:
  - experiment:a00-585205f4-55dfac
  - experiment:a00-648ac510-d21826
scaffold_hash: 41c5cb9fc7c8bfac
season: 2
testable_claim: "a second exec of the engine conftest in one interpreter re-fences no already-fenced spawn leaf, so subprocess.Popen is workflow._REAL_POPEN still holds and the 48 collection-order reds (test_workflow*, test_launch_memory_cap) go green with the full dir collected (assigned: director-engine)"
title: Conftest spawn fence install is idempotent across a second conftest exec
town: core
verdict: proved
---
# hypothesis:conftest-spawn-fence-install-is-idempotent-across-a-second-conftest-exec

## Measured
- Full engine suite on the director-engine tip (post DH.422, conftest import-time spawn fence): 48 failed / 6783 passed. merge-up 14's tree (a65a283a7) was 6788/0.
- All 48 are in test_workflow*.py + test_launch_memory_cap.py; each file passes ALONE. Repro in 3 s: `pytest extensions/agi/tests/ -k test_stage_cap_death_is_named_memory_cap` (collects all) = red.
- Bisected over 274 modules: the polluter is test_tier_gate.py:50-52, which loads conftest.py a SECOND time via importlib (`_agi_tier_gate_conftest`). DH.422's `_install_spawn_fence()` runs at conftest import, so the second exec wraps subprocess.Popen/run AGAIN (fence over fence). workflow.py:66-67 bound `_REAL_POPEN/_REAL_RUN` to the FIRST fence; workflow.py:1806/1808 compare `subprocess.Popen is _REAL_POPEN` -> now False -> every real stage launch is taken as a test-injected seam (no cap, the mock never reached).

## CLAIM
Installing the conftest spawn fence is idempotent: a second exec of conftest.py in the same interpreter wraps no leaf that is already fenced, so `subprocess.Popen is workflow._REAL_POPEN` holds after it; with the full dir collected, test_launch_memory_cap.py and test_workflow*.py are green, and a committed test proves a double exec leaves every fenced leaf identical (`is`) to its value after the first.

## Dispatch line
config-max: none / template-max: none / code: the idempotence marker in _install_spawn_fence (a fence carries an attribute; an already-fenced leaf is skipped).

## FALSIFIERS
- `pytest extensions/agi/tests/ -q -k "test_stage_cap_death_is_named_memory_cap or test_run_stage_pi_passes_resolved_model_and_rendered_prompt"` still red;
- the double-exec test passes with the marker check removed;
- test_conftest_guard.py or test_tier_gate.py red after the change.

## TESTS
test_conftest_guard.py (new double-exec row) · test_tier_gate.py · test_workflow.py · test_launch_memory_cap.py · test_rotate_term_grace.py, and the -k full-collection repro above. Every pytest under `timeout 600`, --basetemp under /tmp.

## FILE SCOPE
extensions/agi/tests/conftest.py · extensions/agi/tests/test_conftest_guard.py. Never workflow.py, never test_tier_gate.py (the second exec is its own subject; the fence must survive it).

## CEILING
1 kid · <= 12 production lines · pi parents (tier-0) · 0 USD. Never a pytest that can re-collect its own dir from inside a test; a subprocess pytest runs under `timeout` + a process cap; kids never launch real claude.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
evidence_runs linked: the two proved kid experiments of DH.424 and DH.431 (a00-585205f4, a00-648ac510) are parented here but were never listed, so the grid-commit gate read evidence_runs=0 and demoted the hand-set proved to lean_proved:50. The verdict stands on those two runs; the missing link was the defect, not the evidence.
<!-- THOUGHT:END -->
