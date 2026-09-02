---
confidence: 0.9
goal_id: G1.11
goal_kind: subgoal
heading_level: 3
id: "goal:g1.11"
mint_id: 9d41f7ac6b2e4d0fa5c38e71b04d29f6
next_edges:
  - hypothesis:per-spawn-keys-cost-under-a-second
origin: goals-doc
parents:
  - goal:g1
seeds: []
status: active
tags:
  - goal
  - subgoal
title: "G1.11: A fresh, credit-capped provider key per spawn — not one key for the whole run"
type: goal
---

**Today every spawned agent inherits the same long-lived
`OPENROUTER_API_KEY`, and that one key is the whole balance.** One runaway kid
in a retry loop can spend it; one leaked context can expose it; and when the
spend line looks wrong there is nothing in the bill that says which agent did
it. The key is a single point of failure, a single point of leak, and a single
point of attribution — three problems that happen to share one cause.

**The owner holds an OpenRouter provisioning key, which mints and revokes
runtime keys.** That turns the credential from a constant into something the
engine can *issue*: a short-lived, credit-capped key created at the start of a
director loop, handed to the spawns that need it, and revoked when the loop
ends.

## Config-maxxing, applied to credentials

This is `goal:g1`'s invariant on the one surface still improvising. Everything
else a run does is declared — metrics, dispatch, harnesses, schemas, cron
cadences, and now the spawn budget. **The credential a spawn uses is decided by
whatever happened to be in the environment.** Under this goal the key becomes
declared: how many are minted, what each is capped at, what scope it carries,
and when it dies.

`.geometry/secrets.md` already declares *where* credentials live and *which*
keys exist; it now declares `OPENROUTER_PROVISIONING_KEY` as optional and says
plainly that it is never inherited by a child. **This goal is the code path
that reads it** — the same relationship `envfile.py` has to that node, one
layer up.

## The batching question, and why it is the design decision

The owner named three candidate granularities: one key per spawn, one key per
`ceil(max_live / 3)` batch, or one key per max-concurrent-spawn slot minted at
the start of the loop. They trade the same two things against each other:

- **Per spawn** is the strongest isolation and the most API calls — at 25 live
  agents and ten iterations that is hundreds of mint/revoke round trips, each
  a place a run can fail for a reason that has nothing to do with the work.
- **Per slot, minted once at loop start** is the fewest calls and the coarsest
  blast radius: `max_live` keys, reused by whichever agent occupies the slot.
  It also composes exactly with `spawn_budget`, which already owns the notion
  of a bounded set of slots — **a lease and a key are the same object at
  different layers**, and that is the strongest argument for this shape.

**Settled 2026-09-02 by `verdict:per-spawn-beats-batching`: per spawn.** The
cost that motivated batching was measured at **0.77s mean per mint**, with ten
concurrent mints completing in 0.92s wall — 0.06% of the 20-minute agent
timeout it gates, and no rate limiting at the concurrency this engine reaches.
Batching is a cost optimisation and nothing else, so a measurement decides it.

Two things then agreed rather than one. Per-slot **cannot** satisfy requirement
5 below, because a slot is occupied by a succession of agents and its key names
the slot; and per-spawn needed no new bookkeeping, because `spawn_budget`'s
lease is already per-agent and already reclaimed by liveness. The credential
hangs on the lease, so reclaiming the slot and revoking the key are one event.

## What has to exist

1. **A minting module** that reads `OPENROUTER_PROVISIONING_KEY` through
   `envfile.py` — never a literal, never `os.environ` directly — and creates
   keys with an explicit credit limit and a name that identifies the run.
2. **Issuance wired to `spawn_budget`.** A slot already has a lease taken at
   the spawn site; the key should ride on it, so there is one admission path
   that grants both. If issuing a key needs a second code path, the seam is
   wrong (`goal:g4.6`'s argument, applied again).
3. **Revocation that survives a crash.** A director that dies mid-loop must
   not leave live keys behind. Reclaiming by liveness — the property
   `spawn_budget` already has — is the shape; a cleanup step that only runs on
   the happy path is not.
4. **The provisioning key scrubbed from every child environment.**
   `dispatch.py` already scrubs `ANTHROPIC_*` and `CLAUDE_CODE_*` so pi
   children cannot bill the Claude subscription. A kid holding the
   provisioning key could mint uncapped keys or revoke the ones the run
   depends on, which is strictly worse. **Same mechanism, one more name.**
5. **Attribution.** A minted key carries the iteration and agent id in its
   name, so the spend line answers "which agent" without anyone correlating
   timestamps by hand.

## Falsifier

A loop runs with `OPENROUTER_PROVISIONING_KEY` set and every spawned agent
authenticates with a key it did not have before the loop started. Killing the
director mid-run leaves **zero** live minted keys within one reclamation
interval. A kid's environment contains no provisioning key — verified by
inspecting the spawned command's environment, not by reading the scrub list.
And the loop still runs to completion with the provisioning key **absent**,
falling back to the single runtime key, because a hardening feature that
becomes a hard dependency has made the project more fragile, not less.

## Deliberately not in scope

Rotating `OPENROUTER_API_KEY` itself, a secret store, or anything touching
`MINIMAX_API_KEY` / `OPENAI_API_KEY`. One provider, one mechanism, proved
before it is generalised.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted 2026-09-02 at the owner's direction, on the same message that raised
`spawn.max_live` to 25 — and the two are the same concern seen twice. Raising
the concurrent population to 25 raises exactly the risk this goal addresses:
more agents sharing one key means more ways for one of them to spend or leak
the whole balance, and no way to tell afterwards which one did.

Filed under `goal:g1` rather than as a security ticket because it *is*
config-maxxing. The owner's framing for G1 is that everything is declared and
nothing is improvised; a credential picked up from the ambient environment is
the last big improvisation in a spawn.

The batching question was recorded unanswered in v1 and is answered in this
version, within the same session — which is the sequence the rule was for, not
a failure of it. v1 refused to pick before mint latency was measured; the
measurement took four minutes and decided it. **The candidate framing is left
standing above the answer on purpose**, because a goal that shows only the
conclusion cannot be re-argued, and the per-slot case was strong enough that a
later reader deserves to see why it lost rather than being told it did.

What actually settled it was not the latency alone. Per-slot fails requirement
5 — a slot outlives the agents in it, so its key names the wrong thing — and
that would have held even at 3s per mint. The honest counterfactual is
recorded in `verdict:per-spawn-beats-batching`: had latency been high, the
answer would have been "batching costs a stated requirement, so drop the
requirement or pay the latency", never a silent trade.

The leading-candidate note in v1 said a lease and a key are the same object at
two layers. That turned out to be the right intuition attached to the wrong
granularity: a lease is per-**agent**, not per-slot, so the argument was always
an argument for per-spawn and v1 misread its own reasoning.

The last falsifier clause is the one most likely to be dropped under pressure
and is therefore stated first-class: the loop must still run with no
provisioning key at all. A project that cannot start without a key-management
API is less robust than the one that shared a single key, and it would have
gotten there while calling itself hardened.
<!-- THOUGHT:END -->
