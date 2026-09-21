---
id: experiment:mint-latency-and-a-live-spawn
mint_id: 7a6054f9aca04bec94cc0e9cb5db7b3f
type: experiment
parents:
  - hypothesis:per-spawn-keys-cost-under-a-second
next_edges:
  - verdict:per-spawn-beats-batching
confidence: 0.96
edited_by: season.py
evidence_runs:
  - experiment:mint-latency-and-a-live-spawn
scaffold_hash: 57c2044e4b2806cf
season: 1
thought_session: season
title: Mint latency against the live API, and one real spawn end to end
verdict: proved
---
# experiment:mint-latency-and-a-live-spawn

## Experiment

Two parts, run 2026-09-02 against OpenRouter's live key-management API with a
real provisioning key: **latency**, which settles the batching question, and
**one full spawn**, which verifies the wiring does in reality what the unit
tests say it does.

### Part 1 — latency and concurrency

| measure | n | result |
|---|---|---|
| serial mint | 10 | mean **0.760s**, p50 0.747s, max **0.859s**, 10/10 ok |
| concurrent mint (10 at once) | 10 | **wall 0.919s**, mean 0.773s, max 0.908s, 10/10 ok |
| concurrent revoke (20 at once) | 20 | **wall 2.781s**, 20/20 ok |
| keys leaked after cleanup | — | **0** |

**Ten concurrent mints cost 0.92s of wall time — barely more than one.** There
is no rate limiting at the concurrency this engine reaches, so the amortisation
that batching exists to buy is worth under a second per loop.

Cost of each candidate granularity, at `max_live: 25` over a ten-iteration run:

| granularity | mints per run | added critical-path latency | attribution |
|---|---|---|---|
| per slot, at loop start | ~25 | ~1s once | **slot**, not agent |
| per `ceil(25/3)` batch | ~90 | ~1s per batch | batch |
| **per spawn** | ~250 | **~0.77s per spawn** | **agent** |

0.77s against a 20-minute agent timeout is **0.06%** of the thing it gates.

### Part 2 — one live spawn, end to end

`dispatch.py . 908 --tier parent --target goal:g1.11 --level small`, with
`harnesses.pi.bin` pointed at a stub that dumps its own environment and exits.
`--tier parent` because a parent scaffolds no node, so nothing entered the
graph. The config was restored in a `finally`; the session directory and the
stub were deleted.

Observed, in order:

1. `credentials: minting per spawn, limit=$0.25 ttl=60min`
2. Key minted, named **`agi-iter908-parent-a00-245fe1f5`** — iteration, tier
   and agent id, which is requirement 5 satisfied by inspection.
3. `limit: 0.25`, `expires_at: 2026-09-02T17:36:46.835Z` — both caps present.
4. **Child environment: `OPENROUTER_API_KEY` present (`sk-or-v1-e35...`),
   `OPENROUTER_PROVISIONING_KEY` absent.** Read out of the spawned process's
   own environment, not out of the scrub list — which is what `goal:g1.11`'s
   falsifier demands, because reading the list only proves the list.
5. Lease carried the 64-char **hash** and no secret.
6. Stub exited. The next sweep reclaimed the lease and **revoked the key**:
   engine-minted keys went 1 → 0 with no cleanup step run by hand.
7. Leak audit over every file under `sessions/` and the lease directory: **no
   `sk-or-` string anywhere.**

### Part 3 — the TTL trap, found by running it

`expires_in_seconds` is **accepted with a `201` and silently ignored**, giving
back a key with `expires_at: null` — a key with no TTL, from a call that looked
like it worked. Only `expires_at` as an ISO-8601 `Z` timestamp is honoured.
Verified both ways, and `mint` now refuses a TTL-less key: it revokes it
immediately and raises, rather than handing out a credential that outlives
every other guarantee in the module.

### A near miss worth recording

The owner's own long-lived key is named **`agi`**. `reap_orphans` matches on
`agi-` **with the hyphen**, so it is out of scope — confirmed by a dry run
reporting `would revoke 0`. Had the prefix check been `startswith("agi")`, the
first reap would have revoked the key the whole project runs on.

### What this experiment does NOT show

- **No pi agent ran.** The child was a stub. What is proved is the credential
  path, not that a real agent authenticates with a minted key and completes.
- **Spend attribution is proved by the key's *name*, not by a bill.** No
  minted key was ever used, so nothing appeared against one in the dashboard.
- **Latency was measured from one machine, once.** A slow network or an
  OpenRouter incident would change the numbers, though not the ranking.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The two parts answer different questions and were nearly split into two
experiments. They are one because part 2 is what stops part 1 from being a
benchmark of an API nobody wired up — the latency numbers only license a
decision if the thing being decided actually works.

Part 3 was not planned. It came from testing whether a TTL could be expressed
as a duration rather than a timestamp, which looked like a convenience
question and turned out to be the sharpest edge in the module: an API that
accepts unknown fields with a 201 will happily hand back a credential missing
the exact property you thought you had asked for. It is recorded as its own
part, and asserted in a live test, because the next person to touch this will
find `expires_in_seconds` more natural and there would be no error to tell them.

The near miss is recorded for the same reason and is not a joke at anyone's
expense: `startswith("agi")` is the obvious spelling, the owner's key is
called `agi`, and the reaper's whole job is revoking keys. One character of
prefix separated a cleanup routine from an outage, and that is worth a
paragraph in the permanent record.

The limits section names the stub explicitly because "end to end" is exactly
the phrase a later reader will over-read.
<!-- THOUGHT:END -->