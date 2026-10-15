---
id: goal:g4.18.1.4
mint_id: 42d61a432c574e70a70767958276eb62
type: goal
parents:
  - goal:g4.18.1
next_edges: []
confidence: 0.7
edited_by: director-general-1
goal_id: G4.18.1.4
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: 4525ce3fdd159882
season: 2
seeds: []
status: active
tags:
  - engine
  - write
title: "G4.18.1.4: the location row -- names the raw file; a row change renames it in one commit; a directory move needs an explicit confirm"
town: core
---
# goal:g4.18.1.4

# goal:g4.18.1.4

## OWNER 2026-09-26 ~23:2xZ, verbatim (fragment; whole quote on goal:g4.18.1)
"And each build node contains a reference to the location of its actual file." / "Then the node automatically gains the file name as well, and the file can be renamed via a node write/mint by using the location row change. It just checks and confirms if you literally ask to move the file to a new location not just a rename."

## Why this exists
goal:g4.18.1 -- a node's raw file is linked by `payload_ref`, but moving the file is a separate hand `git mv` plus a hand ref edit, so the two drift; the predecessor's reading (c): the location row = the file path, the mint id never changes (G2.5).

gap (measured 09-29 by director-general-3, bundle 1 row D narrowing; moved into the body by director-general-1): no write path moves a payload file when its location row changes (os.rename / .rename( / shutil.move / git mv in write.py + node_writer.py = 0 hits); --payload creates a file at mint, never renames one.

## Target end-state
- A node's location row names its raw file; minting with a location creates the file there and fills the row.
- Changing the location row by a node write renames the file and updates the row in ONE commit; the mint id and grid history are untouched.
- A change that moves the file to another DIRECTORY (not a rename in place) is refused unless the write explicitly confirms the move.

## Invariants
- After any write, the location row resolves to an existing file (links.py reports 0 broken payload refs).

## Falsifier
1. A location-row rename on a temp build node leaves the file at the new name, the row pointing to it and the mint id equal, in one commit, exit 0.
2. Negative: a directory move without the confirm refuses and moves nothing.

## Out of scope
goal:g4.18.1.1 · goal:g4.18.1.2 · goal:g4.18.1.3 · goal:g4.18.1.5

## Agent Notes
Assigned to **director-engine**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Residue 6 of sanctuary-master mur wf_a56d005b-d6b (bundle 1, fixed by director-general-1): the measured gap line that narrowed this goal (director-general-3, row D) lived only in THOUGHT, which is rewritten whole each version, while goal:g7.16.1.1.4 F2 reads it; it now sits in the body under Why this exists, and this block records only why this version moved it.
<!-- THOUGHT:END -->
