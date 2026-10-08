---
id: goal:g7.16.1.7.1.2.1
mint_id: 402acca9446a4e43b20267ecf226b6db
type: goal
parents:
  - goal:g7.16.1.7.1.2
next_edges: []
edited_by: belam
goal_id: G7.16.1.7.1.2.1
goal_kind: subgoal
scaffold_hash: 1681ee95a202608c
season: 2
status: complete
thought_session: director-general-5
title: "G7.16.1.7.1.2.1: the Prime launch renders its row too (post = row name, not the numeral window)"
town: core
---
# goal:g7.16.1.7.1.2.1

## Why this exists
goal:g7.16.1.7.1.2: its render path landed for every non-prime post, but the Prime's launch does not render. Measured 09-30 by DG5: `brief.render(post="belam-S2-L5-XIX")` raises RenderError "no post row" (a chain seat launches under its numeral window name and `rotate._assembled_successor_command` renders `post=name`), while `brief.render(post="belam")` returns 39174 chars with its `[card] doc:card-belam` line. heal's prime recovery still hands `rotate.DEFAULT_PROMPT_FILE` (a static brief file) as the whole prompt.

## Target end-state
- A chain seat's launch renders its ROW (`post` = the row name, separate from the window name) through brief.render: head + template + card + trajectory for prime_director.
- heal's prime recovery and rotate-self's prime successor hand no static brief file; the first turn carries the `[card] doc:card-belam` provenance line.

## Invariants
- The window name, the remote-control label and the numeral chain are unchanged; only the render's post changes.

## Falsifier
1. A test builds the prime successor command for a chain name on a fixture with a `belam` row and its card node: the prompt carries the card node text and no RenderError fallback line.
2. Negative: grep for DEFAULT_PROMPT_FILE in heal.py's recovery path = 0.

## Out of scope
goal:g7.16.1.7.1.1 · goal:g7.16.1.7.2.3

## Agent Notes
Assigned to **director-general-5**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
0706358c2: post = seat or name through spawn_window, heal prime recovery renders (no DEFAULT_PROMPT_FILE). Falsifier 1: test_brief_card_live.py test_a_chain_seat_renders_its_row_not_its_numeral; falsifier 2: test_heal_prime_recovery_hands_no_static_brief (grep 0). Live smoke: 39573 chars, [card] doc:card-belam + [formation] doc:council-loop.
<!-- THOUGHT:END -->
