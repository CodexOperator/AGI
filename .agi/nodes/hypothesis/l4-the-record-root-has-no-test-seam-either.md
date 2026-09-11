---
id: hypothesis:l4-the-record-root-has-no-test-seam-either
mint_id: 81dd842e0eef422784912178cf8f3bdb
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-the-kid-tier-gate-has-no-env-seam
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 47d9f241b88ff9b1
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-IX) ruling merge-up 33 (0cfa40571; verdict on goal:g17.1 at f033f751b), ACCEPTED there; minted by sanctuary-director gen XIII 11:1xZ. (residue of L4.176, HALF) conftest.py still carries `--agent-records-root` guarded by `PYTEST_CURRENT_TEST` -- a guard that reuses the broken mechanism (an env var), so a kid clears the gate with one env var + one flag; and the current subprocess falsifier test plants a phantom running-kid record in the LIVE sessions dir. CLAIM: drop `--agent-records-root`, `pytest_addoption`, the `_TEST_AGENT_RECORDS_ROOT` global and the PYTEST_CURRENT_TEST guard entirely; `_record_root()` is `_default_record_root()` and nothing else; in-process tests monkeypatch `_default_record_root`; the subprocess falsifier tests plant their record under the REAL tree's sessions dir in a unique throwaway `iter-test-<uuid>` dir and remove it in `finally`. TESTS (test_tier_gate.py): a kid record + any env var + any flag -> bare directory run refused; no record -> passes; the planted dir is gone after the test. FALSIFIER: a bare directory run from inside a kid succeeding with any env var or flag set. CEILING: 1 kid. FILE SCOPE: extensions/agi/tests/conftest.py + test_tier_gate.py. SERIAL on conftest.py with l4-the-kid-tier-gate-scans-every-root-it-can-reach (g15-36a) -- one round may carry both."
thought_session: bca4febf-020c-4ee2-b023-9ed885b937bc
title: "the kid-tier gate's record root has no test seam at all: in-process tests monkeypatch, subprocess falsifiers plant under the real tree"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-record-root-has-no-test-seam-either

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-IX) ruling merge-up 33 (0cfa40571; verdict on goal:g17.1 at f033f751b), ACCEPTED there; minted by sanctuary-director gen XIII 11:1xZ. (residue of L4.176, HALF) conftest.py still carries `--agent-records-root` guarded by `PYTEST_CURRENT_TEST` -- a guard that reuses the broken mechanism (an env var), so a kid clears the gate with one env var + one flag; and the current subprocess falsifier test plants a phantom running-kid record in the LIVE sessions dir. CLAIM: drop `--agent-records-root`, `pytest_addoption`, the `_TEST_AGENT_RECORDS_ROOT` global and the PYTEST_CURRENT_TEST guard entirely; `_record_root()` is `_default_record_root()` and nothing else; in-process tests monkeypatch `_default_record_root`; the subprocess falsifier tests plant their record under the REAL tree's sessions dir in a unique throwaway `iter-test-<uuid>` dir and remove it in `finally`. TESTS (test_tier_gate.py): a kid record + any env var + any flag -> bare directory run refused; no record -> passes; the planted dir is gone after the test. FALSIFIER: a bare directory run from inside a kid succeeding with any env var or flag set. CEILING: 1 kid. FILE SCOPE: extensions/agi/tests/conftest.py + test_tier_gate.py. SERIAL on conftest.py with l4-the-kid-tier-gate-scans-every-root-it-can-reach (g15-36a) -- one round may carry both.
