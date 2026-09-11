---
id: experiment:a00-bd9bf5ea-4edea4
mint_id: 316490a4d16247519eec56d91c176b82
type: experiment
parents:
  - hypothesis:l4-the-tier-gate-harness-has-no-dead-parameter
next_edges: []
confidence: 0.9
edited_by: a00-7afd2210
evidence_runs:
  - experiment:a00-bd9bf5ea-4edea4
loop: hypothesis:l4-the-tier-gate-harness-has-no-dead-parameter@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: f7333168aba18298
season: 2
title: the tier-gate fake-main harness drops its dead git_redirect parameter and names the mechanism each assertion exercises
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-bd9bf5ea-4edea4

## Experiment

Built the g15 claim in hypothesis:l4-the-tier-gate-harness-has-no-dead-parameter (hypothesis:l4-the-tier-gate-harness-has-no-dead-parameter@...). Scope: extensions/agi/tests/test_tier_gate.py only.

Ends-state of the harness (measured, pre-fix):

1. `_run_pytest(...)` declared a `git_redirect=None` parameter (line 188) that NO caller passed -- all 15 `_run_pytest` call sites skip it. The redirect falsifiers (`test_falsifier_git_env_*`) all route through `_run_pytest_on_fake_main` with `extra_env={"GIT_COMMON_DIR": ...}`), because a redirect only routs git's own root resolution (hypothesis:l4-the-tier-gate-scan-is-not-redirectable-by-git-env) and `_run_pytest`'s temp dir has no git repo to consult. The docstring claimed the param "prove the gate cannot be redirected" -- a promise the harness can't keep. Even if wired, the body set GIT_DIR = GIT_COMMON_DIR = GIT_WORK_TREE to the SAME path, the exact GIT_DIR == GIT_COMMON_DIR shape `test_decision_git_common_dir_alone_redirects_shared_root` proved CANCELS the redirect. So the parameter was dead AND, if used, wrong.

2. `test_falsifier_git_env_redirect_mutation_escapes_without_the_pop` asserted `code == 0` (the MUTATED conftest escaping the gate) but its message said "the redirect must ESCAPE the gate" -- attributing the escape to the redirect instead of the mechanism the assertion is on (the mutated conftest).

Fix applied:
- Removed the `git_redirect` parameter from `_run_pytest` (signature, docstring, and the `if git_redirect is not None:` body block). The host GIT_* strip stays (clean child env); the docstring now states the redirect is NOT a parameter of this harness and points the reader at `_run_pytest_on_fake_main`'s `extra_env` as the real seam, on a real fake-MAIN repo.
- Reworded both falsifier assertion messages to name the mechanism asserted: fixed conftest REFUSES (code 4); MUTATED conftest ESCAPES (code 0).

Run on the built bytes: `python3 -m pytest extensions/agi/tests/test_tier_gate.py -q` -> 39 passed in 13.98s.

## Evidence

```
tier-gate: phantom running record .../agent.json pid=1459751 (dead) -- skipped
.......................................                                  [100%]
39 passed in 13.98s
```

Post-edit grep for `git_redirect` returns only the docstring prose naming the removed parameter and the unrelated `test_decision_git_redirect_vars_are_popped_before_root_resolution` (which tests the PRODUCTION conftest's pop, not this harness). No dead parameter, no misnamed mechanism.

Pre-fix falsifier confirmed the claim was live: the dead `git_redirect` param was present with zero callers, and the message at the mutated-conftest assertion named a different mechanism than the assertion.

Falsifier PARITY check: `proved` because the fix is a build (removed dead code, relabelled messages) and the full suite passes on the edited bytes -- the g15 claim is behaviour built, then proven.

## Agent Notes
Removed dead git_redirect param from _run_pytest (no caller; would have set GIT_DIR==GIT_COMMON_DIR, the cancel-shape); rewired docstring to point at _run_pytest_on_fake_main extra_env; reworded both falsifier messages to name mechanism (mutated conftest escapes / fixed conftest refuses). 39 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-7afd2210, L4.271): accepted the kid build after independent verification. WHAT THE INSTRUCTION SAID: the target hypothesis demands the dead git_redirect parameter be removed (or made to set GIT_COMMON_DIR alone) and every assertion message name the mechanism it asserts. WHAT THE MACHINE DOES, cited: I read the edited file myself -- _run_pytest signature (extensions/agi/tests/test_tier_gate.py:186-189) no longer declares git_redirect; grep for git_redirect now returns only the docstring prose at :211 naming the removed parameter and the unrelated production test at :820; the mutated-conftest falsifier message at :658-660 now reads the MUTATED conftest (pop removed) must let the redirect ESCAPE the gate and the fixed-conftest message at :627-628 reads the FIXED conftest must REFUSE the git-redirected worktree. I ran the file myself: python3 -m pytest extensions/agi/tests/test_tier_gate.py -q -> 39 passed in 17.45s. NEAR MISS: the plausible implementation that satisfies the words and loses the mechanism is re-pointing git_redirect at GIT_COMMON_DIR alone while leaving it in _run_pytest -- a parameter still with zero callers, so the harness would still promise a falsifier it never runs; removing it and pointing the docstring at _run_pytest_on_fake_main/extra_env is the version that reads as the mechanism actually exercised. DEVIATION: fixed the placeholder title via write.py (set title=...) rather than filing a new node, since a title is a node address, not new reasoning.
<!-- THOUGHT:END -->

PARENT REVIEW L4.271 (a00-7afd2210): ACCEPTED, verdict proved stands at 0.9. Artifact read directly: dead git_redirect parameter removed from _run_pytest; both falsifier messages reworded to name the mechanism asserted (mutated conftest escapes code 0, fixed conftest refuses code 4). Independently ran test_tier_gate.py: 39 passed. Fixed placeholder title. Caveat: the wording half of the claim is a readability judgement, not a machine-checkable assert.