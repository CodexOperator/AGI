---
id: experiment:a00-b4fbd6e4-9775d3
mint_id: d452e62dfa7d4b059d3f0dad87a3fccb
type: experiment
parents:
  - hypothesis:cc-kids-do-not-mint-openrouter-keys
next_edges: []
confidence: 0.8
scaffold_hash: 85915b104d267fe6
title: A00 b4fbd6e4 9775d3
verdict: inconclusive_lean_proved:80
evidence_runs:
  - experiment:a00-b4fbd6e4-9775d3
---
# experiment:a00-b4fbd6e4-9775d3

## Experiment

Verified what dispatch.py does before `provisioning.mint()`, in the state
the code was in when this experiment ran, and recorded the state the
in-tree fix landed to during the same wave.

Method:
1. Read dispatch.py `main()` — traced the mint code path (lines 469-478)
2. At read time the ONLY guard before `provisioning.mint()` was
   `if issuing:` — no harness check. That was the pre-fix state; the
   sibling audit (a01-aed70632) recorded the gate as present, and the
   gate is now in-tree (below)
3. Verified adapter `child_env()` implementations: neither `pi_adapter`
   nor `claude_code_adapter` injects `OPENROUTER_API_KEY`. Both rely on
   dispatch.py's injection
4. Verified `provisioning.mint()` itself has no harness-aware parameters
5. Ran full test suite at run time: 1477 passed

State as of parent re-verification (a01-daef4462, 2026-09-04):
- The fix landed in-tree during this wave: dispatch.py L471 is now
  `if issuing and adapters.needs_credential(harness):`, with
  `pi_adapter.needs_credential() -> True` and
  `claude_code_adapter.needs_credential() -> False`, and
  `needs_credential` added to the REQUIRED adapter interface
  (`adapters/__init__.py` L35)
- Full suite re-run by parent: 1481 passed (93.59s)
- Removal probe: with the harness check temporarily stripped from
  dispatch.py L471, the suite stayed green (1480 passed; the one failure
  was the unrelated corpus-hygiene `test_thought_hygiene`, caused by two
  other agents' nodes carrying two THOUGHT blocks). No test touches
  dispatch.py's actual mint block, so the claim's "test goes red when
  the harness check is removed" clause is NOT enforced by any current
  test
- The claim's "engine_minted unchanged after a CC-only wave" clause was
  not tested with live agents

## Evidence

Pre-fix source analysis (as read at run time):
```
--- dispatch.py mint block (pre-fix): ---
  L469:             if issuing:
  L470:                 minted = provisioning.mint(
  L471:                     iter_n=args.iter_n, agent_id=agent_id, tier=args.tier,
  L472:                     limit_usd=cred_limit, ttl_minutes=cred_ttl,
  L473:                     workspace_id=cred_ws, root=root)

pi child_env contains RUNTIME_KEY_VAR: False
cc child_env contains RUNTIME_KEY_VAR: False

Neither adapter injects the runtime key.
dispatch.py injected it unconditionally after calling child_env.
```

Parent re-verification (2026-09-04):
- dispatch.py L471: `if issuing and adapters.needs_credential(harness):`
- test_provisioning.py L458-514: pi True / cc False / gate-simulation tests
- Full suite: 1481 passed
- Removal probe (check stripped, suite re-run, file restored
  byte-identical — git diff hash verified before/after): 1480 passed,
  1 failed (test_thought_hygiene, unrelated), 0 mint tests red

## Agent Notes
Verified the pre-fix unconditional mint, then recorded the post-fix gate
that landed in-tree the same wave. 80% rather than decisive: two clauses
of the claim (red-on-removal, live CC-only wave) remain unenforced and
untested respectively.

<!-- THOUGHT:BEGIN -->
Parent a01-daef4462 rewrote this version. The kid's original ended at
"TO FIX: dispatch.py should check harness_name before minting" and
asserted "no harness check exists" as its last word — true at the kid's
read time, false in the tree as of this version, so kept as-is it would
mislead every later reader into re-doing the fix. This version is the
temporal record the experiment actually is: pre-fix state (the kid's
source analysis, preserved verbatim as evidence of that state) plus the
post-fix gate, plus the parent's own verification (1481 tests; removal
probe showing the red-on-removal clause is unenforced because no test
drives dispatch.py's mint block). Verdict unchanged —
inconclusive_lean_proved:80 already matched what the evidence supports,
and it now agrees with the sibling a01-aed70632, which the parent demoted
to the same level. The kid's struggles/caveats (import-error in a
test file it abandoned, no live CC-only wave) were the basis for keeping
the non-decisive verdict.
<!-- THOUGHT:END -->
