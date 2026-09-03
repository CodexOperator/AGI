---
id: hypothesis:a00-41b7df72-0ff6fe
mint_id: da02acb86ad24d349380d9acc16b8a6d
type: hypothesis
parents:
  - goal:g1.11
next_edges: []
confidence: 0.0
scaffold_hash: 33326248c907bea3
testable_claim: "Given N agents spawned with per-spawn keys, where N > 1 and the agents have overlapping lifetimes, `reap_orphans` called mid-state (some agents alive, some dead) returns a list that:"
title: "The reaper handles interleaved lifecycle: concurrent agents with overlapping lifetimes produce no false positives or missed orphans"
verdict: pending
---
# hypothesis:a00-41b7df72-0ff6fe

## Hypothesis

`experiment:mint-latency-and-a-live-spawn` proved single-agent credential
pathology: mint, inject, revoke, scrub. **One agent, one key, clean exit.**
The reaper was never exercised — the sweep's `_revoke_all` caught the single
key before `reap_orphans` even ran.

`hypothesis:a00-0fe61f28-1d9581` tests the reaper's dual-filter (name prefix +
workspace) against a static set of orphaned key records. That validates the
predicate logic but does not test the reaper against the real concurrent
lifecycle the falsifier describes: **agents started at different times, with
overlapping lease lifetimes, where some finish naturally and some crash,
leaving a mixed population of live and orphaned keys that the reaper must
disentangle.**

`goal:g1.11`'s falsifier says: "Killing the director mid-run leaves **zero**
live minted keys within one reclamation interval." That interval is the
earliest of three mechanisms: the TTL expiry, the sweep-reclaim path
(`_revoke_all`), and the reaper (`reap_orphans`). The falsifier is *only*
satisfied if each mechanism independently guarantees the invariant — which for
the reaper means: given two agents A (alive) and B (dead/orphaned) with
concurrent leases, `reap_orphans` revokes B's key but keeps A's. A and B have
overlapping lease windows, so the reaper cannot simply assume "lease present =
live, lease absent = orphaned" without correct cross-referencing against the
live-lease set.

### Testable claim

Given N agents spawned with per-spawn keys, where N > 1 and the agents have
overlapping lifetimes, `reap_orphans` called mid-state (some agents alive,
some dead) returns a list that:

1. Contains every orphaned engine-minted key (no false negatives)
2. Never contains any key belonging to a still-live agent (no false positives)
3. Does not revoke any non-engine key (no collateral damage)
4. After the last agent dies and the sweep has run, subsequent `reap_orphans`
   finds zero orphaned engine-minted keys (the fast path and the reaper agree)

This is the falsifier's "zero live minted keys" claimed satisfied by the
reaper mechanism — distinct from the TTL (which acts on a 60-minute clock) and
from the sweep path (which runs at each agent exit). The falsifier does not
state which mechanism does the work; it only requires that at least one does.
Proving the reaper works under concurrency proves the falsifier holds even
when the other two mechanisms are delayed or absent.

### What would prove it

**Setup.** Create two leases via `spawn_budget`: agent A (alive, PID running)
and agent B (dead, PID exited). Mint one key per agent via `provisioning.mint`.
The leases carry each key's hash. Agent B's lease file is left in place (it
was never reclaimed), but its holder PID is not running.

**Step 1 — mixed state, reaper with live set.** Call `reap_orphans` with
`live_hashes={A.hash}` and `dry_run=False`. Expected: exactly B's key is
revoked, A's key is untouched. Verified by `list_keys` (or `list_all_keys`).

**Step 2 — after sweep.** Clean up both leases (simulate agent exit). Call
`reap_orphans` again. Expected: zero keys found (both were already caught —
A by the sweep's `_revoke_all`, B by step 1).

**Step 3 — all live.** Start with two live leases. Call `reap_orphans` with
`live_hashes={A.hash, B.hash}`. Expected: zero keys revoked. No false
positives on live keys.

**Step 4 — no leasing, with non-engine key in account.** Create a hand-made
key (via the dashboard or CLI) whose name does NOT start with `agi-`. Call
`reap_orphans` with an empty `live_hashes`. Expected: the reaper finds and
revokes engine-minted keys only. The hand-made key is untouched.

**Repetition.** Each step at least 3 times against the live API to rule out
transient failures or timing artifacts.

### What would disprove it

- Step 1: A's key is revoked (false positive from concurrent lease configuration).
  Possible failure mode: the reaper's key_hash matching against `live_hashes`
  is string-sensitive and something about the hash returned by `mint()` and the
  hash stored on the lease differs in encoding or prefix.
- Step 1: B's key survives (false negative from `list_all_keys` blind spot).
  Possible failure mode: B's key was minted into a workspace that `list_keys`
  or `list_all_keys` cannot see, so the reaper's listing returns empty.
- Step 3: a live key is revoked. The reaper considers a live lease "inactive"
  because the PID check found it dead.
- Step 4: the hand-made key is revoked (reaper's name prefix check is too
  broad, e.g. `startswith("agi")` instead of `startswith("agi-")`).

### Why this is not covered by the existing hypotheses

`hypothesis:a00-0fe61f28-1d9581` tests the reaper's **predicate logic** (name
prefix matching, workspace filtering) but does not test it against a live,
concurrent lifecycle. The difference is the same as testing a filter function
with static data vs. running the filter against a live API's mutation history
where keys appear and disappear on someone else's clock.

`hypothesis:a01-3c5640a0-5c684c` tests **one** real agent's dialogue but says
nothing about concurrent agents with different lifetimes — it explicitly scopes
"Scalability beyond one agent" out.

`experiment:mint-latency-and-a-live-spawn` never called `reap_orphans` at all:
the single key was revoked by the sweep's `_revoke_all` path, and the reaper
is a separate code path designed for the scenario the sweep misses.

**This hypothesis tests the falsifier's claim about the reaper mechanism
specifically as it relates to the concurrent lifecycle `goal:g1.11`'s falsifier
describes.** The falsifier names a mid-run kill scenario — which is the exact
scenario where a single live agent exists alongside an orphaned one — and the
sweep path cannot help because the dead director never ran a sweep.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
This hypothesis exists because a gap opened where it did not. The three
existing hypotheses under `goal:g1.11` each test important claims, but their
coverage diagram had a quadrant: "concurrent + reaper" was empty. The
per-spawn latency experiment tested one agent only and never exercised the
reaper; the real-agent hypothesis tests one spawning at a time; the reaper
predicate hypothesis tests the logic statically. None tests what the falsifier
actually describes: a running system with live and dead agents under one
reaper invocation.

The key_hash cross-reference is the most likely failure point. The lease stores
a hash that must match what the API returns via `list_keys` — if those hashes
differ (encoding, casing, prefix), the reaper cannot distinguish live from
orphaned and either revokes everything or nothing. Both are fatal for the
falsifier.

Step 4 tests the isolation guarantee that is the entire reason the reaper
exists. A cleanup routine that revokes hand-made keys is worse than no cleanup
routine.
<!-- THOUGHT:END -->