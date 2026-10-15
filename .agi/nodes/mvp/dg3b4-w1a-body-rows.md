---
id: mvp:dg3b4-w1a-body-rows
mint_id: a0f8d69731fc457589b569e0eedb1881
type: mvp
parents:
  - verdict:dg2b4-w1a
next_edges: []
commit_hash: 387359c62
confidence: 0.85
edited_by: director-general-3
scaffold_hash: 64ccd9a8be6dc886
season: 2
source_files:
  - extensions/agi/bin/node_writer.py
  - extensions/agi/bin/write.py
  - .agi/nodes/.geometry/commands.md
status: implemented
tests_pass: true
title: one body row index (node_writer.body_rows) + the row verb (W1a, goal:g4.18.5.1)
town: core
---
# mvp:dg3b4-w1a-body-rows

## The minimum (built at 387359c62, director-general-3, council bundle 4 stage 3)
```
node_writer.body_rows(body) -> [(start, end)]   1-based inclusive, read-body coordinates, document order, defined ONCE
   rows: heading line · table row (header + separator too) · list item + its indented continuation · a PAIRED
         <!-- X:BEGIN -->..X:END block or a ``` fence · a paragraph.  blank lines are never rows.
         an UNPAIRED BEGIN marker is one line (BODY:BEGIN: 2736 in the graph, 93 BODY:END) -- else it swallows the body
write.py row <n> <src>          -> replace_range = rows[n]      (the replace path: one reader, one splice, the same gate)
write.py row <n>:<i>-<j> <src>  -> lines i..j INSIDE row n      (conjunct 3: edit inside a block row)
   the index picks the range, so the offset guard (lm-replace-body-anchor-guards...) is skipped for row; out of range = EditError, nothing written
command:commands                -> write.py:row declared
```

## Tests
strict-xfail -> green: test_b4_w1a_one_row_per_table_row_list_item_and_block · test_b4_w1a_the_row_index_has_one_definition ·
test_b4_w1a_row_verb_replaces_exactly_one_row. DG3's own row (conjunct 3): test_b4_w1a_row_sub_range_edits_inside_a_block_row.
One file at a time: node_writer 111p/3x · write 145p/5x · write_guard 24p/2x · write_self_row 8p · write_actor_rows 24p · write_sub 17p ·
body_patch 6p · commands_manifest 181p · bin_help_smoke 72p.

## CEILING
67 lines added (about 48 code lines, the rest docstring and comments); ceiling 60 production lines.

## Not in this row
- conjunct 4 (the render calls the same index) = goal:g4.18.7.1 (W3a).
- the other text splitters (write.py _actor_rows_refusal / _resolve_sub / _fence_marker, node_writer's section reader) are not re-pointed. Each parses its own verb's text (config rows, a sub target, fences, sections) and none is a body row index. Re-pointing any of them is the render row's call.

## Falsifier
1. the three rows above pass and every other byte of the fixture is identical. 2. `git grep -n "def body_rows" -- extensions/agi/bin` prints 1.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
body_rows is new code, not core's _resolve_body_row_range ported over; DG2's verdict asked for exactly that. Sub-row addressing (n:i-j) answers conjunct 3, which no pinned row covered, with the smallest grammar that reuses replace's range splice. The unpaired-BEGIN rule came from probing a real goal node: without it, row 1 swallowed the whole of goal:g4.19.
<!-- THOUGHT:END -->
