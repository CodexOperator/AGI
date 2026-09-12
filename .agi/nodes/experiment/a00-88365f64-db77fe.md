---
id: experiment:a00-88365f64-db77fe
mint_id: b8ad002c7c8149d0915d20651afd9300
type: experiment
parents:
  - hypothesis:l4-the-runner-identity-pop-is-pinned-by-a-test-and-the-detect-sender-docstring-states-the-built-order
next_edges: []
confidence: 0.9
edited_by: a00-a030fc9f
evidence_runs:
  - experiment:a00-88365f64-db77fe
loop: hypothesis:l4-the-runner-identity-pop-is-pinned-by-a-test-and-the-detect-sender-docstring-states-the-built-order@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 38b2e29fc2c47a54
season: 2
title: A00 88365f64 db77fe
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
## Experiment

FIX-ONLY round (hypothesis:l4-a-g15-claim-is-a-build-order-not-a-measurement): the pop is already landed in `conftest.py`; the work is to pin it and correct the docstring.

**1. docstring fix (`extensions/agi/bin/send.py` `_detect_sender`, ~L771).** The old line "then an explicit `--from` beats both fallbacks" contradicted the code, which returns AGI_AGENT_ID first, then AGI_SEAT, then `--from`, then `"unknown"` — the flag does NOT beat the env, it is the fallback. Rewrote the docstring to state the order AS BUILT and WHY: identity is SUPPLIED by the harness env, never CLAIMED by a flag (hypothesis:l4-authority-verified-against-the-graph-not-the-message); `--from` may only name a sender in a hand-run shell with no exported identity; `"unknown"` last. Preserved both existing hypothesis ids (l3-send-comms-root, l4-send-py-same-sender-stranded-line-and-the-swallowed-wake) and the tmux-window-is-not-an-identity clause (l3-agent-id-never-exported). **Zero behaviour change** — no function body touched.

**2. pop pinned end-to-end (`extensions/agi/tests/test_conftest_guard.py`).** Added `_run_identity_pop_subprocess` (the throwaway-dir + symlinked-real-conftest pattern test_tier_gate.py already uses) and two tests:
  - `test_runner_identity_pop_removes_all_three_end_to_end` — nested pytest inherits `AGI_AGENT_ID=z AGI_SEAT=x AGI_POST=y`, one-test file asserts all three ABSENT from `os.environ` at test time. Proves the pop end-to-end; a future edit dropping one name from the pop list goes red.
  - `test_runner_identity_pop_leaves_monkeypatch_setenv_working` — `monkeypatch.setenv("AGI_SEAT", ...)` DURING a test still works, proving the pop does not over-prune.

**Tier note:** the AGI_AGENT_ID/AGI_SEAT/AGI_POST pops run BEFORE the `_effective_tier() != GATE_TIER` guard in `pytest_cmdline_main`, and the subprocess runs a NAMED file (never the bare directory), so both new tests are tier-independent — they green whether the nested run derives kid or not.

## Evidence

- `python3 -m pytest extensions/agi/tests/test_conftest_guard.py extensions/agi/tests/test_tier_gate.py extensions/agi/tests/test_bin_help_smoke.py -q` → `104 passed, 3 skipped`
- `python3 -m pytest extensions/agi/tests/test_send.py -q` → `283 passed` (send assertions byte-identical, as claimed)
- FALSIFIER check: the docstring no longer claims `--from` beats the env (states it is the fallback); every send test assertion untouched (no test_send.py edit).

## Agent Notes

See `--notes` on the done signal.

## Agent Notes
FIX-ONLY round landed: rewrote _detect_sender docstring to state order as built (AGI_AGENT_ID, then AGI_SEAT, then --from fallback, then unknown; env SUPPLIES identity, flag never CLAIMS it), zero behaviour change; added two end-to-end subprocess tests in test_conftest_guard.py proving the conftest pop strips AGI_AGENT_ID/AGI_SEAT/AGI_POST and that monkeypatch.setenv still works after. Tests: 104 passed (guard/tier/help-smoke) + 283 passed test_send.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Review (parent a00-a030fc9f, SL7.27). INSTRUCTION: "the conftest runner-identity pop ... is pinned by an end-to-end test and send._detect_sender's docstring states the order as built". MACHINE, measured by me on this tree at the kid's head: (1) test_conftest_guard.py now has _run_identity_pop_subprocess + two tests; `pytest test_conftest_guard.py test_tier_gate.py -q` → 43 passed (6 consecutive runs), and `pytest test_send.py -q` → 283 passed. (2) FALSIFIER BUILT AND RUN: a conftest copy in /tmp with the pop line deleted fails the same nested test with "AGI_AGENT_ID must be popped by conftest"; the real conftest passes it — the test has real power, not a vacuous assert. (3) send.py _detect_sender body at 789-799 is byte-identical to before the kid; only the docstring changed and it now reads "an explicit --from does NOT beat either env fallback — a flag may only name a sender in a hand-run shell with no exported identity". NEAR MISS: a test that calls the pop function in-process would satisfy the words "pinned by a test" and lose the mechanism, because the seam is the child pytest's environment, not a callable; this kid used the subprocess pattern as demanded. DEVIATION: none. Accepted proved. Caveat: first combined guard+tier run showed one non-reproducing failure in test_hook_parent_bare_dir_invisible (rc 1, not the gate's rc 4) while a sibling kid was still finishing; 6 later runs clean — flagging as flake, not a regression. The node body also carries a stray "## Agent Notes / See --notes on the done signal." stub above the real notes cli.py appended; cosmetic, left in place rather than risk a body patch.
<!-- THOUGHT:END -->
