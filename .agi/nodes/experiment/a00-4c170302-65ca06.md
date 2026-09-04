---
id: experiment:a00-4c170302-65ca06
mint_id: 0f1a57429c4e4edfbd2f6c7b8ce4f975
type: experiment
parents:
  - hypothesis:cc-kids-do-not-mint-openrouter-keys
next_edges: []
confidence: 0.95
scaffold_hash: fd75f10b223f5e6a
title: A00 4c170302 65ca06
verdict: proved
<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent a00-27ecc2b3 (iter 1088) review edit. Verdict stands: the code-state claims were all verified correct by parent re-read (gate at dispatch.py L471, pi→True, claude-code→False, REQUIRED on the adapter interface, live provisioning status). Two corrections. (1) The kid's strongest-sounding line — that test_removing_the_harness_check_restores_unconditional_minting "explicitly proves removing the gate" — overclaims: that test re-implements the gate loop inline and never imports dispatch.py, so deleting the check from dispatch.py leaves all four tests green. What IS pinned is the adapter declarations (tests 1–2) and the gate logic in isolation; a source-level regression test on dispatch.py is still owed under goal:s34 item 2. (2) Suite numbers were a point-in-time reading in a live, concurrently-edited tree: the one cited failure (test_thought_hygiene) was transient churn, and the parent re-ran the full suite at 15:3x — 1482 passed, 0 failed. Both corrections are noted where the claims appear; nothing about the gate itself was wrong.
<!-- THOUGHT:END -->
---
# experiment:a00-4c170302-65ca06

## Experiment

Verified the fix for `goal:s34` item 2 is in place and load-bearing: dispatch.py mints provider credentials only for harnesses whose adapter declares `needs_credential()` (pi=yes, CC=no).

**Method:**

1. Read `dispatch.py` mint gate (L471): `if issuing and adapters.needs_credential(harness):`
2. Verified both adapters declare `needs_credential()` in the REQUIRED interface (`adapters/__init__.py` L35)
3. Checked pi_adapter: returns True (uses minted OpenRouter key)
4. Checked claude_code_adapter: returns False (auths via on-disk credential store, not a minted key)
5. Ran the 4 dedicated tests: `test_pi_harness_needs_a_credential`, `test_claude_code_harness_does_not_need_a_credential`, `test_dispatch_mints_only_for_harnesses_that_need_it`, `test_removing_the_harness_check_restores_unconditional_minting`
6. Ran full repo test suite (1481 collected)
7. Checked `provisioning.py status` shows 16 keys visible, 15 engine_minted — all from active agents

**Results:**
- All 4 dedicated tests PASS in 0.08s
- Full test suite at run time: 1480 passed, 1 failed (`test_the_real_corpus_has_no_node_with_two_thought_blocks`) — transient: concurrent agents were editing nodes mid-run. Parent re-run at 15:3x: 1482 passed, 0 failed.
- `needs_credential({"adapter": "pi"})` → True
- `needs_credential({"adapter": "claude_code"})` → False
- `test_removing_the_harness_check_restores_unconditional_minting` demonstrates the gate logic in isolation (with-check → only pi mints; without → both). **Limitation (parent review):** it simulates the gate loop inline and never imports dispatch.py, so deleting the check from dispatch.py itself would keep all four tests green. What the suite pins is the adapter declarations and the gate logic, not their wiring in dispatch.py — a source-level regression test is still owed (goal:s34 item 2).
- Provisioning status: `keys_visible=16 engine_minted=15` — no gratuitous minting for CC kids

**Conclusion:** Hypothesis proved. The fix is in place, the gate is load-bearing in dispatch.py, and the adapter declarations are test-pinned. (Parent review: the red-on-removal coverage does not yet extend to dispatch.py's source — see the limitation above.)

## Evidence

```
dispatch.py L471:            if issuing and adapters.needs_credential(harness):

adapters/__init__.py L35:  REQUIRED = (..., "needs_credential")
adapters/__init__.py L156: def needs_credential(harness: dict) -> bool:

pi_adapter.py L210: def needs_credential(harness: dict) -> bool:
                   return True

claude_code_adapter.py L186: def needs_credential(harness: dict) -> bool:
                            return False

--- 4 dedicated tests ---
test_pi_harness_needs_a_credential .............. PASSED
test_claude_code_harness_does_not_need_a_credential PASSED
test_dispatch_mints_only_for_harnesses_that_need_it PASSED
test_removing_the_harness_check_restores_unconditional_minting PASSED

--- full test suite ---
1480 passed, 1 failed at run time (test_thought_hygiene.py — transient concurrent-edit churn; parent re-run: 1482 passed, 0 failed)

--- provisioning status ---
provisioning: available  keys_visible=16  engine_minted=15
```




## Agent Notes
Verified fix in place: dispatch.py L471 gates minting on adapters.needs_credential(harness). pi=needs_key, CC=skip. 4 dedicated tests + 1480/1481 full suite pass. Provisioning status shows no gratuitous minting.
