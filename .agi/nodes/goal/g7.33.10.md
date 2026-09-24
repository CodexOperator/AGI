---
id: goal:g7.33.10
mint_id: 734c1936e27f46e89c085dde54452fb9
type: goal
parents:
  - goal:g7.33
next_edges: []
confidence: 0.9
edited_by: thought-master
goal_id: G7.33.10
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: 6a295cf662c54245
season: 2
seeds: []
status: active
tags:
  - local-maxxing
  - engine
  - write
title: "G7.33.10: SCHEMA-CHECKED ROWS -- write.py writes one named row of a node, and the node type's schema decides whether that row exists and whether its value is well-formed"
town: core
---
# goal:g7.33.10

| | |
|---|---|
| goal | write.py writes ONE named row of a node -- a frontmatter field or a schema-declared body row -- and the node type's schema decides both whether that row exists and whether the value's format is valid: no verb can invent a row |
| origin | the owner 17:57Z 09-24 (verbatim on town:local-maxxing's board) · enables clean re-titling of goals and clean node body modifications |
| measured | 18:0xZ 09-24, real writes in a scratch worktree: `set` on goal:g7.33.9 admitted all five of an invented field (invented_row), goal_id X9 (fails [goal]'s regex), status bogus (fails its regex), confidence notafloat (fails its types) and a title with no id prefix (no rule declared) -- exit 0 each; write.py consults no schema on edit |
| scope | every node type with a schema under .agi/context/schemas/ · frontmatter fields, list rows, and body rows the schema declares · checks the row being written, never blocks on an unrelated legacy violation (links.py schema lists those) · NOT create (the spawn gate already runs there) |
| done | the five probes above each refused (exit != 0, one line naming the row and the rule) · a valid goal re-title = ONE verb, and snapshot-goals.py --render --check still exits 0 · a body row replaced by its name, never by line numbers · [goal] declares the title format (<goal_id>: <text>) · tests pin all of it |
| who | director-engine, batched by thought-master (TMM.128) |

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
gen 17: the duplicated heading from the mint removed (write.py create adds its own heading; the body file carried a second one)
<!-- THOUGHT:END -->
