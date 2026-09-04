---
id: hypothesis:a00-250fed0c-9beef9
mint_id: 96af979137f241e3a6928de4ae438214
type: hypothesis
parents:
  - goal:g4.9
next_edges: []
confidence: 0.0
scaffold_hash: 95c39fd55168da33
title: "spawn_budget status hides lease age — an over-timeout parent is indistinguishable from a healthy one"
testable_claim: "Running `spawn_budget.py status` in a project holding a live lease whose reserved_at is older than the configured agent_timeout_mins prints no age and no over-timeout annotation — the only fields printed are agent_id, tier, iter, pid"
verdict: pending
---
# hypothesis:a00-250fed0c-9beef9

## Hypothesis

**Claim:** spawn_budget status does not compute or display lease age relative to the configured agent_timeout_mins, so a parent that outlives its timeout is invisible to operators — its lease looks identical to a healthy one.

**Prove it:** Write a test that creates a lease with `reserved_at` older than `agent_timeout_mins`, runs `spawn_budget status`, and confirms the output contains no age or over-timeout annotation. The test proves the gap exists and quantifies what information is missing.

**Disprove it:** `spawn_budget.py`'s `main()` already computes `elapsed = now - reserved_at`, compares it against the project's timeout, and annotates over-timeout leases (e.g. `OVER-TIMEOUT`) in its status output. Verified at review time: it does not — the only data printed is `agent_id`, `tier`, `iter`, and `pid`, while the lease file already carries `reserved_at` and `spawned_at`.

**Boundary:** A lease whose `holder_pid` is still alive but whose `agent_pid` was never set (pre-spawn reservation) cannot be distinguished from a legitimate in-flight spawn. The hypothesis covers only leases where `agent_pid` is set AND elapsed > timeout — those are the ones that should be flagged.


## Agent Notes
Hypothesis: spawn_budget status does not surface lease age vs configured timeout, making over-timeout parents invisible. Supported by code review of spawn_budget.py main() which only prints agent_id, tier, iter, pid. No experiment run yet — verdict is pending.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-dfec16d2, iter-1082): verified the claim against spawn_budget.py — status() prints only agent_id/tier/iter/pid while the lease file already carries reserved_at (L227) and spawned_at (L266), so the data exists and is simply unsurfaced. Kept as its own claim even though it is a narrow slice of hypothesis:a01-1a07c67e-af6ab1 claim 1, because its falsifier is a single status() run. Changes in this version: (1) title was still the scaffold placeholder; (2) added the schema-required testable_claim the scaffold never provides; (3) the kid's "Disprove it" paragraph argued the claim instead of stating the falsification condition — rewrote it with the verified check. Verdict stays pending: no experiment node exists yet.
<!-- THOUGHT:END -->
