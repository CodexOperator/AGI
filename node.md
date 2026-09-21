---
id: goal:g4
mint_id: 8d0f63708d94497d86da5e2eccd3ee79
type: goal
confidence: 1.0
edited_by: season.py
goal_id: G4
goal_kind: long-term
heading_level: 2
origin: goals-doc
season: 1
seeds:
  - goal:g4.1
  - goal:g4.2
  - goal:g4.3
  - goal:g4.4
  - goal:g4.5
  - goal:g4.8
  - idea:engine-agi-bridge-index
  - idea:engine-dispatch
  - idea:engine-heal
status: horizon
tags:
  - goal
  - root
thought_session: season
title: "G4: Right model at the right grain, several goals at once"
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