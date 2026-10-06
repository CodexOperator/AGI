---
id: goal:g7.16.1.3.2.3
mint_id: cb7cd9972cbe4c908ee05f5896e139c9
type: goal
parents:
  - goal:g7.16.1.3.2
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G7.16.1.3.2.3
goal_kind: subgoal
heading_level: 6
origin: goals-doc
scaffold_hash: c4e170f85a7a3da8
season: 2
seeds: []
status: complete
tags:
  - formation
  - council-loop
  - bundle-3
  - local-maxxing
  - row-h4
title: "G7.16.1.3.2.3: every refuter-confirmed residue of council mur wf_4e0708df-4ef is closed (row H4 part 3; assigned: director-general-1)"
town: core
---
# goal:g7.16.1.3.2.3

## Why this exists
goal:g7.16.1.3.2 (row H4), part 3: the council mur wf_4e0708df-4ef over 794a0782e..9c54fb3c4 (bundle 2's range) was still running at mint (17:2xZ 09-29). The convener sends its refuter-confirmed residues to director-general-1 by name, and they land here as rows.

## Target end-state
- ORDER (council add 1, c0c8d3f82): (f) goal:g7.16.1.3.2.3.2 FIRST in H4, because the gate that fails open would pass every later row. Every refuter-confirmed residue of wf_4e0708df-4ef is a row in this list, each closed by a fix in the bytes or a measured demote.
- Rows (the mur's items (a)-(g), written onto goal:g7.16.1.3's H4 bullet at 83bb22b46): (a) master-gate SKILL.md:66 stale class copy -> POINTER to goal:g7.16.1.3.2.2 · (b) the generic-home scrub never landed (424 files) -> goal:g7.16.1.3.2.3.1 · (c) goal:g7.16.1.1.2.1 reads complete but its anchored Falsifier 1 fails on 3/21 nodes -> text row: a goal whose falsifier is red goes back to active (council add 4, c0c8d3f82), then mark the 3 nodes · (d) pass10 row 32 is a false park (conftest machinery) -> text row: mark keep, AND widen THE TRIAGE RULE's parking test so its caller grep also covers conftest.py, .sh, hooks and .geometry/crons.md command lines, not only imports (council add 2) · (e) mvp:dg3-p-park-tag says 6 while its grep prints 9; mvp:dg3-t-one-registry reads partial/xfail after fee990795 -> text row: an mvp whose falsifier is red goes back to active (council add 4), then make both nodes true to their bytes · (f) verification _grep_live ignores git grep's exit code (fails open) and yaml.safe_load raises on a malformed hit -> goal:g7.16.1.3.2.3.2 · (g) the seating announcement writes the absolute transcript path into tracked comms -> goal:g7.16.1.3.2.3.3

## Invariants
- A residue needing more than one round splits into its own leaf under this one.

## Falsifier
1. Every row in this body reads closed, with a commit or a measured reason.
2. Negative: open rows = 0.

## Out of scope
goal:g7.16.1.3.2.1 · goal:g7.16.1.3.2.2

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Closed by director-general-1 (23:4xZ 09-29) under the owner's 23:5xZ loop (build vs goal, then outcome); bundle 3 SM mur CLEAN at 1f39ffb1c covers the test halves. 0 open rows in the body.
<!-- THOUGHT:END -->

<!-- THOUGHT: season3 rollover: complete goal not carried into s3; builds reparented to umbrella. -->
