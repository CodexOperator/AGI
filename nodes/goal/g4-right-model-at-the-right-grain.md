---
confidence: 1.0
goal_id: G4
goal_kind: long-term
id: "goal:g4"
origin: goals-doc
seeds:
  - goal:g4.1
  - goal:g4.2
  - goal:g4.3
  - goal:g4.4
  - idea:engine-agi-bridge-index
  - idea:engine-dispatch
  - idea:engine-heal
status: horizon
tags:
  - goal
  - root
title: "G4: Right model at the right grain, several goals at once"
type: goal
---

Model choice is a knob the user sets per tier and experiments with — nothing
hardcoded. Three tiers: **delegator** (the user's own session, holding intent
and coordinating several parent/kid groups), **parent** (a subagent by default,
so review motion never accumulates in the chat the user reads), **kid** (one
node, bounded scope).

**Not refuted by G2's evidence — its price is now a number.** Prose recall of
0.792 from a cheap tier is what a cheap tier is *for*. What is refuted is
handing the cheap tier the contract layer. Tiering survives if the model authors
prose and the harness moves structure.

**Budget invariant:** inner-loop completions count against a single global
iteration budget, so recursion is bounded regardless of nesting depth.

Owns: **L3** (per-tier and eventually per-level model assignment), **L6**
(recursive sub-loops; `cc_dispatch.max_goals_active` exists and is unread).
Blocked on G2 for per-level assignment.
