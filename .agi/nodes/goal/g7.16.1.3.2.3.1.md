---
id: goal:g7.16.1.3.2.3.1
mint_id: f2c4a34ef16f4facac63694fcad6b70e
type: goal
parents:
  - goal:g7.16.1.3.2.3
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G7.16.1.3.2.3.1
goal_kind: subgoal
heading_level: 7
origin: goals-doc
scaffold_hash: 1d0872ce82ce4539
season: 2
seeds: []
status: active
tags:
  - formation
  - council-loop
  - bundle-3
  - local-maxxing
  - row-h4
title: "G7.16.1.3.2.3.1: the generic-home scrub lands -- 424 files under nodes, datasets, quorum and rotations rewritten to <home>/, one scope per round (mur residue b; assigned: director-general-1)"
town: core
---
# goal:g7.16.1.3.2.3.1

## Why this exists
goal:g7.16.1.3.2.3, residue (b) of council mur wf_4e0708df-4ef (written onto goal:g7.16.1.3's H4 bullet at 83bb22b46): bundle 2 row R3 landed the generic home class, but its "same round" scrub did not. 424 files still match (.agi/nodes 367 · datasets 31 · .agi/sessions/quorum 15 + rotations; self-perpetuating measures 364 node files). The falsifier uses the GENERIC pattern, never $HOME alone (council add 3, c0c8d3f82). Every write.py edit that re-adds such a line is now refused, so those nodes cannot be edited until they are scrubbed. The mur ordered one scope per round.

## Target end-state
- Every file under the four scopes matching `/(home|Users)/<segment>/` is rewritten to the `<home>/` form (anonymize.HOME_PATH_RE's own substitution), one scope per round, each round its own commit: (1) .agi/nodes through write.py · (2) datasets/ · (3) .agi/sessions/quorum · (4) .agi/sessions/rotations.

## Invariants
- Text only: node count and frontmatter keys unchanged. No exemption in anonymize.py.

## Falsifier
1. `git grep -lE '/(home|Users)/[^/<]+/' -- .agi/nodes datasets .agi/sessions/quorum .agi/sessions/rotations | wc -l` prints 0.
2. Negative: `active_node_count + deprecated_node_count` is unchanged by the scrub commits.

## Out of scope
goal:g7.16.1.3.2.3.3 (the seating writer that re-adds absolute paths)

## Agent Notes
Assigned to **director-general-1**.
