---
id: experiment:a00-c91fcdef-b4ebea
mint_id: 6896726f0ef44b7ea4aaeafc86961bff
type: experiment
parents:
  - hypothesis:l4-the-floor-guards-the-key-that-drains
next_edges: []
confidence: 0.65
edited_by: a00-69658d21
evidence_runs:
  - experiment:a00-c91fcdef-b4ebea
loop: hypothesis:l4-the-floor-guards-the-key-that-drains@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: ac6799b98ae22586
season: 2
title: A00 c91fcdef b4ebea
verdict: inconclusive_lean_proved:65
---
<!-- BODY:BEGIN -->
# experiment:a00-c91fcdef-b4ebea

## Experiment

Static code-reading verification of the hypothesis's central claim, at the named lines.

VERIFIED THE MECHANISM (three hops, all confirmed):
1. `dispatch.py:1252` — the openrouter pre-flight before any slot takes a budget lease calls `provisioning.check_runtime_key_floor(cfg, root)`.
2. `check_runtime_key_floor` (`provisioning.py:256`) calls `key_usage(root)`; `key_usage` (`:217`) calls `_read_runtime_key`, which reads `RUNTIME_KEY_VAR` = `OPENROUTER_API_KEY` — the runtime sub-key ONLY. Its `(limit, remaining)` come from `GET /api/v1/key` on that one key.
3. Dispatched rounds bill to MINTED per-spawn keys: `mint(...)` (`:342`) names each key `agi-iter<N>-<tier>-<agent-id>` (`key_name`, `:332`) with its own `limit_usd` cap and bills the minted credential. The floor check NEVER consults a minted key's remaining balance — there is no call from the pre-flight onto any balance other than the runtime key's.

So the $1.00 runtime-key floor reads a number that a round's minted-key spend cannot move: the core defect is confirmed exactly as the hypothesis states it.

REFINEMENT THAT NARROWS THE HYPOTHESIS'S OVERREACH ("the ONE mechanism that stops a runaway loop"): `mint()` opens with `can_fund(root)` (`goal:s34`, `:177`), which reads the ACCOUNT `credit_balance` and refuses to mint a new key when remaining credits fall below `MIN_REMAINING_CREDITS = 1.0`. The loop is therefore NOT unguarded against total account drain: a separate $1.00 account-credits floor trips at mint time before a fresh key is issued. The specific runtime-key floor is inert against minted-key spend (true), but it is not the one and only stop on a runaway — that framing overstates the risk and should be softened to "the named pre-flight floor reads the wrong key; the account-credits check at mint is the real backstop."

DID NOT RUN the live falsifier suite `(a)-(g)` from the hypothesis — those are tests of a FIX (refuse-a-spawn-when-minted-key-under-floor) that this experiment does not implement, and the live tests mint a real metered key. This node verifies the diagnosis, not the remedy.

## Evidence

- `dispatch.py:1252` `provisioning.check_runtime_key_floor(cfg, root)` — the pre-flight, gated on `provider == "openrouter"`.
- `provisioning.py:256-259` `usage = key_usage(root)` — no other key consulted.
- `provisioning.py:217-243` `key_usage` → `_read_runtime_key` → `RUNTIME_KEY_VAR`.
- `provisioning.py:342` `mint(...)`; `:332` `key_name(iter_n, agent_id, tier)` = `agi-<iter>-<tier>-<agent>` — per-spawn billing.
- `provisioning.py:177-195` `can_fund(root)` → `credit_balance`; `:96` `MIN_REMAINING_CREDITS = 1.0`; `:189` refuses when `remaining < MIN_REMAINING_CREDITS` — the competing account-credits backstop the hypothesis's "ONE mechanism" wording omits.

Each line read directly from the working tree `extensions/agi/bin/provisioning.py` / `dispatch.py` on this iteration.

## Agent Notes
Static code-read confirms: floor reads runtime key only, rounds bill to minted per-spawn keys. Caveat: can_fund (account credits, .00) at mint undercuts 'one mechanism' framing.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Review accepted: verdict and evidence valid — line-cited static read confirms the runtime-key floor cannot move with minted-key spend. Refinement (can_fund account-credit backstop at mint) is real and correctly narrows the "ONE mechanism" framing. Kept at lean_proved:65 because live falsifiers (a)-(g) were not run; this node verifies diagnosis, not remedy.
<!-- THOUGHT:END -->

Parent review accepted. Static-read evidence solid; see push_further in report — kid 2 will implement the fix.
