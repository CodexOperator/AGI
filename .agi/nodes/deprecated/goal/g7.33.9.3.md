---
id: goal:g7.33.9.3
mint_id: 8437422093334e2bbee003a46d94c9e2
type: goal
parents:
  - goal:g7.33.9
next_edges: []
confidence: 0.9
edited_by: belam
goal_id: G7.33.9.3
goal_kind: subgoal
heading_level: 5
origin: goals-doc
role: prime_director
scaffold_hash: 906cf61e293d8ffa
season: 2
seeds: []
status: complete
tags:
  - write
  - mint
  - schema
  - redesign
thought_session: agi-3a
title: "G7.33.9.3: [goal] title regex — id-prefix format refused/admitted by write.py"
town: core
---
# goal:g7.33.9.3

## Why this exists
**Parent `goal:g7.33.9`.** G7.33.10 round B landed schema-checked `set`/`create --set` (lean_proved:70) but left open measured probe 5: a goal `title` with no id-prefix format — `[goal].md` declared no `title` regex. Parallel nest used G7.33.9.1/.2 for skills adoption + write/mint route; this leaf owns the title-format residue only.

## Target end-state
| # | conjunct |
|---|---|
| 1 | `[goal].md` `validation.regex.title` = `^[GS]\d+(\.\d+)*: .+` |
| 2 | `write.py set title <bad>` refuses by name; well-formed title admits |
| 3 | `test_write_schema_checked` pins refuse + admit |

## Invariants
- write-path only; ~20 legacy titles stay until re-titled
- does not re-own G7.33.10 invented-field policy (TMM.171 admit)

## Falsifier
1. `write.py goal:g7.33.9 --dry-run 'set title nope'` exits != 0 naming title+regex
2. `write.py goal:g7.33.9 --dry-run 'set title G7.33.9: ok'` admitted
3. Negative: `set title G7.33.9` (id only, no `: text`) admitted

## Out of scope
- mass re-title of legacy-direct / pre-prefix goals
- G7.33.9.1 skills adoption · G7.33.9.2 write/mint route

## Agent Notes
Assigned to **belam** (NO-PI self-work).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
landed [goal] title regex + tests; write-path only; NO-PI Belam
<!-- THOUGHT:END -->

<!-- THOUGHT: season3 rollover: complete goal not carried into s3; builds reparented to umbrella. -->
