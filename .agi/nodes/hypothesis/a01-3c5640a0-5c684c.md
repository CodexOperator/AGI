---
id: hypothesis:a01-3c5640a0-5c684c
mint_id: f3fd69e2ddf54a6f84d8d941a5c79b8a
type: hypothesis
parents:
  - goal:g1.11
next_edges: []
confidence: 0.0
edited_by: season.py
scaffold_hash: 34f0fb318b13290b
season: 1
testable_claim: "**Part A — provisioning key present.** A real pi agent dispatched through the engine with a provisioning key set authenticates against OpenRouter using the minted per-spawn key (injected as `OPENROUTER_API_KEY`), completes its assigned dialogue, and the key is revoked when the agent exits. The agent's environment contains no `OPENROUTER_PROVISIONING_KEY`. The run succeeds."
thought_session: season
title: A real pi agent completes a dialogue using a per-spawn OpenRouter key — the last untested falsifier clause
verdict: pending
---
# hypothesis:a01-3c5640a0-5c684c

## Hypothesis

`experiment:mint-latency-and-a-live-spawn` proved the credential *path* of `goal:g1.11` — mint, inject, revoke, scrub — but the child was a stub that dumped its environment and exited. **A real pi agent has not authenticated with a minted per-spawn key or completed its assigned dialogue.** That is the last untested clause of the falsifier.

This hypothesis tests two things in one pass: the provisioning-present case and the provisioning-absent fallback, because the two halves of the falsifier are the same spawn path with one environment variable flipped.

### Testable claim

**Part A — provisioning key present.** A real pi agent dispatched through the engine with a provisioning key set authenticates against OpenRouter using the minted per-spawn key (injected as `OPENROUTER_API_KEY`), completes its assigned dialogue, and the key is revoked when the agent exits. The agent's environment contains no `OPENROUTER_PROVISIONING_KEY`. The run succeeds.

**Part B — provisioning key absent.** The same dispatch, with `OPENROUTER_PROVISIONING_KEY` unset, falls back to the long-lived `OPENROUTER_API_KEY` that existed before the loop started. The agent completes the same dialogue. **No minting code runs, no crash, no hard dependency on the provisioning API.** The engine is not more fragile with the feature off than it was before the feature existed.

### What would prove it

- Part A: a spawned agent running a known dialogue (e.g. a single-turn `--prompt` call) authenticates and returns a valid completion. The agent's environment (captured at spawn, not read from a config list) contains `OPENROUTER_API_KEY` starting with `sk-or-v1-` (minted) and zero occurrences of `OPENROUTER_PROVISIONING_KEY`. After exit, the sweep reclaims the lease and the key count drops by one.
- Part B: the same dialogue completes without the provisioning key. The agent's environment contains the *original* long-lived `OPENROUTER_API_KEY` (not a minted one) and no `OPENROUTER_PROVISIONING_KEY`. The run produces the same outcome.
- Both paths verified at least 3 times each to rule out transient failures.

### What would disprove it

- Part A: the agent fails to authenticate, returns an auth error, or the key is leaked into the child's environment in the wrong position (e.g. a written credential that is never picked up by the pi process because of key-name priority).
- Part B: the engine errors out when `OPENROUTER_PROVISIONING_KEY` is absent, or the existing `OPENROUTER_API_KEY` is stripped by the scrub logic (which would mean the scrub is too aggressive and breaks the fallback).
- The revocation path drops the key before the agent finishes (premature revocation on a still-live lease).

### Why this is the last untested clause, not the same claim

The per-spawn verdict proved everything *except* that a real pi agent can use the credential. The experiment ran a stub to isolate the credential-management code from pi's own HTTP client, authentication flow, and model-call retry loop — and that isolation is the right way to debug the mint layer. But the falsifier demands a spawn that runs end to end; a verified credential path that goes no further than the environment dump is a path no agent has walked.

Part B is here because the falsifier's strongest clause is the one most likely to be dropped: "the loop still runs with no provisioning key." If the fallback is never verified, the feature cannot be deployed safely — because it would turn a hardening option into a hard requirement the first time the provisioning key is rotated or revoked upstream.

### What this does *not* test

- Spend attribution on the OpenRouter bill. The key name proves it; this would run short enough that nothing appears in the dashboard.
- Scalability beyond one agent. The per-spawn verdict already measured latency at `max_live` concurrency and found no rate limiting.
- All model providers. OpenRouter only, consistent with `goal:g1.11`'s explicit scope.
- Crash survival of revocation (already proved in the experiment — reclaim-by-liveness is tested, not trusted).