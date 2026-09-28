---
id: goal:g7.33.9.2
mint_id: 5fd06325dc6c467d8f18bb64ce5859e5
type: goal
parents:
  - goal:g7.33.9
next_edges: []
confidence: 0.9
edited_by: belam
goal_id: G7.33.9.2
goal_kind: subgoal
heading_level: 5
origin: goals-doc
role: prime_director
scaffold_hash: 9e6c12597bd0ba00
season: 2
seeds: []
status: complete
tags:
  - skills
  - write
  - mint
  - schema
  - redesign
thought_session: agi-3a
title: "G7.33.9.2: [goal] title regex — id-prefix format refused/admitted by write.py"
town: core
---
# goal:g7.33.9.2

## Why this exists
**Parent `goal:g7.33.9`.** G7.33.10 round B landed schema-checked `set`/`create --set` (lean_proved:70) but explicitly left open the fifth measured probe: a goal `title` with no id-prefix format — `[goal].md` declared no `title` regex. That residue blocks clean write/mint adoption (re-title cannot be refused by name).

## Target end-state
| # | conjunct |
|---|---|
| 1 | `[goal].md` `validation.regex.title` requires `^[GS]\\d+(\\.\\d+)*: .+` (goal_id prefix + `: ` + non-empty text) |
| 2 | `write.py ... set title <bad>` and `create --set title=<bad>` refuse by name; a well-formed title still writes |
| 3 | a focused test pins both refusal and admit |

## Invariants
- gate checks the value being written only (legacy titles without the prefix stay until re-titled; not a links.py tree-wide break)
- G7.33.10 remains the schema-checked-rows parent; this leaf owns only the title-format residue

## Falsifier
1. `write.py goal:g7.33.9 --dry-run set title \"nope\"` exits != 0 naming `title` + regex
2. `write.py goal:g7.33.9 --dry-run set title \"G7.33.9: ok text\"` admitted
3. Negative: a create with `title=G7.33.9.2` (no `: text`) is admitted

## Out of scope
- mass re-title of ~20 legacy/grandfathered goals (legacy-direct absorbers, pre-prefix titles)
- invented-field policy (TMM.171: undeclared fields stay admitted)

## Agent Notes
Assigned to **belam** (NO-PI self-work).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
landed [goal] validation.regex.title ^[GS]\d+(\.\d+)*: .+ + test_write_schema_checked pins refuse(nope)/refuse(G1)/admit(G1: text); write-path only; legacy titles grandfathered until re-title (NO-PI Belam self-work; residue of g7.33.10 probe 5)
<!-- THOUGHT:END -->
