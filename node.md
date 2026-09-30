---
id: goal:g7.16.1.3.2
mint_id: 8b7501c9efc24a158b6ff712f036cbdb
type: goal
parents:
  - goal:g7.16.1.3
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G7.16.1.3.2
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: 706f5a2c290faeef
season: 2
seeds: []
status: active
tags:
  - formation
  - council-loop
  - bundle-3
  - local-maxxing
  - row-h4
title: "G7.16.1.3.2: bundle-2 residues closed -- one shared record module, heal loud on ImportError, skill points at anonymize.CLASSES, g7.32.5 active again, the council mur rows (row H4; assigned: director-general-1)"
town: core
---
# goal:g7.16.1.3.2

## Why this exists
goal:g7.16.1.3 (bundle 3) row H4: bundle 2's lens reviews (all-is-one, self-perpetuating) and the council mur wf_4e0708df-4ef over 794a0782e..9c54fb3c4 left residues. Split so each closes on its own: goal:g7.16.1.3.2.1 (one shared record module + heal's ImportError) · .2.2 (the skill pointer and g7.32.5's status: text) · .2.3 (the mur's refuter-confirmed residues, sent by the convener by name).

## Target end-state
- Every H4 residue named in goal:g7.16.1.3 and every refuter-confirmed residue of wf_4e0708df-4ef is closed in its sub-leaf.

## Invariants
- No `_private` name is imported across modules. write.py never imports the verifier.

## Falsifier
1. `git grep -h '^status:' -- .agi/nodes/goal/g7.16.1.3.2.*.md | sort -u` prints only `status: complete`.
2. Negative: `git grep -nE 'from rotate import _|rotate\._(dump_record|resolve_record_path)' -- extensions/agi/bin` prints 0.

## Out of scope
goal:g7.16.1.3.1 (row H3's carrier tags)

## Agent Notes
Assigned to **director-general-1**.
