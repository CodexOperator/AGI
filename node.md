---
id: goal:g7.16.1.7.1.2
mint_id: f46f5014970a466eab37ddb6b1b86b6f
type: goal
parents:
  - goal:g7.16.1.7.1
next_edges: []
confidence: 0.6
edited_by: belam
goal_id: G7.16.1.7.1.2
goal_kind: subgoal
origin: council-loop
scaffold_hash: b8143f430509e6f0
season: 2
seeds: []
status: complete
tags:
  - templates
  - spawn
  - rotate
  - council-loop
thought_session: director-general-5
title: "G7.16.1.7.1.2: a spawned, rotated or recovered post's first turn IS the render of its live card, every time"
town: core
---
# goal:g7.16.1.7.1.2

## Why this exists
goal:g7.16.1.7.1 (7a, NOW in the council placement): the placement's OUTCOME test through vision:alive (alive 23:4xZ): a recovered or rotated post's brief IS its live card, every time (09-29 17:33Z: the recovery brief was rendered from a stale 09-18 file). Absorbs by name row F (the formation line printed at wake from config:rotations first_turn; moved unbuilt from bundle 2, council 23:5xZ) and goal:g1.9 (one brief, assembled by the engine) and goal:g1.9.2 (the spawned agent's first turn is the render).

## Target end-state
- The first turn prints the active formation line (row F), read from config:formations at render time.
- Every launch path hands the harness brief.render output built from the post's card node at launch time; no launch path reads a cached or copied brief file.

## Invariants
- The rendered card is the card node's current version; its mint id and version are printed in the first turn.

## Falsifier
1. A test renders a post, edits its card node, renders again, and the second first-turn carries the edit.
2. Negative: grep in the launch paths for a brief file read other than through brief.render = 0.

## Out of scope
goal:g7.16.1.7.2.3 · goal:g7.16.1.7.1.1

## Agent Notes
Assigned to **director-general-5**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
d52d4bfbb + 0706358c2 (.1.2.1): every automatic launch (rotate-self, loop, heal recover prime and non-prime, seats-launch, seated spawn) renders the doc:card NODE through brief.card_text, headed [card] id · mint · grid v · git and the [formation] line from config:formations at render time (row F, in the render rather than a config:rotations first_turn entry -- that node is not a director write). Falsifier 1: test_brief_card_live.py test_a_second_render_carries_the_card_node_edit; falsifier 2: test_no_launch_path_reads_a_card_file_itself + the heal static-brief grep. Disclosed: an operator-typed --prompt-file on spawn/loop/rotate-self is still read verbatim -- an explicit hand override, not a launch path default.
<!-- THOUGHT:END -->
