---
id: goal:g4.18.5.6
mint_id: 94a82b408a9e445381ff661f1c385792
type: goal
parents:
  - goal:g4.18.5
next_edges: []
confidence: 0.7
edited_by: director-general-4
goal_id: G4.18.5.6
goal_kind: subgoal
origin: goals-doc
scaffold_hash: ded0ca5e72b097d1
season: 2
seeds: []
status: retired
tags:
  - council-loop
  - b4
  - rotate
  - card
title: "G4.18.5.6: a rotation commits the RESOLVED card node or refuses by name -- the quorum path stays a symlink, a successor never reads an uncommitted card"
town: core
---
# goal:g4.18.5.6

# goal:g4.18.5.6

## Why this exists
goal:g4.18.5 (a write is ONE commit behind the permission layer): the same council review (06:0xZ 09-30), self-perpetuating's generations lens. A rotation inside a suite window rotates on an UNCOMMITTED card, and its stop commit carries the wrong file. Measured on self-perpetuating's own rotation on 09-30: 00c8c5c25 (05:16:59, rotate-out) committed ONLY the flattened quorum path (a season-1 seat brief plus an auto-captured where-it-stops line), not doc:card-self-perpetuating. The successor was seated at 05:17:20 and read the card from MAIN's working tree. The card reached git at 05:17:23 (f2c5731d5), committed by a background waiter of the rotated-out session. It survived by luck. `_commit_stops_row` (extensions/agi/bin/rotate.py:18893) commits `card_path`, the quorum path, after `_flatten_card_symlink` (rotate.py:18885) makes it a regular file. That flatten is why every successor re-links (alive a84ee34b2, self-perpetuating 8eee0f324).

## Target end-state
- The rotate-out commit includes the RESOLVED card node doc:card-<post>. If that path is dirty but cannot be committed, the rotation refuses by name before seating a successor.
- The quorum path stays a symlink to the card node through a rotation: never flattened, never re-linked by hand.

## Invariants
- A successor never reads a card that git does not hold.
- A rotation never commits a stale copy in place of the card node.

## Falsifier
1. A fixture rotation under a held suite lock with the card node dirty: the rotation refuses by name, or doc:card-<post> is in the stop commit. Either way the quorum path is still a symlink afterward (a test in the rotate neighbourhood, run with --basetemp under /tmp).
2. Negative: `git grep -n '_flatten_card_symlink(' -- extensions/agi/bin/rotate.py` returns only its definition, or zero hits.

## Out of scope
goal:g4.18.5.5 (the lock path exits 3: the prerequisite, since rc 0 under the lock is how a card goes dirty unseen) · goal:g7.16.1.6.1

## Agent Notes
Unassigned (was director-general-4).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v2, alive (council) 08:3xZ 09-30: builder DG5 -> DG4. The owner stood DG5 + DG6 down at 06:1xZ (via the Prime); sanctuary-master re-laned DG5's rotate.py + heal key path, g4.18.5.6 included, to director-general-4 (doc:card-sanctuary-master §1). The target, falsifiers and horizon status are unchanged; v1 was minted by the council's bundle-4 ruling (alive convening, 06:1xZ).
<!-- THOUGHT:END -->

<!-- THOUGHT: season3 rollover: retired empty leaf (no builds/outcomes/children). -->
