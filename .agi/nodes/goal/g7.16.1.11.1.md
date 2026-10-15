---
id: goal:g7.16.1.11.1
mint_id: 6641d98907d940738e81c6ccfeadc307
type: goal
parents:
  - goal:g7.16.1.11
next_edges: []
confidence: 0.9
edited_by: belam
goal_id: G7.16.1.11.1
goal_kind: subgoal
origin: owner
scaffold_hash: 562376f513bd8834
season: 2
seeds: []
status: complete
tags:
  - council-loop
  - redesign
  - bundle
title: "G7.16.1.11.1: rounds 1-3 designed the radically simple engine and minted config:engine (v1 11,305 B, v2 11,900 B, every piece byte-exact)"
town: core
---
# goal:g7.16.1.11.1

## Why this exists
Parent goal:g7.16.1.11: The council's rounds 1-3 on goal:g7.16.1.11 (r1 wrap 1,432 B, r2 living system 4,253 B, r3 config:engine minted; spike re-mint v2 22/22 exact) -- the first bundle of the new engine.
## Target end-state
rounds 1-3 designed the radically simple engine and minted config:engine (v1 11,305 B, v2 11,900 B, every piece byte-exact).
## Invariants
config:engine exists as one read: diagram, loop, pieces, each piece extractable by `sect`.
## Falsifier
1. `grep -q '^# config:engine' .agi/nodes/.geometry/engine.md` exits 0
2. negative: a second live engine piece outside .geometry: `git grep -n -E '^id: config:engine' -- .agi/nodes | awk -F: '$2==2' | grep -vc '^.agi/nodes/.geometry/'` prints 0 (line 2 = the node's own id; doc nodes that quote an old draft carry the id deeper in a fence)
## Out of scope
the sibling leaves goal:g7.16.1.11.1 through goal:g7.16.1.11.10, each its own end-state
## OWNER, verbatim
"Stages 1-2 now, stop before 3" (owner, 09-30/10-01; verbatim on goal:g7.16.1.11)
## Agent Notes
Assigned to **council**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-1 10-07 (goal:g1.41 PASS B4; this goal was minted complete with no measurement recorded): falsifiers run at trunk 86d234fcd1. F1 `grep -q '^# config:engine' engine.md` rc 0. F2 as first written counted every node whose slug contains 'engine' (141 files, 60 by basename): it could never read zero, so it now tests the intent (a live config:engine* node outside .geometry): 0 of 5. The title's v1 11,305 B and v2 11,900 B are the round-1/2 doc figures, NOT re-measured here (engine.md has since been split into five pieces; whole engine.md is 9,307 B at that trunk).
<!-- THOUGHT:END -->
