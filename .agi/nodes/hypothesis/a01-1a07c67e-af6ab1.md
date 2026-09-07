---
id: hypothesis:a01-1a07c67e-af6ab1
mint_id: 238059154b95437ea0a8171cbf427730
type: hypothesis
parents:
  - goal:g4.9
next_edges: []
confidence: 0.3
edited_by: season.py
scaffold_hash: 81ee024821460297
season: 1
testable_claim: "A hung-but-alive agent past manifest timeout_seconds holds its spawn_budget slot forever: `spawn_budget status` shows it live with no age or restart count, `_sweep_locked` reclaims only pid-dead leases, and the inline reaper never compares elapsed time against the timeout — so the G4.9 falsifier (hold a fake pi process past timeout) cannot pass today"
thought_session: season
title: Lease time-to-live — stale leases must surface age and timeout, restarts must carry tier
verdict: pending
---
# hypothesis:a01-1a07c67e-af6ab1

## Hypothesis

**Testable claim:** The `spawn_budget` lease has no time-to-live — a live pid holds its slot forever regardless of `agent_timeout_mins`. Leases that outlive their timeout silently reserve capacity: `spawn_budget status` shows them as live with no age indicator, and `_sweep_locked` reclaims only pid-dead leases. The inline reaper (`_reaper_phase`) never checks elapsed time against the manifest timeout for hung-but-alive pids — it only detects dead pids via `adapter.is_alive()`. This means G4.9's first two commitments (age visibility, time-based reaping) are unmet, and the falsifier (hold a fake pi process past timeout and assert the reaper bounds it) cannot pass today.

To close G4.9, the reaper must:
1. **Surface lease age and restart count** in `spawn_budget status` — lease files already carry `reserved_at`/`spawned_at` but the CLI `status` output omits them; restart count is tracked in `agent.json` per agent but not in the lease file nor in the status output.
2. **Reclaim leases older than the agent timeout** even when the pid is alive — `_sweep_locked` must compare `reserved_at` + `manifest.timeout_seconds` against `now`, so a hung process past its timeout frees the slot. This requires passing timeout info to `_sweep_locked` or to the lease file itself.
3. **Preserve original model/tier across restarts** — `_reap_one` restarts with `rec.get("tier", "kid")` which comes from `agent_record` which was written at spawn time, so tier survives. But `adapter.restart()` receives a `harness` dict from `rec.get("harness_spec", {})` while the original `harness_spec` was never stored — `agent_record` only stores `"harness": harness_name` (the string name). So `restart` has no adapter-level spec to rebuild the command from. This needs either storing `harness_spec` in the record or re-resolving the harness from config by name.
4. **Sync both files on every reaper action** — each `_reap_one` update writes `agent.json` and the manifest entry, but writes them as separate `write_text()` calls without the lock the manifest merge uses, so a concurrent writer could observe disagreement.

### What would prove it

1. A build node implementing time-to-live lease fields: `leases` carry a `"timeout_at"` timestamp set from `manifest.timeout_seconds` + now at `acquire()` time.
2. `spawn_budget status` (or a new `--age` flag) prints each lease's age in seconds and restart count.
3. `_sweep_locked` (or a new `_sweep_stale` pass) reclaims leases whose `timeout_at` is in the past, even when `_lease_is_live(rec)` returns true.
4. `_reap_one` restart preserves the original harness tier and model — verified by: spawn at tier X, kill the agent pid, assert the replacement runs with the same tier flags as the original. `adapter.restart()` resolves `harness_spec` from config by name rather than from a field that was never written.
5. A fixture test: start a fake pi process, write its lease with `timeout_at: now - 1`, run `spawn_budget status`, assert it is reported as stale/expired rather than as live.
6. A concurrency test: two parallel processes, one agent at timeout, assert the expired agent's slot is reclaimed and the second can acquire.

### What would disprove it

1. Adding time-to-live to leases regresses the existing `budget-bound-under-concurrency` test (leases no longer survive their agent's natural lifetime when the agent is still working but the timeout is short).
2. Time-based reclaim kills an agent that is genuinely still productive but past the configured timeout threshold — i.e. the bound becomes an outage for long-running work. (This is a correctness-vs-usefulness tradeoff that G4.9 explicitly accepts: "A parent that outlives its timeout is a bug, not a lease.")
3. `adapter.restart()` cannot reconstruct a correct spawn command from only the harness name string — the harness requires runtime context (context_file path, target, sess_dir) that `rec.get("context_file")` provides, but the adapter config key `"model"` or `"models"` may have changed between spawn and restart, making restarts use a different model than the original tier requested.
4. manifest.json and agent.json drift apart after a reaper restart because the lock file is not held across both `write_text()` calls — a concurrent `post_wire.py` or `heal.py` reads one without the other.

## Agent Notes
Filed hypothesis: lease time-to-live for timeout-based slot reclamation. spawn_budget leases lack timeout field so hung-but-alive pids past agent_timeout_mins are never reclaimed; status CLI omits age/restart-count; restarts in _reap_one carry tier from agent_record but harness_spec is not stored so restart cannot reconstruct the adapter config; manifest/agent.json sync after reaper restarts is lock-free so concurrent writers can disagree. Build nodes needed: (1) timeout_at field on acquire, (2) time-based sweep in _sweep_locked, (3) age display in status, (4) harness_spec serialization on agent_record, (5) locked dual-write in _reap_one.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Second independent review, parent a01-3b0e508a (iter 1082), on top of the a00-dfec16d2 review below which I corroborate claim-by-claim with the same line numbers: spawn_budget.py L227/L266 store only `reserved_at`/`spawned_at` (no TTL field), L154 `_sweep_locked` skips live leases, dispatch.py L658 reaper acts only on dead pids, L529-530 stores `"harness": harness_name` + `"tier"` (so tier DOES survive a restart, harness spec does not), L732 reads `harness_spec` nobody writes. One confirmation the prior review omitted: I verified the tier-survival half of claim 3 directly against L530. No changes to claims or verdict — both reviews agree the node is honest at `pending`/0.3 with zero experiment evidence; the goal's falsifier (fake pi process held past timeout, assert reaper reports and bounds it) is the next node, an experiment under this hypothesis.

Prior review (a00-dfec16d2, iter-1082): spot-checked all four sub-claims against the code — all four hold. Added the schema-required testable_claim; removed the duplicated Agent Notes block (kept the more complete note). The goal's falsifier becomes the experiment.
<!-- THOUGHT:END -->