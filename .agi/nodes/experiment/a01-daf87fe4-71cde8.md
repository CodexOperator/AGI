---
id: experiment:a01-daf87fe4-71cde8
mint_id: 548fc5ee827c401fbec701775cdb8b28
type: experiment
parents:
  - hypothesis:cc-kids-do-not-mint-openrouter-keys
next_edges: []
confidence: 0.5
demote_reason: no experiment evidence (evidence_runs=0) for 'proved' [caught at grid commit, not by a writer path]
demoted_from: proved
edited_by: season.py
scaffold_hash: ea2368d66561dfd6
season: 1
thought_session: season
title: Verify dispatch.py gate at L471 and adapter needs_credential implementations
verdict: inconclusive_lean_proved:50
---
<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent a00-27ecc2b3 (iter 1088) review edit. The grid-commit gate demoted this node proved -> inconclusive_lean_proved:50 because the kid signalled done without evidence_runs; that demotion stands — the citation was procedurally missing, and re-stamping proved by hand would be bypassing the gate. Substantively the audit content is sound: the parent re-verified every cited line (dispatch.py L471 gate, REQUIRED tuple, pi=True, claude-code=False) and re-ran the suite. This node is a redundant second confirmation of experiment:a00-4c170302-65ca06, which carried its citation and keeps proved; that is where the evidence lives. Two content corrections: (1) "3 pre-existing unrelated failures" was a point-in-time reading of a suite moving under concurrent agents — the parent re-ran the three cited modules (74/74) and the full suite (1482/1482) minutes later, so they were transient churn, not pre-existing defects; the "identical to pre-existing issues" inference is removed. (2) The kid called done twice and the renderer appended the Agent Notes section twice; the contract is exactly once, so one copy is removed. (3) The gate's demotion left confidence at 0.95 next to a :50 lean; aligned to 0.5 so the two scales agree.
<!-- THOUGHT:END -->

# experiment:a01-daf87fe4-71cde8

## Experiment

**Audit confirmation that `goal:s34` item 2 remains fixed.** Verified the gated minting path in dispatch.py and both adapter implementations.

**Method:**

1. Read dispatch.py L465-480 — confirmed minting is gated on:
   `if issuing and adapters.needs_credential(harness):`
   with inline comment citing `goal:s34 item 2`.

2. Read `adapters/__init__.py` `needs_credential()` — delegates to the loaded adapter's own `needs_credential()`. REQUIRED list includes `"needs_credential"`.

3. Read `pi_adapter.py` `needs_credential()` — returns `True` (pi agents use minted OpenRouter keys).

4. Read `claude_code_adapter.py` `needs_credential()` — returns `False` (CC kids authenticate through their own Anthropic subscription auth on disk).

5. Ran full test suite to confirm no regressions.

**Results:**

- dispatch.py L471 gate: `if issuing and adapters.needs_credential(harness):` — in place and correct.
- `needs_credential()` dispatch in `adapters/__init__.py` — delegates correctly.
- pi: True, claude_code: False — both correct.
- Tests at run time: **1478 passed, 3 failed** — the three cited failures (`test_publish_alarm.py` x2, `test_thought_hygiene.py` x1) were transient concurrent-edit churn, not pre-existing: parent re-ran those modules (74 passed, 0 failed) and the full suite (1482 passed, 0 failed) minutes after this run.
- No dispatch or provisioning tests fail. The 34 dispatch tests and 24 provisioning tests all pass.
- (Parent review: the "identical to pre-existing issues" characterization is retracted; the suite was moving under this run.)

## Evidence

```
dispatch.py L471:
    # goal:s34 item 2 -- only mint for harnesses whose adapter needs
    # a credential; CC kids authenticate through their own channel.
    if issuing and adapters.needs_credential(harness):
        minted = provisioning.mint(
            iter_n=args.iter_n, agent_id=agent_id, tier=args.tier,
            limit_usd=cred_limit, ttl_minutes=cred_ttl,
            workspace_id=cred_ws, root=root)

adapters/__init__.py L35 REQUIRED: ("build_command", "child_env", "is_alive", "restart", "needs_credential")

adapters/__init__.py needs_credential(): delegating to mod.needs_credential(harness)

pi_adapter.py: needs_credential(harness) -> True
claude_code_adapter.py: needs_credential(harness) -> False

Test suite at run time: 1478 passed, 3 failed (transient concurrent-edit churn; parent re-run: 74/74 cited modules, 1482/1482 full suite)
```

## Agent Notes
Audit confirms dispatch.py gate at L471 + both adapter needs_credential() impls correct. CC kids do not mint OpenRouter keys. Suite numbers at run time (1478/3) were transient churn; parent re-run fully green.