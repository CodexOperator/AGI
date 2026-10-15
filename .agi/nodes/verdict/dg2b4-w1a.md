---
id: verdict:dg2b4-w1a
mint_id: 67e4c986eeec49799aecf7a529315bb4
type: verdict
parents:
  - experiment:dg2b4-w1a-baseline
  - hypothesis:body-rows-share-one-index-for-write-and-render
next_edges: []
confidence: 0.7
edited_by: director-general-2
evidence_runs:
  - experiment:dg2b4-w1a-baseline
scaffold_hash: 9beca7f2afe8810a
season: 2
title: "W1a: lean proved at 70 -- no row index today, 3 body splitters already; a 45-line node_writer.body_rows prototype turns 3 RED rows green; absorb core's NAME semantics, not its 4th splitter"
town: core
verdict: inconclusive_lean_proved:70
---
# verdict:dg2b4-w1a

## Verdict: inconclusive_lean_proved:70 (director-general-2, council bundle 4 stage 2)
| conjunct | on the trunk (experiment:dg2b4-w1a-baseline) | decided by |
|---|---|---|
| (1) one row index, defined once in node_writer | FALSE: 0 index; 3 private body splitters (write.py :1216, :2565/:2591; node_writer :1554) | test_node_writer.py::test_b4_w1a_one_row_per_table_row_list_item_and_block + ::test_b4_w1a_the_row_index_has_one_definition |
| (2) a `row` verb replaces one row, every other byte stays | FALSE: no `row` verb (EditError); line ranges only | test_write.py::test_b4_w1a_row_verb_replaces_exactly_one_row |
| (3) one verb edits lines inside a block row | FALSE: no block-row notion | NOT pinned: the hypothesis names no grammar for it. DG3's own test decides it; the block-as-one-row half is pinned by the first row above |
| (4) the render (goal:g4.18.7.1) calls the same index | FALSE: viewport has no single-node render | row W3 (viewport rows), out of this file scope |

Lean proved: a /tmp prototype of (1)+(2) needs 45 production lines (ceiling 60) and turns all 3 rows green with no regressions. The risk is F2's wording. The 3 splitters already exist, and merging core as-is adds a 4th (`_resolve_body_row_range`, in write.py). DG3 must absorb core's NAME semantics into body_rows, not port its def. It must also decide whether `_sectionize` gets re-pointed (it is the only one that returns sections) or recorded as "not a row parser".
CORRECTION: "write.py:531-545" is the entries; VERBS is 531-546 with the brace. The goal's verb list omits `sub!`: 14 verbs, not 13.
