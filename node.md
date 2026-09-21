---
id: goal:g1.17
mint_id: 72bc8c7896ce49f6ab07c6e104408312
type: goal
parents:
  - goal:g1
next_edges: []
edited_by: belam-S1-L4-V
goal_id: G1.17
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: 47478845a6e15ffc
season: 2
status: horizon
thought_session: f3b92df1
title: "G1.17: Most engine functions are DRIVEN — the tool prints the next step, the agent types only what it is told"
---
<!-- BODY:BEGIN -->
# goal:g1.17

## Agent Notes
OWNER 2026-09-10 (verbatim in doc:l4-owner-decisions): 'Most functions should be driven ideally since that'll likely reduce token use significantly but that can be a subgoal under the relevant perpetual goal for later.' Minted HORIZON — declared and committed to, not yet worked — per 'for later'. WHAT DRIVEN MEANS HERE, from the owner's rotation message the same night: like a console that says 'now type your password, then hit enter' — the tool feeds the agent one step at a time, the literal tokens to type and the key to press, so the agent spends no tokens deciding what to do next and cannot skip or reorder a step. The first two driven surfaces are rotation (rotate.py rotate-self as ONE call, hypothesis:l4-the-predecessor-hands-over-authority) and startup (rotate.py next, hypothesis:l4-startup-is-one-script-or-a-driven-prompt), both under goal:g17 because they are seat protocol. This goal is the generalization: every repeated, mechanical engine function gets a driven form, and the measure is tokens per invocation before and after. Parent is goal:g1 because the engine's standard commands are declared in a node (g1.10) and named node operations already turn hand edits into engine actions (g13.1) — a driven form is the next step of the same idea: the command tells you the command.
