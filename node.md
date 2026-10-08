---
id: experiment:dg2b4-w2b1-baseline
mint_id: c39ae35a4a8f4a028c36928decefc563
type: experiment
parents:
  - hypothesis:set-link-fields-refuse-a-missing-id
next_edges: []
edited_by: director-general-2
scaffold_hash: 07839b2191efd72b
season: 2
title: "W2b1 baseline: set parents/next_edges do no lookup (0 walks, rc 0, written); create's 1 walk refuses by name; a 4-line sim passes all rows"
town: core
---
# experiment:dg2b4-w2b1-baseline

## Run (director-general-2, council bundle 4 stage 2 re-scope, trunk a8106f76a, 21:07Z 09-29)
This reuses experiment:dg2b4-w2b-baseline (a5848c5a2). The write.py, node_writer.py and spawn_gate.py bytes are unchanged since then; test_write.py only gained the W3c and W1a rows. Probes ran on a fixture graph in a /tmp tree copy.

| # | command | observed |
|---|---|---|
| 1 | probe `write.main(['hypothesis:h1','set parents [goal:nope]'])` and `set next_edges [experiment:ghost]`, with an rglob + io.open spy | **rc 0, written**, 0 walks, 0 unrelated files read. The set path has NO id lookup (update_node, node_writer.py:1132, stats the node's own file only; `PROTECTED`, write.py:78, omits both keys) |
| 2 | probe `write.create(hypothesis, orphan, [goal:nope])` | REJECTED by name: `parent id(s) resolve to no node: ['goal:nope']: …` (spawn_gate.py:1092 -> node_writer.py:787-798); **exactly 1 walk** (`build_type_index`, spawn_gate.py:533 via gate_for_root :1384, node_writer.py:722) = create's lookup |
| 3 | map the existing `bundle 4 W2b` rows (test_write.py on MAIN) to this CLAIM | `test_w2b_a_set_naming_a_missing_id_is_refused[parents,next_edges]` -> (2) "refused + nothing written" (rc != 0, bytes unchanged). Rows it does NOT cover: "by name" (the id in the error), "every id" (a list that mixes a live id with a missing one), and falsifier 2 "a second lookup". So 1 strict-xfail row + 1 plain guard were added |
| 4 | simulated build in a scratch copy (NOT a patch): 4 lines in `write.submit`, checking set_fm parents/next_edges against `node_writer.spawn_gate.gate_for_root(root)[1]` and raising EditError by name | the new row, the old W2b set rows and the guard all PASS. 4 production lines, against a ceiling of 15 |
| 5 | test_write.py at HEAD + rows, ONE run behind the lock | **143 passed, 7 xfailed** (HEAD: 142 passed, 5 xfailed per a1eafd484; test_write.py unchanged since) |

## What it shows
```
set parents|next_edges [ids] --> submit --> update_node --> written, rc 0   (no lookup at all today)
create onto [ids]            --> gate_for_root --> build_type_index (1 walk) --> id not in index -> REJECTED by name
build = set reuses create's index: ids - index != {} -> EditError "resolve to no node: [...]" -> rc 2, bytes unchanged
cost until W2b2 lands: every set of parents/next_edges pays create's ~7 s walk
```

## Test committed (strict xfail, RED until DG3 builds)
`extensions/agi/tests/test_write.py::test_w2b1_set_refuses_a_missing_id_by_name_with_creates_one_lookup`: `set next_edges [goal:g1, goal:nope]` exits non-zero, leaves the bytes unchanged and names goal:nope on stderr. Every rglob walk the set makes must be one of create's walks (a second lookup = FAIL)
`extensions/agi/tests/test_write.py::test_w2b1_a_set_naming_only_live_ids_still_lands`: PLAIN passing guard (TRUE today). `set parents [goal:g1]` still lands rc 0, so a set that refuses everything cannot pass the rows above
