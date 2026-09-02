---
confidence: 0.8
goal_id: G4.8
goal_kind: subgoal
heading_level: 3
id: "goal:g4.8"
mint_id: 208dc260a25e43959230e94a54785f05
next_edges:
  - hypothesis:a00-a54f694b-b20b78
  - hypothesis:shared-lease-bounds-the-tree
origin: goals-doc
parents:
  - goal:g4
seeds: []
status: active
tags:
  - goal
  - subgoal
title: "G4.8: Many loops at once; the delegator is the director"
type: goal
---

**Several parents each running their own loop, concurrently, against different
regions of the graph, with the delegator holding intent and reviewing across
them.** `goal:g4` already names three tiers and says the delegator "coordinates
several parent/kid groups" — that sentence has never been true. Today there is
one loop, one slot, and the delegator *is* the parent by hand, which is how
every iteration in this project has actually run.

**This is the concurrency goal, and it is deliberately not `goal:g4.4`.** G4.4
is about *specialisation by territory* — many small models each owning a region,
fine-tuned once the territory is stable, gated on **G10**. This goal is about
*running more than one loop at a time at all*, with the generalist models that
exist today. Splitting them matters because G4.4's dependencies are far out and
this one's are all in flight; folding them together would park a near-term
capability behind a horizon.

## What has to exist

1. **A parent brief.** `dispatch.py --tier parent` already spawns and already
   selects `harnesses.<h>.models.parent`, so the model tiering is done. What a
   parent gets handed is the **kid** brief, so it writes one node and stops
   while appearing to have run a loop. `goal:g1.9` owns the assembler; a parent
   brief written by hand here would be exactly the hand-maintained contract
   copy g1.9 exists to delete.
2. **Completion as a graph event.** A parent cannot run a loop without knowing
   its kids finished, and today "done" is `heal.py` polling a pid — the pi
   process model wearing a general name. `goal:g4.6`'s fourth falsifier.
3. ~~**A concurrency bound that survives a tier.**~~ **Built, iter-107.**
   `spawn.parallel` does not bound grandchildren
   (`experiment:a00-763e629b-5c04ad`), and a parent carefully *enforcing* the
   number does not either (`experiment:a00-5f927203-8a66a2`, disproved) —
   because a limit expressed as a number is one each spawner reads its own
   copy of. `bin/spawn_budget.py` puts it in shared state instead: one lease
   per live agent, taken under a lock at the spawn site, reclaimed by liveness.
   A parent gets its kids by running `dispatch.py` again, so **the same
   admission path entered twice is the whole mechanism** — there is no separate
   grandchild path to bound. Measured at caps 1/3/5 against five independent
   spawners opening five slots each: peak equals cap, never exceeds it, where
   the same rig unbounded peaks at 24 of 25
   (`verdict:the-bound-is-structural-now`). This closes **falsifier clause 2
   only**; the other three are untouched.
4. **Kids that do not collide.** `goal:g4.1` — parallel kids share one working
   tree. Unfixed, and it is the failure this goal multiplies rather than
   introduces.
5. **Review that scales past reading everything.** The delegator's whole value
   is holding intent across loops; if directing N parents costs N times reading
   every node, the tier has bought nothing. Parents review kids and report
   deltas; the delegator reviews parents.

## The objective function is `goal:g4.4`'s, and it applies here first

**Functional output per token spent** — not quality alone, not cost alone. A
director on the largest model earns its cost only by multiplying what the tiers
below produce. This goal is where that ratio first becomes measurable, because
one loop cannot exhibit it.

## Falsifier

Two parents run concurrently on the parent model against disjoint targets,
each spawning kids on the kid model, and both complete. Requirements, all four
of which must hold or the run proves nothing: no kid's node is lost or
overwritten by another loop's kid; the total live process count never exceeds
the declared bound; each parent's review gate demotes at least one unevidenced
verdict without the delegator intervening; and the delegator's own token spend
is **sub-linear** in the number of loops. Model tiering is verified by
inspection of the spawned commands, not assumed — a parent silently running on
the kid model would pass every other clause.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted 2026-09-02 at the owner's direction, who asked to "fold in the goal that
allows us to run many agent loops in parallel via parents and you act as
director" and found no goal already holding it.

The judgement call in v1 is that this is not `goal:g4.4`. G4.4's text is about
territory-specialists and fine-tuning, and it declares dependencies on G10 and
G6.8 — stable territory — which are nowhere near ready. The owner's ask needs
none of that: it needs a brief, a completion signal, and a bound. Filing it
under G4.4 would have inherited a horizon this work does not have, and this
project has already watched one goal's framing quietly steer every kid working
under it (`goal:g4.3`), so inheriting the wrong frame is a known, paid-for
failure rather than a hypothetical.

Minted as `active` during a session whose second iteration sweeps 40 active
goals down to roughly 8. That is not an exception being carved out: it is
genuinely in flight this session, and a goal that is being worked is what
`active` means. Adding it to a sweep is cheaper than adding it after one.

The falsifier's last clause — verify the tiering by inspecting the spawned
command — exists because `pi_adapter.model_args` raises rather than falling
back across tiers, and that guard is the only thing standing between "parent on
qwen, kids on deepseek" and a run where everything quietly used one model and
still looked correct. A falsifier that cannot tell those apart is not one.
<!-- THOUGHT:END -->
