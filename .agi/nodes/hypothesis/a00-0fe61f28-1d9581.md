---
id: hypothesis:a00-0fe61f28-1d9581
mint_id: 394e4435bd134230824d55b90290c041
type: hypothesis
parents:
  - goal:g1.11
next_edges: []
confidence: 0.0
edited_by: director
scaffold_hash: 97d95eb295e9f524
testable_claim: reap_orphans and `provisioning.py reap --yes` find engine-minted keys (agi- prefix, scoped to the configured workspace) with no live lease, revoke exactly those, and leave every other key alone -- including the owner long-lived `agi` key
thought_session: L1.02
title: "The reaper survives a mid-run crash: orphaned minted keys are revoked, every other key is untouched"
verdict: pending
---
# hypothesis:a00-0fe61f28-1d9581

## Hypothesis

**`reap_orphans` correctly identifies and revokes orphaned engine-minted keys even after a simulated crash (director killed mid-run), without ever touching non-engine keys or the owner's long-lived key.**

### Testable claim

The `provisioning.reap_orphans()` function and `provisioning.py reap --yes` CLI both correctly find engine-minted keys (`agi-*` prefix, scoped to the configured workspace) that have no live lease, revoke them, and leave every other key alone — including the owner's long-lived `agi` key. This is the crash-safe cleanup path that `goal:g1.11` requires: "Killing the director mid-run leaves **zero** live minted keys within one reclamation interval."

### What would prove it

- `reap_orphans` with `dry_run=True` reports exactly the orphaned engine keys with no false positives (no hand-made keys, no live-lease keys).
- Running the same with `dry_run=False` actually revokes them, verified by a subsequent `list_keys` call — the count of engine-minted keys drops to zero without affecting the owner's key.
- After a simulated crash (no clean `release()`, keys orphaned by design), running `reap_orphans` returns those keys, while a key attached to a live lease is held.
- Workspace scoping works: when `workspace_id` is set, keys in a different workspace are skipped even if they match the name prefix.

### What would disprove it

- A false positive: the reaper revokes a key that does not belong to an engine mint (the owner's `agi` key, or any key without the `agi-` prefix).
- A false negative: an orphaned engine-minted key survives the reap pass.
- `reap_orphans` raises or blocks when the provisioning key is absent (it must return an empty list).
- A live-lease key is mistakenly reaped because the lease check fails.

### Why this matters beyond the existing experiment

The existing `experiment:mint-latency-and-a-live-spawn` proved the happy-path cleanup works (one spawn, clean exit, revocation via `release()` and the sweep's `_revoke_all`). But the goal's falsifier specifies mid-run crash survival, which exercises a **different code path**: `reap_orphans` reading the whole key list from the API, cross-referencing against live leases, and revoking whatever does not match. The existing experiment never called `reap_orphans` at all — the single test key was revoked directly by hash.

Reaping is the backstop for every mechanism that can fail: a director killed with SIGKILL, a machine reboot, a lease file that hits a corrupt write. The TTL and credit cap bound the blast radius, but the reaper is what closes the gap within the reclamation interval.

### The workspace dual-filter, which is the design's novelty

`goal:g1.11` settled on two independent filters for `reap_orphans` (2026-09-03, after the near miss with `agi` vs `agi-`): the name prefix `agi-` AND the declared workspace. The workspace filter is more structural than the string prefix — a hand-made key in a different workspace is isolated even if its name happened to collide. This hypothesis tests that isolation.