---
id: verdict:per-spawn-beats-batching
mint_id: 4a914d2169ce4432ac276eaf176346cf
type: verdict
parents:
  - experiment:mint-latency-and-a-live-spawn
next_edges: []
confidence: 0.96
edited_by: season.py
evidence_runs:
  - experiment:mint-latency-and-a-live-spawn
scaffold_hash: 12e5714ccf548dde
season: 1
thought_session: season
title: Issue one key per spawn; the cost that motivated batching is 0.77s
verdict: proved
---
# verdict:per-spawn-beats-batching

## Verdict

proved

## Evidence

`experiment:mint-latency-and-a-live-spawn`, against the live API:

- **Serial mint: 0.760s mean, 0.859s max, 10/10 ok.**
- **Ten concurrent mints: 0.919s wall** — barely more than one call, so there
  is no rate limiting at the concurrency this engine reaches.
- Twenty concurrent revocations: 2.781s wall, 20/20 ok. Zero keys leaked.
- One live spawn through `dispatch.py` minted a key named
  `agi-iter908-parent-a00-245fe1f5`, injected it into the child as
  `OPENROUTER_API_KEY`, kept `OPENROUTER_PROVISIONING_KEY` out of that child's
  environment, stored only the 64-char hash on the lease, and **revoked the key
  automatically when the agent died** — 1 engine-minted key → 0, no cleanup
  step run by hand, no `sk-or-` string anywhere on disk.

## The decision, and why it is not close

`goal:g1.11` banked three granularities. **Batching is not a design with its
own merits — it is a cost optimisation**, so measuring the cost is
dispositive. The cost is **0.77s per spawn against a 20-minute agent timeout:
0.06% of the thing it gates.**

Against that, per-spawn is the only granularity that satisfies a requirement
the goal already states. Requirement 5 asks that the spend line answer *which
agent* without correlating timestamps by hand. A slot is occupied by a
succession of agents, so a per-slot key names a slot and the honest answer
becomes "one of these five". **Per-slot does not answer the question the goal
asked.**

**The structural argument came out the same way**, which is the part that
would have overridden the numbers had they disagreed. `spawn_budget`'s lease
is already per-agent and already reclaimed by liveness, so hanging the
credential on the lease makes *reclaiming the slot* and *revoking the key* one
event rather than two that can disagree. Per-spawn needed **no new
bookkeeping**; the hypothesis predicted that a granularity requiring a second
tracking structure would be the wrong one, and none was required.

## Three limits, not one, because a cleanup step is not a safety property

The design that follows carries a credit cap, a TTL, and explicit revocation,
and the redundancy is the point: **revocation that only runs on the happy path
is not revocation.** A director killed mid-loop leaves keys that can spend at
most $0.25 each and expire by themselves within the hour.

## What is NOT proved — read this before citing it

- **No pi agent ran.** The child was a stub that dumped its environment. The
  credential *path* is proved; "a real agent authenticates with a minted key
  and completes its work" is not.
- **Attribution is proved by the key's name, not by a bill.** No minted key
  was ever spent against, so nothing has appeared in the dashboard under one.
- **Latency was measured once, from one machine.** An OpenRouter incident or a
  slow link changes the numbers. It would not change the ranking, since
  batching's advantage is bounded by the same latency.
- **`goal:g1.11`'s falsifier is satisfied except for the live-agent clause.**
  Absence-tolerance, scrubbing, crash-safe revocation and attribution all hold.

## Consequence

The batched alternatives are **not** kept as a fallback. If mint latency ever
degrades enough to matter, the answer is a longer TTL and key reuse *within one
agent*, not a coarser granularity — because coarsening trades away attribution,
which is a stated requirement, to buy back a cost that is currently 0.06%.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
This verdict closes a decision the owner banked rather than one they made, so
it states the reasoning at the length a reader would need to overturn it. The
load-bearing sentence is that batching is a cost optimisation and nothing else:
once that is agreed, a measurement decides it, and no amount of design taste
gets a vote.

The consequence section exists because "we can always batch later" is the
obvious escape hatch and it is wrong in a specific way. Coarsening the
granularity spends a requirement to buy back latency; if latency ever becomes
the binding constraint, reusing one key across one agent's retries costs
nothing in attribution and should be tried first. Writing that down now stops
a future reader from reaching for the batched design as though this verdict
had left it on the table.

Confidence 0.96 rather than higher because the live-agent clause is untested
and the latency sample is one machine on one day. Neither would change the
ranking, which is why it is not lower.
<!-- THOUGHT:END -->