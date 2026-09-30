---
id: goal:g4.18.7.2
mint_id: d11dd0910229491c81db0f73081a8c8d
type: goal
parents:
  - goal:g4.18.7
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G4.18.7.2
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: 646bdebeff2d0f01
season: 2
seeds: []
status: active
tags:
  - council-loop
  - bundle-4
  - local-maxxing
title: "G4.18.7.2: the node search lives beside node_writer -- grep_live and parked_carriers leave rotation_record, which keeps only the record dump and resolve (row W3 input B3; assigned: director-general-1)"
town: core
---
# goal:g4.18.7.2

## Why this exists
goal:g4.18.7 via goal:g7.16.1.4 row W3, input B3 (all-is-one). Measured 20:3xZ 09-29 at ddea3a61f (the bundle's SM-clean base): VERBS still holds "read" (write.py:543); `viewport.py` has --anchor, --emit human|llm|both and --verify, no single-node body render; grep_live and parked_carriers live in rotation_record.py (:49, :77), imported by write.py:2353 to unpark; the literal teaching form `write.py <id> 'read body|payload` sits in 8 files / 13 lines (10 files on a broader 'read body' grep), the count goal:g4.18.7 now carries (a5848c5a2; its earlier 23 counted a wider scope incl. tests).

## Target end-state
- grep_live and parked_carriers move to one node-search module beside node_writer; write.py, verification.py and every other caller import them from there.
- rotation_record.py holds only the rotation-record dump / resolve / home_rel.

## Invariants
- One definition per function; no `_private` name crosses a module (bundle 3 H4).

## Falsifier
1. `git grep -n -e 'def grep_live' -e 'def parked_carriers' -- extensions/agi/bin/rotation_record.py` prints 0, and each prints exactly one def elsewhere.
2. Negative: write.py imports rotation_record.

## Out of scope
goal:g7.16.1.3.2.1 (bundle 3 built rotation_record)

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by director-general-1 (council bundle 4, stage 1, 20:3xZ 09-29) from input B3. Hypothesis: node-search-lives-beside-node-writer.
<!-- THOUGHT:END -->
