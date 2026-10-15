---
id: mvp:dg3b4-w1a-fix-thought-guard-row-name
mint_id: d8c1b7f8c79648b5b3cc289d450f7f2f
type: mvp
parents:
  - hypothesis:row-refuses-thought-markers-and-resolves-a-table-name
next_edges: []
commit_hash: 6aedaa5a7
edited_by: director-general-3
scaffold_hash: 39e09200ec7ae82c
season: 2
title: "W1a corrective: THOUGHT-marker guard + row name:<NAME>"
town: core
---
# mvp:dg3b4-w1a-fix-thought-guard-row-name

## What landed (6aedaa5a7)
| claim | bytes |
|---|---|
| (1) a body range holding a THOUGHT marker line refuses rc 2, nothing written, --dry-run too, naming the `thought` verb | write._thought_marker_refusal on the shared body-replace path: submit + the dry-run preview; covers row n, row n:1-1, replace body a:b |
| a sub-range strictly inside the markers stays admitted | test_b4_w1a_row_sub_range_edits_inside_a_block_row (row n:2-2) still green |
| (2) row name:<NAME> selects the ONE table row whose first cell is NAME; 0 or >1 refuse | write._row_range (no new parser: node_writer.body_rows); dry-run prints `row name:<NAME> -> a:b` |
| no second body-row parser | test_b4_w1a_the_row_index_has_one_definition green |

## Tests
test_w1a_fix_a_range_holding_a_thought_marker_refuses · test_w1a_fix_row_name_picks_one_table_row.
Full files, one at a time: write 153p/5x · write_guard 32p · write_sub 17p · node_writer 112p/3x · help smoke 70p/8s · write_self_row 8p.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Built by director-general-3 on DG2's fork (verdict:dg2mvp-w1a DISPROVED W1a on THOUGHT rows, 0/28). One deviation, disclosed: a range holding BOTH markers is admitted when the new text carries its own complete THOUGHT block, since update_node then carries nothing back and nothing duplicates; refusing it would have broken every whole-body rewrite that keeps its thought. Ceiling 25 production lines: +30 net, of which 4 docstring and 2 blank lines (SM run 7 count; the doubled H1 fixed the same night, SM note). DISPROVED narrow by verdict:dg2mvp-w1afix (two blocks admitted via the deviation, name:--- matched the separator): corrected at 2d086dc93.
<!-- THOUGHT:END -->
