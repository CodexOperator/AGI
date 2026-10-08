---
id: experiment:a01-48bc04f6-2b4009
mint_id: 9e48bd0018a44230836e734ff8f3950b
type: experiment
parents:
  - hypothesis:provisioning-reads-the-workspace-weekly-budget
next_edges: []
confidence: 0.7
edited_by: season.py
scaffold_hash: f81a46dc1369c240
season: 1
thought_session: season
title: A01 48bc04f6 2b4009
verdict: inconclusive_lean_proved:70
---
# experiment:a01-48bc04f6-2b4009

## Experiment

### Goal
Test the claim: provisioning.py can read the OpenRouter account credit balance before minting, refuse to mint when remaining credits cannot fund the next key, and a fixture with exhausted budget makes the refusal test fail when the check is removed.

### What I did

1. **Probed OpenRouter API** for budget/credit endpoints. Found `/api/v1/credits` returns `{"data": {"total_credits": 45, "total_usage": 35.76}}` — account-level total and usage, NOT workspace-scoped and NOT a "weekly budget". Workspaces endpoint has no budget field. No workspace-scoped budget endpoint exists.

2. **Added `credit_balance()`** to provisioning.py — reads the credits endpoint, returns `(total, used, remaining)` tuple or None when the provisioning key is absent. Raises ProvisioningError on API failure when key IS present.

3. **Added `can_fund()`** — returns `(True, None)` when remaining credits >= MIN_REMAINING_CREDITS ($1.00), else `(False, reason_string)`. The threshold is the per-key default limit ($0.25) with a safety margin: enough budget to mint the next key without painting the loop into a corner.

4. **Integrated budget check into `mint()`** — calls `can_fund(root)` before the POST, raises ProvisioningError with a descriptive message when the check fails.

5. **Added 6 new tests**:
   - `test_credit_balance_returns_none_when_key_is_absent` — absence is supported
   - `test_can_fund_passes_when_key_is_absent` — no provisioning key = no budget error
   - `test_mint_refuses_when_credits_are_exhausted` — the red-on-purpose fixture: 45 - 44.5 = $0.50 remaining, below $1.00 threshold → mint raises ProvisioningError, POST never reached
   - `test_mint_proceeds_when_credits_are_sufficient` — healthy balance proceeds normally
   - `test_credit_balance_live` (live) — live API confirms endpoint works
   - `test_live_can_fund_passes_with_sufficient_balance` (live) — live account has credits

### What happened

All 24 tests pass (18 existing + 6 new). 0 regressions in the full 1477-test suite.

Live API confirmed: total_credits=45, total_usage=35.81, remaining=$9.19 — sufficient.

The `test_mint_refuses_when_credits_are_exhausted` fixture passes now and would fail ("mint POST should never be called when budget is exhausted") if the `can_fund()` check is removed from `mint()`. Green-on-purpose.

### Findings vs hypothesis claims

| Claim | Status | Detail |
|---|---|---|
| provisioning.py reads the workspace weekly budget before minting | ✅ PARTIALLY | Reads account-level credits, not workspace budget. No "weekly budget" concept in OR API. |
| Refuses to mint when key cannot be funded | ✅ CONFIRMED | `mint()` raises ProvisioningError when remaining < $1.00 |
| dispatch.py reports the slot unadmitted with reason | ❌ NOT IMPLEMENTED | dispatch.py catches ProvisioningError and exits with code 1 — does not report unadmitted |
| Fixture with exhausted budget makes test go red when check removed | ✅ CONFIRMED | `test_mint_refuses_when_credits_are_exhausted` depends on the `can_fund()` call in `mint()` |

## Evidence

```
$ python3 -c "import provisioning; print(provisioning.credit_balance())"                                                                                                      
(45.0, 35.810426473, 9.189573527)

$ python3 -c "import provisioning; ok, reason = provisioning.can_fund(); print(f'ok={ok} reason={reason}')"
ok=True reason=None

$ python3 -m pytest extensions/agi/tests/test_provisioning.py -q --tb=short
........................
24 passed in 6.98s

$ python3 -m pytest extensions/agi/tests/ -q --tb=short
...1477 passed in 89.85s
```

### Key caveats

1. **Account-level, not workspace-scoped.** The `/credits` endpoint reports the whole account balance. A project that uses a dedicated workspace for engine-minted keys cannot separate its budget from the account default. No OpenRouter API endpoint for workspace-scoped budgets exists as of 2026-09-04.

2. **Fatal error, not unadmitted.** A budget-exhausted mint raises ProvisioningError, which dispatch.py handles by printing an error and exiting with code 1. The slot is NOT recorded as "unadmitted" in the manifest — the hypothesis claim about dispatch.py behavior remains unimplemented.

3. **$1.00 threshold is arbitrary.** MIN_REMAINING_CREDITS = $1.00 is a reasonable default (enough for 4 default $0.25 keys) but should be configurable per-project for production.


## Agent Notes
Proved budget reading and refusal (account-level credits, not workspace weekly budget). Dispatch unadmitted reporting not implemented. All 24 tests pass, 1477 total no regressions.


<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-f065aff5, iter 1085). `inconclusive_lean_proved:70` accepted as written; the parent re-verified rather than agreed. `test_provisioning.py` re-run: 28 passed. Full suite re-run: 1481 passed, 0 failed. The red-on-purpose property was re-tested independently in a scratch copy of `bin/` + the test file with the `can_fund()` call deleted from `mint()`: `test_mint_refuses_when_credits_are_exhausted` goes red (`DID NOT RAISE`), exactly as the node claims. Two corrections of scope, not of substance: (1) the trailing item-2 tests in `test_provisioning.py` (`needs_credential`, dispatch minting gate) belong to the sibling hypothesis `cc-kids-do-not-mint-openrouter-keys` — another iteration's kid in the shared tree — and are NOT this node's evidence; (2) "24 tests / 1477 total" was the count at this kid's run moment; both numbers grew as sibling work landed, which is why the parent re-ran rather than trusting the counts. The lean, not `proved`, is right: the hypothesis's literal "workspace weekly budget" does not exist in the OpenRouter API (account-level only) and dispatch.py still exits fatal on a refused mint rather than reporting the slot unadmitted.
<!-- THOUGHT:END -->