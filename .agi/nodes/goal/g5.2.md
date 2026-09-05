---
id: goal:g5.2
mint_id: 5a5a74b9f6f347c495b216240cf0e8af
type: goal
parents:
  - goal:g5
  - build:COMPLETE.md
next_edges: []
confidence: 1.0
edited_by: director
goal_id: G5.2
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: 1d476dccd6b13d22
seeds: []
status: horizon
tags:
  - goal
  - subgoal
thought_session: L1.13
title: "G5.2: Splitting a goal is a mechanical act — classifiers and encoders, not taste"
---
# goal:g5.2

## Agent Notes
**Why this exists, with a worked failure.** `goal:g9.4` — the live graph viewport
— was handed to the loop as one goal and came back as a list view: correct
against the words, nowhere near the intent. It should have been split first, into
a hook layer plus two skins plus a player avatar (now `goal:g9.8`, `goal:g9.9`,
`goal:g9.10`), each chasing its own mvp. Nothing in the engine noticed the goal
was too big to aim at, so a director had to, and did not. That is a harness gap,
not a model failure.

`goal:g5.1` says a saturated goal gets broken up. This says the breaking up is
**mechanical**:

- **Classify goals with real classifiers.** OpenRouter-hosted classifier models,
  or plain encoders, over the goal body and its chain. Both are cheap; both
  likely carry usable signal, and which signal is worth having is itself
  research, not a decision to make up front.
- **Score saturation.** How many distinct intents a goal body carries, how many
  independent falsifiers it implies, how far its chains have drifted from its
  words.
- **Propose the split, and eventually perform it** — sub-goals with their own
  mvps — with the classifier's output as the evidence in the node, so the split
  is reviewable rather than asserted.
- **Assign the loop flavor** each sub-goal should launch (`goal:g1.12`).

Falsifier shape: run the classifier over the goal corpus as it stood before
2026-09-04 and check that `goal:g9.4` scores as over-saturated while goals that
closed cleanly in one chain do not.