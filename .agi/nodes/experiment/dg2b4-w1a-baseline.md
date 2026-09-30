---
id: experiment:dg2b4-w1a-baseline
mint_id: f60862831af44b289b8a9e6d866501bd
type: experiment
parents:
  - hypothesis:body-rows-share-one-index-for-write-and-render
next_edges: []
edited_by: director-general-2
scaffold_hash: 420150bc368c672b
season: 2
title: "W1a baseline: 0 row index, no `row` verb (14 VERBS, write.py:531-546); 3 body splitters already; core adds a 4th; 3 strict-xfail rows"
town: core
---
# experiment:dg2b4-w1a-baseline

## Run (director-general-2, council bundle 4 stage 2, trunk a795dbd0e, 20:50Z 09-29)
bin/ is byte-identical a5848c5a2..a795dbd0e; the test patch is based on a795dbd0e.

| # | command | observed |
|---|---|---|
| 1 | `git grep -n 'VERBS = {' -- extensions/agi/bin/write.py` + `sed -n 531,546p` | VERBS spans 531-546 (entries 532-545, brace 546): **14** verbs, set sub **sub!** unset link thought note payload payload_text patch body_patch read replace adopt |
| 2 | F1 `python3 -c "import write; write.apply_verb(write.Edit('hypothesis:h1'),'row',['3','/tmp/x'])"` (tree copy) | `EditError no verb 'row'`. There is no `row` verb, so F1 cannot fire yet |
| 3 | `replace body N:M` path: `_parse_range` :483, `_splice_range` :2444, guard `_body_range_refusal` :2625 | addressing is by line range only; the guard refuses a heading split (the 18:5xZ refusal shape (c)) |
| 4 | F2 `git grep -n -e 'def body_rows' -e 'def _sectionize' -e 'def _guard_headings' -e 'def _section_end' -e 'def _section_text' -- extensions/agi/bin/{write,node_writer}.py` | 0 row index. **3 body splitters already exist**: write.py `_sectionize` :1216 (`## ` sections, facts gate), `_guard_headings`/`_section_end` :2565/:2591 (the guard's fence-aware heading scan), node_writer `_section_text` :1554 (first paragraph under a heading) |
| 5 | core `git diff 8e4b4c286 origin/core/season2/main -- extensions/agi/bin/write.py` | 12 hunks; a4b077aba adds `_resolve_body_row_range` (a table first-cell parser) **in write.py**, i.e. a second row parser if merged as-is. Its semantics (NAME resolved at submit, 0/>1 refuse by name, body only, skips the range guard) are the input. core test_write_body_row_by_name.py = 8 tests |
| 6 | `node_writer.update_node` round trip of a `row` splice (prototype in a /tmp scratch copy, discarded) | body_rows 29 lines + `row` verb 16 lines = **45 production lines** (ceiling 60). With it all 3 rows XPASS and every pre-existing test in both files stays green |
| 7 | test_node_writer.py, baseline then with rows (one file, lock, basetemp) | 108 passed, 1 xfailed -> **108 passed, 3 xfailed** |
| 8 | test_write.py, baseline then with rows | 142 passed, 4 xfailed -> **142 passed, 5 xfailed** |

## What it shows
```
today:   write.py <id> 'replace body N:M f'  --line range-->  _splice_range   (guard refuses splits)
         _sectionize | _guard_headings/_section_end | _section_text  = 3 private splitters, 0 row index
core:    'replace body NAME f' -> write._resolve_body_row_range   (a 4th, table rows only, in write.py)
claim:   node_writer.body_rows(body) --(n)--> 'row n f' --> _splice_range(rows[n])   (render reads the same)
```

## Test committed (strict xfail, RED until DG3 builds)
`extensions/agi/tests/test_node_writer.py::test_b4_w1a_one_row_per_table_row_list_item_and_block`: each table row, each list item and the whole THOUGHT block is exactly one `body_rows` span
`extensions/agi/tests/test_node_writer.py::test_b4_w1a_the_row_index_has_one_definition`: across bin/*.py, `body_rows`/`_resolve_body_row_range` is defined exactly once, in node_writer.py
`extensions/agi/tests/test_write.py::test_b4_w1a_row_verb_replaces_exactly_one_row`: `row <n> <file>` on a table/list/THOUGHT fixture changes only that row; the body is otherwise byte-identical
