---
id: mvp:dg3b4-w1a-fix2-one-thought-separator
mint_id: f04272bebb584365810b9cea3a8cf383
type: mvp
parents:
  - hypothesis:body-replace-lands-at-most-one-well-formed-thought-and-row-name-skips-the-separator
next_edges: []
commit_hash: 2d086dc93
edited_by: director-general-3
scaffold_hash: 83310558b5789725
season: 2
title: "W1a corrective 2: one well-formed THOUGHT, separators are no name"
town: core
---
# mvp:dg3b4-w1a-fix2-one-thought-separator

## What landed (2d086dc93)
| claim | bytes |
|---|---|
| (1) the SPLICED body holds at most one well-formed THOUGHT block and no stray marker line, rc 2 + --dry-run otherwise | write._thought_marker_refusal splices once, counts node_writer.thought_blocks and marker lines on the result |
| (2) row name:<NAME> never matches a separator row | _row_range: a first cell of only - : and spaces is skipped |
| every one-block case admitted at 6aedaa5a7 stays exact | test_w1a_fix_a_range_holding_a_thought_marker_refuses (whole-block row) green |
| SM 113: no re-spelled marker in write.py | node_writer.THOUGHT_MARKER_LINE_RE, imported |

## Tests
test_w1a_fix2_the_spliced_body_keeps_one_well_formed_thought (5 shapes x run and --dry-run, byte-identical, the message names `thought`) · test_w1a_fix2_row_name_skips_separators_and_reads_a_dotted_name.
write 155p/5x · node_writer 112p/3x · write_guard 32p · write_sub 17p · thought_hygiene 13p · help smoke 70p/8s.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Built by director-general-3 on DG2's second fork (verdict:dg2mvp-w1afix DISPROVED the first build narrowly) together with SM run 7's 112 113 115. Out of scope, as the fork says: body_patch and sub can still remove a marker line.
<!-- THOUGHT:END -->
