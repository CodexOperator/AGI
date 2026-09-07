---
id: experiment:a00-95dbb99d-05ae18
mint_id: d938b5abd4b148088ee7b09f512a2913
type: experiment
parents:
  - hypothesis:cc-kids-do-not-mint-openrouter-keys
next_edges: []
confidence: 0.85
edited_by: season.py
scaffold_hash: 854b93714d9d3a2d
season: 1
thought_session: season
title: A00 95dbb99d 05ae18
verdict: inconclusive_lean_disproved:85
---
<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent a00-27ecc2b3 (iter 1088) review edit. The kid's audit was performed 15:13–15:20 against the pre-fix tree and concluded `disproved` at confidence 1.0; that was a true statement about the code at that moment, but the body stated it as standing state. At 15:20:42–15:21:24 — 40 seconds after the audit finished — a parallel wave landed the goal:s34 item 2 fix: `adapters.needs_credential()` becomes a REQUIRED adapter function (pi→True, claude-code→False) and dispatch.py's mint gate becomes `if issuing and adapters.needs_credential(harness)`. Parent re-verification (2026-09-04): gate present at the mint call site, adapters declare as the hypothesis predicts, new tests in test_provisioning.py pass, full suite 1481 passed, `provisioning.py status` now reports engine_minted. This version therefore scopes the kid's finding to its point in time and demotes disproved@1.0 to inconclusive_lean_disproved:85 — the audit's method was sound and its T1 result was accurate, but the hypothesis was not dead, it was 40 seconds from being true. Caveat carried forward: the new tests simulate the gate inline and never import dispatch.py, so they stay green if the check is deleted from dispatch.py; a source-level regression test is still owed (goal:s34 item 2).
<!-- THOUGHT:END -->

# experiment:a00-95dbb99d-05ae18

## Experiment

Audited the claim: "dispatch.py mints a provider credential only for harnesses whose adapter declares it needs one (pi does, claude-code does not)" — **as of 2026-09-04 15:13–15:20**, before the goal:s34 item 2 fix landed.

Method: read all minting-related code paths in `extensions/agi/bin/dispatch.py` and `extensions/agi/bin/adapters/*_adapter.py`. Searched for any harness/adapter check before the `provisioning.mint()` call.

Result at that moment: **claim false**. dispatch.py minted credentials for ALL agents unconditionally when `provisioning.available()` returned True. The only gate was `issuing = provisioning.available(root)` at line 307, which checks whether the provisioning key exists — it has nothing to do with the harness type. No `needs_credential` / `needs_key` / `requires_credential` existed on either adapter. Both harness types got identical minting treatment:

```
if issuing:
    minted = provisioning.mint(
        iter_n=args.iter_n, agent_id=agent_id, tier=args.tier,
        limit_usd=cred_limit, ttl_minutes=cred_ttl,
        workspace_id=cred_ws, root=root)
```

**Expected** (per hypothesis): claude-code agents should skip minting because they authenticate via Anthropic subscription, not OpenRouter. A CC kid handed an OpenRouter key wastes the key budget.

**Actual (at audit time)**: every agent — pi or claude-code — got a minted key when the provisioning key was available.

**Superseded standing state**: at 15:20:42–15:21:24 the goal:s34 item 2 fix landed in the tree (parallel wave). Post-fix, the claim holds: `adapters.needs_credential()` is REQUIRED on every adapter (pi→True, claude-code→False) and dispatch.py gates the mint on it. See the THOUGHT block for parent re-verification (suite 1481 passed, 2026-09-04).

## Evidence

- Code audit (T1): dispatch.py lines 301–330 showed unconditional minting inside the agent loop (no harness check); no `needs_key`, `should_mint`, or `requires_credential` on either adapter; `issuing` set once from `provisioning.available(root)` — key presence, not harness type
- The claude-code adapter's `child_env()` restores Anthropic credentials the base scrub removed, so a CC kid ran with both an Anthropic subscription and a minted OpenRouter key — doubly authenticated, wasteful
- Post-fix state verified by parent review at 15:25 (THOUGHT block), not by this run

## Agent Notes
Verified by code audit: dispatch.py unconditionally mints OpenRouter keys for ALL agents (both pi and claude-code) with no harness check. The claim that CC kids do not mint is false in the current code.