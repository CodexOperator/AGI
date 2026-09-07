---
id: hypothesis:per-spawn-keys-cost-under-a-second
mint_id: 8c193121f6ce4aa6b9b226f063f2c1c7
type: hypothesis
parents:
  - goal:g1.11
next_edges:
  - experiment:mint-latency-and-a-live-spawn
confidence: 0.85
edited_by: season.py
scaffold_hash: 1eca7dbcc740cd65
season: 1
testable_claim: Minting one OpenRouter key costs under 1s and does not degrade under concurrency, so issuing per spawn is affordable — and per-spawn is the only granularity that gives per-agent attribution, which is one of goal:g1.11's requirements.
thought_session: season
title: Per-spawn credentials are affordable, so batching buys nothing worth its cost in attribution
verdict: pending
---
# hypothesis:per-spawn-keys-cost-under-a-second

## Hypothesis

`goal:g1.11` records three candidate granularities for issuing keys — per
spawn, per `ceil(max_live / 3)` batch, or one per slot minted at loop start —
and deliberately does not choose. **Batching exists only to amortise a cost.**
If that cost is small, batching is paying attribution to buy nothing.

### Testable claim

Minting one key through OpenRouter's key-management API costs **under one
second**, and ten concurrent mints complete in **wall time comparable to one**
— i.e. the call does not serialise behind a rate limiter at the concurrency
this engine actually reaches (`spawn.max_live: 25`). If both hold, per-spawn
issuance adds under a second to a spawn path whose agents run for up to
twenty minutes, and the amortisation argument for batching disappears.

### What would prove it

- Mean mint latency < 1s over at least 10 serial calls, with the max also < 1s.
- 10 concurrent mints completing in wall time within ~2x a single call.
- Zero failures across the sample, since a per-spawn scheme multiplies any
  failure rate by the number of spawns.
- Revocation at the same concurrency completing without loss.

### What would disprove it

- Latency above ~2s, or a heavy tail: per-spawn would then add minutes of
  critical-path latency across a ten-iteration run at 25 live agents.
- Rate limiting at 10 concurrent, which is well below `max_live` — batching
  would then be forced regardless of what attribution wants.
- Any failure rate high enough that 250 mints per run would reliably break one.

### The attribution half, which is not a cost question

`goal:g1.11` requirement 5 asks that the spend line answer *"which agent"*
without correlating timestamps by hand. **Per-slot cannot do that** — a slot is
occupied by a succession of agents, so the key names a slot and the answer is
"one of these five". Per-spawn names the agent. So the two granularities are
not merely cheaper and dearer versions of one design; only one of them
satisfies a requirement the goal already states.

### The convergence this predicts

If per-spawn wins, it should fall out of the existing structure rather than
needing new machinery: `spawn_budget`'s lease is already per-agent and already
reclaimed by liveness, so hanging the credential on the lease makes
*reclaiming the slot* and *revoking the key* one event instead of two that can
disagree. **A design that needs a second bookkeeping structure to track keys is
evidence the granularity is wrong.**

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted to settle a decision the goal banked rather than to explore an unknown.
The framing that matters is that batching is not a design with its own merits —
it is a cost optimisation, so measuring the cost is dispositive. Stating it
that way makes the experiment small and makes a null result meaningful in both
directions.

The attribution paragraph is here because the cost measurement alone could
produce the wrong decision. If mint latency had come in at 3s, the honest
conclusion would still not be "batch by slot" — it would be "batching costs a
stated requirement, so either drop the requirement or pay the latency". A
hypothesis that measured only latency would have let a requirement be traded
away silently.

The last section is a prediction rather than a claim, and it is written as one
on purpose: "the right granularity needs no new bookkeeping" is a design
intuition, and if the implementation had needed a second structure that would
have been evidence against per-spawn rather than an inconvenience to work
around.
<!-- THOUGHT:END -->