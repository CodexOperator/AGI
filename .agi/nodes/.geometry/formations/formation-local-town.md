---
id: doc:formation-local-town
mint_id: 1c5a958393ef4cb7bb1ed4fc2c59e2ea
type: doc
parents:
  - goal:g5.18
next_edges: []
edited_by: director-general-3
scaffold_hash: 04e95c468d805e25
season: 2
tags:
  - local-maxxing
  - formation
  - template
title: "THE LOCAL-TOWN FORMATION -- a research-focused formation template: the base templates plus two overrides (the town master is interim ruler over its branch, seats included, while the Prime stays quiet; no point / helper -- directors free-float under the master) and one hedge (a framing check before minting ideas)"
town: local-maxxing
---
# doc:formation-local-town

# doc:formation-local-town

**The LOCAL-TOWN FORMATION -- a research-focused formation template.** Base = `doc:unified-head` (every role) + `doc:unified-master-brief` + `doc:unified-director-brief`. This template overrides the base ONLY where it says so; everything else is the base. Owner 2026-09-23: formation templates may nest recursive overrides of the base -- not implemented programmatically yet; for now local-town is simply its own formation.

## Overrides of the base (owner 2026-09-23 14:5xZ, verbatim in the source column)
| the base says | local-town says | source |
|---|---|---|
| config:posts rows, spawns and re-seats are the Prime's | the town master is INTERIM RULER over its branch -- full authority, seat assignment included -- while the Prime stays quiet | owner 09-19 grant; 09-23: "Yes grant stands. You have full authority as interim ruler over your branch while prime stays quiet." |
| a point and a helper where a town runs two directors | no point / helper: two directors, each works ONLY the batches the town master hands it | owner 09-20; 09-23: "Yes local-town is a new formation template that is research-focused." |
| directors self-loop the trajectory | the town master BATCHES: small research batches to director-thought (one results report once every hypothesis and hypothesis leaf in the batch is built out), small engine-fix batches to director-engine (one report only when the batch is complete, no residue); the master keeps the board's research trajectory current and picks the next batch -- directors keep their nose down on graph build, the master holds the bigger picture | owner 09-24, verbatim: "Let's switch the formation to you batching research rounds and engine rounds as needed. Directors go back to just working the batches - research batches for director thought until all hypotheses and hypothesis leaves are built out then report results, and engine fix batches for director-engine who only reports back when batch complete no residue." |

## Posts
| post | role in this formation |
|---|---|
| thought-master | the town master, interim ruler over its branch (seats included) while the Prime stays quiet |
| director-thought · director-engine | two directors, each works ONLY the batches the town master hands it |

## Stand up / take down (skill agi-post)
Stand up / take down = skill agi-post (§1 down: flags first, kill second · §2 up: row committed BEFORE spawn, card, then spawn); switch = `write.py config:formations 'set active doc:formation-local-town'`, ONE call (Prime / owner), read back by verification.py `formation`.
## Hedge -- a prompt, never a gate
Before minting ideas, a quick framing check: is there a bigger picture here, or a smaller, simpler one? (owner 09-23 07:5xZ-08:2xZ; kept as a hedge 09-23 14:5xZ)

## Where the town's other rules live
The research, dispatch and batch rules: the director cards (`doc:card-director-thought`, `doc:card-director-engine`; `doc:lm-director-brief-customizations` retired 09-24) · spawn limits: the director cards only · the town todo: `town:local-maxxing` trajectory_standin · owner lines: where the HEAD's notes line says (never a goal).

## Agent Notes

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Council bundle 2 row T (director-general-3, goal:g7.16.1.2.8): the stand-up / take-down steps are one pointer line to skill agi-post, and the goal:g7.16 L<n> citations point at goal:g7.16.2 (R5 Falsifier 2, re-scoped onto T). KEPT, mapped to goal g5.18 (its own parent: the local-maxxing town). It is the base formation doc:unified-director-brief names for local-town, so retiring it would orphan a live reference. That map cell is the Prime's write, proposed on mvp:dg3-t-one-registry. Prior THOUGHT: grid history.
<!-- THOUGHT:END -->
