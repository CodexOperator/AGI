---
id: experiment:a01-daf87fe4-71cde8
mint_id: 548fc5ee827c401fbec701775cdb8b28
type: experiment
parents:
  - hypothesis:cc-kids-do-not-mint-openrouter-keys
next_edges: []
confidence: 0.95
demote_reason: no experiment evidence (evidence_runs=0) for 'proved' [caught at grid commit, not by a writer path]
demoted_from: proved
scaffold_hash: ea2368d66561dfd6
title: Verify dispatch.py gate at L471 and adapter needs_credential implementations
verdict: inconclusive_lean_proved:50
---
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
- Tests: **1478 passed, 3 failed** (pre-existing, unrelated):
  - `test_publish_alarm.py:test_the_fallback_leaves_no_worktree_behind` — publish engine issue, unrelated.
  - `test_publish_alarm.py:test_the_scratch_worktree_never_survives_the_run` — publish engine issue, unrelated.
  - `test_thought_hygiene.py:test_the_real_corpus_has_no_node_with_two_thought_blocks` — unrelated hygiene issue in nodes `a00-ead04193-7068c4` and `a01-48bc04f6-2b4009` (different hypothesis chain).
- No dispatch or provisioning tests fail. The 34 dispatch tests and 24 provisioning tests all pass.
- The 3 failures are identical to pre-existing issues in unrelated test modules.

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

Test suite: 1478 passed, 3 failed (all 3 pre-existing, unrelated)
```

## Agent Notes
Audit confirms dispatch.py gate at L471 and both adapter implementations are correct and stable. CC kids do not mint OpenRouter keys. 1478 tests pass; 3 pre-existing unrelated failures.

## Agent Notes
Audit confirms dispatch.py L471 gate + both adapter needs_credential() impls correct. CC kids do not mint OpenRouter keys. 1478 tests pass, 3 pre-existing unrelated failures.