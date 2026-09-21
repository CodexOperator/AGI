---
id: goal:g1.9
mint_id: d71f94660ce843c0879bd5a9f1d4c121
type: goal
parents:
  - goal:g1
confidence: 1.0
edited_by: season.py
goal_id: G1.9
goal_kind: subgoal
heading_level: 3
origin: goals-doc
season: 1
seeds: []
status: horizon
tags:
  - goal
  - subgoal
thought_session: season
title: "G1.9: One brief, assembled by the engine, never typed per spawn"
---
**A parent should name the target and the tier, and nothing else.** Today
`SKILL.md` tells it to hand-assemble a self-contained prompt per kid, listing
six ingredients by name:

> zoom scope, target parent node id, chain step, node file format, verdict
> taxonomy, project paths (`INJECTION.md`, `GOALS.md`, spec)

Every one of those is already known to the engine at spawn time. The parent is
retyping the harness's own state into a string, once per kid, once per
iteration, forever — and paying tokens to do it in the tier where tokens are
most expensive, because a parent's context carries every brief it wrote for the
rest of the run. **That is the Design Ethic's exact failure mode: motion spent
on operations instead of work**, and it is not even *fresh* motion, it is the
same six facts re-emitted every time.

It is also a correctness problem, not only a cost one. A hand-assembled brief
is a hand-maintained copy of a contract that lives elsewhere, so it drifts, and
it drifts silently — nothing compares the string a parent typed against the
taxonomy the gate actually enforces. Two instances of exactly that were found
in one session on 2026-08-31: kids received a completion contract belonging to
the other runtime (**`goal:s8`**), and the verdict taxonomy reached them as a
bare `:N` that one kid read as `0.6` and lost a verdict to.

## What has to exist

1. **One assembler, not one per caller.** A function that takes
   `(target, tier, iteration)` and returns the whole brief. `zoom.py`'s
   `completion_contract()` is the shape to copy — it exists because the same
   contract had been pasted into three renderers and drifted in all three.
2. **Every varying part derived, not passed.** Zoom scope from the target;
   node format and verdict taxonomy from the schema registry and
   `evidence_gate`, so a change to the enforced rule changes the brief in the
   same commit; project paths from `locations.py`; the map from `zoom.py`.
3. **Tier is a parameter, and the only interesting one.** A parent brief and a
   kid brief differ in scope, permissions and what they own — not in six
   re-typed facts. This is the input `goal:g4.3`'s dispatcher needs for its
   two spawn modes, and building it there instead would put the assembler
   inside one runtime.
4. **A per-project override that is additive.** A project says what is
   *special* about its briefs; it never restates the general ones. Same rule
   as `.agi/config.json` — the customization surface is a delta, never a fork.

## Deliberately in scope: the brief is a file with no node

`extensions/agi/lib/agent-prompt.md` is the pi kid brief today, and
`dispatch.py` appends it. It is one of the files **`goal:g6.6`** names as
outside the graph entirely — *"a change to `agent-prompt.md` alters every kid
in every future iteration, and today that change can be made with no node
behind it"*. The assembler must not inherit that. Whatever it reads from is
graph content, versioned like everything else.

## Where this sits among its neighbours

- **`goal:g1.6`** is the same complaint one layer down — *invoking* a command
  costs ceremony. This is *briefing* an agent costing ceremony. They are the
  two halves of "an action should cost what the action is worth" and should be
  built with the same instinct, not merged.
- **`goal:g1.1`** is why the brief can be small at all: if an agent needs only
  the graph to orient, the brief is a pointer plus a scope, not a manual.
- **`goal:g1.4`** decides what a briefed kid is *allowed* to do. A brief that
  is assembled and a permission set that is enforced are the same statement
  made twice, and stage 2 there should read from here.
- **`goal:g9.3`** — ride along as a kid — is how a human checks the output of
  this without spending an agent. It is the natural falsifier's front-end.
- **`goal:g4.3`** is the first consumer: its CC dispatcher needs parent briefs
  and kid briefs from one place, or it grows its own copy and breaks the
  "runtime flag, not a parallel code path" invariant.

## Falsifier

Spawn a kid and a parent with nothing but a target id and a tier. Both arrive
with a correct, complete brief; neither prompt contains a fact the engine
already knew. Then change the verdict taxonomy in `evidence_gate.py` and spawn
again — **the brief must change with it, in the same commit, with nothing
edited by hand.** Until that second half holds, the drift this goal exists to
remove is still possible, and the first half alone is a convenience.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Raised by the owner while setting up hierarchical loops, with the note that a
related goal already existed. It does — several — and the first draft of this
node tried to be all of them. The distinction that made it its own goal: G1.6
is about the *cost of invoking* a command, G1.1 about *how little an agent
needs to orient*, G1.4 about *what it may touch*. None of them says the brief
itself should be assembled rather than typed, and SKILL.md still instructs a
parent to type it, ingredient by ingredient.

Written as active rather than horizon because the session that raised it also
produced its evidence twice over: the wrong-runtime contract and the
ambiguous `:N` were both hand-maintained copies of a contract enforced
elsewhere, and both cost a live kid something. That reframes the goal —
assembly is not an ergonomic upgrade, it is the only way the brief and the
gate can be the same fact. The falsifier is written to test that half
specifically, because the convenience half will look done long before the
drift half is.
<!-- THOUGHT:END -->