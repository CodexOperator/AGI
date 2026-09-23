---
id: goal:g1.25.1
mint_id: 84ba4ad3e7eb4d65a96f6efd5f378d17
type: goal
parents:
  - goal:g1.25
next_edges: []
confidence: 0.75
edited_by: director-engine
goal_id: G1.25.1
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: c19699b52227f021
season: 2
seeds:
  - hypothesis:propose-completes-every-argv-or-refuses-and-spend-verbs-are-not-proposable
status: active
tags:
  - config-maxxing
  - cli-grammar
  - jev
  - leaf
title: "G1.25.1: PROPOSE COMPLETES OR REFUSES -- no silently dropped arg, no unmapped placeholder, spend/spawn/destructive verbs not proposable, the [command] schema declares manifest/excluded (the jev mur's demote; assigned director-engine)"
town: local-maxxing
---
# goal:g1.25.1

# goal:g1.25.1 — PROPOSE COMPLETES OR REFUSES; SPEND / SPAWN VERBS NOT PROPOSABLE (the jev mur's demote)

```
leaf      jev's choice surface never hands back an argv it cannot complete, and never offers a verb that spends or spawns
source    the g1.25 mur 09-23 (review accept_with_residue · verify DEMOTE): propose validates then silently drops a required arg for
          19 of 110 proposable entries (e.g. workflow.py:note drops harness_id, workflow.py:register drops script); workflow.py:run
          (side_effects spawn) is proposable while dispatch.py is excluded; extras substitute any <x>; [command].md lacks manifest/excluded
rule      KEEP SPLITTING (owner 09-23, goal:g5): one leaf, one small round
round     hypothesis:propose-completes-every-argv-or-refuses-and-spend-verbs-are-not-proposable
```
