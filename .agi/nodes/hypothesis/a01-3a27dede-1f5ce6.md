---
id: hypothesis:a01-3a27dede-1f5ce6
mint_id: cc217f038c3b4279a30102da2aabc290
type: hypothesis
parents:
  - goal:g1.11
next_edges: []
scaffold_hash: 881987ac95eea42e
title: "TTL-enforced expiry: a minted key stops authenticating after expires_at passes — the crash-safety TTL guarantee is real, not aspirational"
confidence: 0.0
testable_claim: "A key minted with expires_at set to T minutes ahead authenticates a live API call within its lifetime, but fails with a 401/403 after the TTL expires. This proves the third independent limit is load-bearing and satisfies the falsifier's 'within one reclamation interval' even when no sweep or reaper runs."
verdict: pending
scaffold_hash: 881987ac95eea42e
---

# hypothesis:a01-3a27dede-1f5ce6

## Hypothesis

`goal:g1.11` asserts three independent limits: a credit cap, a TTL, and
explicit revocation. The TTL is the one that guarantees crash safety when NO
process is running to sweep or reap — a director killed with SIGKILL, a
machine reboot, a lease file corrupted — and the falsifier's "zero live minted
keys within one reclamation interval" is satisfied by the TTL alone.

**That claim has been guarded but never tested.** `expires_in_seconds` was
found to be silently ignored by the API (returning a key with `expires_at:
null`). The guard works, but nobody has verified that a key with a correctly
set `expires_at` actually *stops authenticating* after expiry. A key that
lives past its declared TTL would make the crash safety guarantee
decorative — visible in the dashboard as an expiry timestamp that nothing
enforces.

### What would prove it

**Mint a key with a short TTL (3-5 minutes), verify it authenticates a call
within its lifetime, wait for expiry, then verify the same call returns 401/**
**403.** Each leg proven with a live API call — using the key to authenticate
`GET /api/v1/keys` against OpenRouter, which returns 200 within TTL and 401
after TTL.

Specifically:

1. **Baseline confirmation.** Mint a key with `ttl_minutes=5`. Immediately
   call `list_keys` authenticated with this minted key. Expect 200 and a valid
   response. This proves the key works at mint time.

2. **Within-TTL test.** Wait ~2 minutes (comfortably inside 5). Call
   `list_keys` with the same key. Expect 200. This proves the key is usable
   during its lifetime, not just at the instant of minting.

3. **Post-TTL test.** Wait until `expires_at + 1 minute`. Call `list_keys`
   with the same key. Expect 401 or 403 — the key has expired and is rejected.
   Verify the response body or status indicates authentication failure, not a
   network error or a different HTTP code.

4. **Control — a live key next to an expired one.** After the TTL key has
   expired, mint a *second* key with the provisioning key. Call `list_keys`
   with the *new* key. Expect 200. This proves the issue is the expired key,
   not the provisioning credential or the API endpoint.

5. **Cleanup.** Revoke both keys via the provisioning key. Verify zero
   engine-minted keys outstanding.

**Repeat 3 times total** to rule out API-side caching or clock skew artifacts.
A single run is vulnerable to: OpenRouter caching a valid auth response after
TTL; clock skew between the issuer and the authenticator; a grace period the
API silently applies (e.g. 30s past expiry) that would make the TTL a soft
rather than hard boundary.

### What would disprove it

- **The key authenticates fine after expiry.** The TTL is a display-only
  field in the dashboard: OpenRouter records it but does not enforce it.
  Keys would then outlive their declared TTL always, and crash safety would
  depend entirely on the sweep (which needs a director running) and the
  reaper (which needs a cron or a CLI invocation).
- **The key is dead before the TTL expires.** The API revokes keys
  aggressively or uses a shorter internal TTL. If a 5-minute key dies in 60
  seconds, the TTL is not the mechanism it appears to be.
- **The API has a grace period that invalidates the concept.** If keys work
  for 5x their TTL, then the TTL is not a hard limit and the claim "within
  one reclamation interval" is false in practice.
- **`list_keys` does not auth-check the calling key.** If the GET endpoint
  authenticates via the provisioning key or accepts any valid key, then a
  call authenticated with a minted key may succeed regardless of expiry.
  Alternative: call the OpenRouter models endpoint or completion endpoint with
  the expired key to verify auth rejection there instead.
- **A failed revocation after cleanup** would leave a residual key that
  counts against later runs. This is mitigated by the TTL (the leftover key
  expires on its own) but would still be a defect worth recording.

### Why this is not covered by existing hypotheses

`hypothesis:per-spawn-keys-cost-under-a-second` proved mint latency and the
credential path via a stub, but the stub used the key immediately — well
within the TTL — so it could not verify post-expiry behaviour.

`hypothesis:a01-3c5640a0-5c684c` (real agent dialogue) involves agents that
run for at most a few minutes, always within the 60-minute default TTL. The
TTL is not exercised.

`hypothesis:a00-0fe61f28-1d9581` and `hypothesis:a00-41b7df72-0ff6fe` test
the reaper path — the mechanism that acts on a *different* reclamation
timescale (within seconds of a crash, if the cron runs). They never wait for
a TTL to elapse.

**The TTL is the only one of the three independent limits whose real-world
enforcement is unverified.** The credit cap appears in the OpenRouter
response and the dashboard (confirmed in
experiment:mint-latency-and-a-live-spawn), but whether OpenRouter actually
*stops* spend at the cap is a billing question that takes days to verify.
The TTL is measurable in minutes.

### What makes this hard

- **Timing is critical.** A 3-minute TTL means the experiment takes ~8
  minutes per run (mint, wait 2min for within-TTL test, wait 4min for
  post-TTL test, cleanup). Three runs take ~25 minutes. A 60-minute TTL is
  infeasible.
- **Clock skew.** The mint code uses `datetime.datetime.now(timezone.utc)`
  and the API sets `expires_at` from that. If the local clock is ahead of
  OpenRouter's clock, the key appears to expire earlier than intended. If
  behind, the key outlives its declared TTL by the skew.
- **`list_keys` endpoint may enforce differently from the completion
  endpoint.** A key that fails to list keys may still authenticate a model
  completion. The strongest test would use a real model call, but that costs
  money and depends on a model being available. The experiment should note
  this scope limitation and test at least the auth boundary.

### Relation to the falsifier

`goal:g1.11`'s falsifier:

> Killing the director mid-run leaves **zero** live minted keys within one
> reclamation interval.

If the TTL does not actually expire keys, the falsifier's "within one
reclamation interval" shrinks to "within one reaper-interval-with-a-running-
cron" — which is not the same guarantee. The falsifier admits three
independent mechanisms; this hypothesis tests whether the cheapest one (no
process needed, no API call needed) actually works.



## Agent Notes
Filled scaffold: TTL-enforced expiry hypothesis. Claims the TTL actually terminates a minted key's auth capability after expires_at. Tests within-TTL auth (200) vs post-TTL auth (401/403) against live OpenRouter API. Unverified gap among 3 independent limits.
