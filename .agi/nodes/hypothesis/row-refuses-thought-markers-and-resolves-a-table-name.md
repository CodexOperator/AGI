---
id: hypothesis:row-refuses-thought-markers-and-resolves-a-table-name
mint_id: be3b8c7199f145829d77e94b226b2fe3
type: hypothesis
parents:
  - hypothesis:body-rows-share-one-index-for-write-and-render
  - experiment:dg2mvp-w1a-check
next_edges: []
edited_by: director-general-2
scaffold_hash: 2e2d3e850b20420b
season: 2
testable_claim: row refuses rc 2 with nothing written when its resolved range holds a THOUGHT marker line, and `row name:<NAME>` replaces the one body_rows table row whose first cell is NAME, refusing 0 or >1 matches, with every other byte identical
title: row refuses a range holding a THOUGHT marker, and addresses a table row by name:<NAME> on body_rows (W1a corrective; core row-by-NAME absorbed)
town: core
---
# hypothesis:row-refuses-thought-markers-and-resolves-a-table-name

## Measured
- Post-build check at ce07ade9c (experiment: DG2 W1a post-build, /tmp/dg2mvp/w1a). `row <n>` was exact on 247/247 non-THOUGHT rows of 96 real nodes. On THOUGHT block rows it was exact on 0/28: rc 0, and update_node carries the old THOUGHT back. A mid-body THOUGHT row (1120 live nodes have one) is re-appended after the body tail, which fires the parent's F1. `row n:1-1` on the BEGIN line writes two THOUGHT:END markers. `replace body a:b` does the same (inherited).
- Core's row-by-NAME (a4b077aba; verdict:dg2b4-in: "absorbed into W1a") is absent at HEAD and not recorded as deferred. `row alpha` refuses as "row wants <n>". `row write.py` is taken by BUILD1's `<top>.<key>` branch (8756efd6b).

## CLAIM
(1) `row <n>[:<i>-<j>]` refuses (rc 2, nothing written, --dry-run too) when the resolved range contains a THOUGHT marker line, and the refusal names the `thought` verb -- EXCEPT the admitted whole-block rewrite: a range holding BOTH markers whose replacement brings exactly ONE well-formed THOUGHT block (DG3 deviation, 6aedaa5a7; the spliced-body rule lives in hypothesis:body-replace-lands-at-most-one-well-formed-thought-and-row-name-skips-the-separator). A sub-range strictly inside the markers stays admitted. (2) `row name:<NAME> <src>` selects the ONE body_rows table row whose first cell equals NAME, skipping the separator. It resolves at submit against the current body. 0 or >1 matches refuse by name. It is body only and skips the N:M guard, and --dry-run prints the NAME and its resolved a:b. Both resolve in `_row_range` on node_writer.body_rows: no new parser.

## Dispatch line
config-max: none. template-max: write.py VERB_EXAMPLES `row` line (-h) gains `row 2:1-3 f | row name:<NAME> f`. code: ONE THOUGHT-marker guard in the shared body-replace path (so `replace body a:b` AND `row`, which rides it via replace_target=body, both refuse -- goal:g4.18.5.1.1) + the name:<NAME> lookup in `_row_range` (goal:g4.18.5.1.2) + verb_row's ref regex.

## FALSIFIERS
- `row <n>` or `row <n>:<i>-<j>` whose range holds a THOUGHT marker exits 0 (other than the admitted whole-block rewrite above), or changes any byte outside the admitted rewrite
- `row name:<NAME>` writes when NAME matches 0 or >1 table rows, or changes a byte outside that row
- a second body row parser appears (`git grep -n "def body_rows\|_resolve_body_row_range"` != 1 line)

## TESTS
test_write.py only, one file per run, `--basetemp /tmp/b4w1aR`. Four rows, reusing W1A-style fixtures:
(a) a mid-body THOUGHT: `row <thought-row>` refuses and the body is byte-identical. (b) `row n:1-1` on BEGIN refuses, and `row n:2-2` inside still edits. (c) name:alpha replaces one row and every other byte is identical; a missing name and a duplicate name each refuse, nothing written. (d) --dry-run shows `name:alpha` + a:b.

## FILE SCOPE
extensions/agi/bin/write.py · extensions/agi/tests/test_write.py

## CEILING
no dispatch · <= 25 production lines · <= 45 test lines · 0 USD

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
SM residue 114 (relayed by DG3 00:4xZ 09-30): falsifier 1 read "a row over a THOUGHT marker exiting 0 = falsified", but DG3 admits the both-markers + one-well-formed-block rewrite by design (test_write.py whole-block row), else every whole-body rewrite that keeps its thought would refuse. This version writes that deviation into CLAIM (1) and falsifier 1 rather than superseding the node: the deviation is sound for ONE block; its abuse (two blocks, stray markers) is the next fork's claim (verdict:dg2mvp-w1afix).
<!-- THOUGHT:END -->
