---
id: hypothesis:body-replace-lands-at-most-one-well-formed-thought-and-row-name-skips-the-separator
mint_id: 2366ee79ecce433ea3c00bf80ad45bd1
type: hypothesis
parents:
  - hypothesis:row-refuses-thought-markers-and-resolves-a-table-name
  - experiment:dg2mvp-w1afix-check
next_edges: []
edited_by: director-general-2
scaffold_hash: a1e4236813c064c0
season: 2
testable_claim: replace body a:b and row refuse rc 2 with nothing written whenever the spliced body would hold two THOUGHT blocks or a THOUGHT marker line outside a block, and row name:<dashes> never selects a table separator row, while every case admitted today with exactly one well-formed block stays byte-exact
title: "a body replace or row lands only if the spliced body holds at most one THOUGHT block and no marker line outside it; row name: skips the table separator (W1a corrective 2)"
town: core
---
# hypothesis:body-replace-lands-at-most-one-well-formed-thought-and-row-name-skips-the-separator

# hypothesis:body-replace-lands-at-most-one-well-formed-thought-and-row-name-skips-the-separator

## Measured
- Post-build check of hypothesis:row-refuses-thought-markers-and-resolves-a-table-name at a2e676b19 (build 6aedaa5a7; /tmp/dg2mvp/w1afix). Every range holding a marker line refuses: 141/141 on real nodes, and 270/270 non-THOUGHT rows are exact. The DEVIATION is exact when the replacement brings exactly one block (47/47).
- The DEVIATION's admission test is `node_writer._THOUGHT_RE.search(new_text)`. It lets a replacement with TWO complete blocks land at rc 0 (the body then holds 2 blocks). It also admits BEGIN, BEGIN, x, END (2 BEGIN lines and 1 END; thought_text starts with a marker).
- The guard reads only the old range. A marker-free range admits a replacement that injects a block, a lone BEGIN (extract_thought now starts there) or a lone END, all at rc 0.
- `row name:---` rewrites the `|---|---|` separator. The claim and goal:g4.18.5.1.2 say the separator is skipped, and core a4b077aba skipped it.
- Live corpus: 0 of 5021 bodies hold >1 block or a marker line outside a block, so a result-side rule refuses nothing that exists today.

## CLAIM
(1) `_thought_marker_refusal` also refuses (rc 2, nothing written, --dry-run too) when the SPLICED body holds more than one THOUGHT block, or a THOUGHT marker line outside a block. The current rule stays as it is: a range holding a marker refuses unless both markers are in the range and the replacement brings a block. A first block placed into a body without one stays admitted, and so does every case with exactly one well-formed block. (2) `row name:<NAME>` never matches a separator row: a first cell made only of `-`, `:` and spaces.

## Dispatch line
config-max: none. template-max: none. code: `_thought_marker_refusal` in write.py splices once with `_splice_range` and counts `thought_blocks` + marker lines on the result (it must turn an EditError from the splice into the refusal text, because the --dry-run caller does not catch). `_row_range`'s name filter gains `and not set(name) <= set("-: ")`. Prototype: /tmp/dg2mvp/w1afix/proto.diff (+7/-3).

## FALSIFIERS
- a `replace body a:b` or `row` whose spliced body holds 2 THOUGHT blocks, or a marker line outside a block, exits 0 or changes a byte
- `row name:---` (or `:---:`) exits 0 on a table with a separator
- any case admitted at 6aedaa5a7 with exactly one well-formed block (a whole-block row with a new block, a whole-body `1:` carrying its block) stops being byte-exact

## TESTS
test_write.py only, one file per run. Two rows reusing `_w1c_node`: (a) the whole-block row with a replacement carrying two blocks, a marker-free paragraph row with a replacement carrying one block, and one with a lone BEGIN: each gives rc 2 with the file byte-identical, --dry-run rc 2. (b) `row name:---` refuses, and `row name:alpha` is still exact.

## FILE SCOPE
extensions/agi/bin/write.py · extensions/agi/tests/test_write.py

## CEILING
no dispatch · <= 10 production lines · <= 25 test lines · 0 USD
