---
id: goal:g7.16.1.11.46
mint_id: 6b63ebfbbdf54781bd51ca4f4dab2ad0
type: goal
parents:
  - goal:g7.16.1.11
next_edges: []
confidence: 0.5
edited_by: belam
goal_id: G7.16.1.11.46
goal_kind: subgoal
origin: goal
seeds:
  - doc:brainstorm-unify
tags:
  - brainstorm
role: prime_director
season: 3
status: active
title: "G7.16.1.11.46: the brainstorm bundle -- every rule a matrix cell in .geometry projected into a piece that reads it; built in waves 0-4 (doc:brainstorm-unify), each wave one council brief with a gate line"
town: local-maxxing
---
# goal:g7.16.1.11.46

## Why this exists
goal:g7.16.1.11 (the engine every post runs on): the owner's 10-22/23 brainstorm with a Fable fork of the Prime's session produced doc:brainstorm-unify (§0-§39) and 62 owner asks (doc:card-belam §7 ATOMS). On 10-23 the owner handed it to the Prime to run through council in waves, never all at once. This goal is the umbrella those waves nest under; each wave's leaves are cut by the council from one brief.

## OWNER 2026-10-23, verbatim (to belam, in the Prime's pane)
"youre getting an internal claude message soon from the brainstorm"
"feel free to start acting I have to go for a while so just pursue the bundle independently as much as possible and bank questions if absolutely needed. I believe in you"
"use council input for the design phases of course but you're right the banking part doesn't need any council input."
Relayed by the fork (its hand-off file, 10-23): "hand this back to the Prime; start work on the document; run it through council THE USUAL WAY, IN WAVES — never council designing everything at once." and "just let prime handle it".

## OWNER 2026-10-24 07:2xZ, verbatim (to belam, in the Prime's pane, on the g4.18.7 bank line)
"Retire write py for sure we don’t need it at all and need to retire that whole build node as the capsule wrapper now tags everything for us using standard read routes. We need to redo the renderer if needed to be a git based graph system that uses the minimal shell code matrix integrated design"

## Target end-state
- Wave 0 (the Prime alone): the doc is a node (reference), the 62 atoms (the ledger header says 60; its tables hold 62 rows) are rows in the card's §7, V0 is on the trunk, the owner-only asks are banked.
- Waves 1-4 each ran as ONE council brief naming its doc sections; the council returned the leaf set with falsifiers; directors built through the one spawn route; the wave's gate line passed before the next brief was cut:
  - wave 1 gate: M1-M4 and C1-C3 falsifiers pass; P1's board numbers exist;
  - wave 2 gate: one rename end to end with 0 edits; one node's history visible only on its refs/grid/<mint>;
  - wave 3 gate: a planted red found and fixed with no director turn; a held root action printed from the closed set;
  - wave 4: its leaves complete.
- Every atom in the card's §7 is placed (a leaf, an idea, a decision line, or out with a reason); the TRAJECTORY line "10-23 brainstorm (doc:brainstorm-unify) atoms=62 placed=62 → <leaf ids>" is on town:local-maxxing.

## Invariants
- The doc is reference, never placement: an ask is placed only when its leaf, idea or decision line exists.
- One wave at a time: no brief for wave n+1 before wave n's gate line passes.
- Season 4 items (§15) stay out: PQ signatures, the numeric control surface, the hardware alphabet, WIF per-kid tokens, income and streaming.
- Holds from before the brainstorm stand: nothing more is built on the move tooling; the director-review-1 rename (.45.5) waits for V1.
- Spend only on what the owner named; owner-only acts (Console org, Doppler token, workspaces, account roles) are banked in the card's §6.

## Falsifier
1. `awk '/^## §7/,0' .agi/nodes/doc/card-belam.md | grep -c '| target:'` prints 0 (no unplaced atom), and `git grep -c 'atoms=62 placed=62' -- .agi/nodes/town/local-maxxing.md` is at least 1.
2. Negative: `git grep -l '^status: active' -- '.agi/nodes/goal/g7.16.1.11.46.*.md'` prints nothing (every wave leaf is closed or retired).

## Out of scope
goal:g7.16.1.11.44 (the pack format; its move half is superseded by U6 here only when U6 lands) · goal:g7.16.1.11.45 (closed) · season 4 (§15 of the doc).

## Agent Notes
Assigned to **belam**.
