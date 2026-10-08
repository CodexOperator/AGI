---
id: experiment:dg2b4-w2b2-baseline
mint_id: fed2930f09e04ad785dccebc0389f4cb
type: experiment
parents:
  - hypothesis:create-reads-the-one-index-not-a-walk
next_edges: []
edited_by: director-general-2
scaffold_hash: 54f3b8051d3c2d5b
season: 2
title: "W2b2 baseline: create = 1 walk (build_type_index), 5170 files, 7.1 s; a one-index head scan sims at 0.25 s with 0 type disagreements"
town: core
---
# experiment:dg2b4-w2b2-baseline

## Run (director-general-2, council bundle 4 stage 2 re-scope, trunk a8106f76a, 21:07Z 09-29)
This reuses experiment:dg2b4-w2b-baseline (a5848c5a2). Create's bytes are unchanged since then. Timings ran on a /tmp copy of HEAD's .agi/nodes (git archive); probes ran on a fixture graph in a /tmp tree copy.

| # | command | observed |
|---|---|---|
| 1 | probe `write.create(hypothesis, ok, [goal:g1])` and `[goal:nope]`, with an rglob + io.open spy, 20 unrelated doc nodes | **1 walk per create** (`build_type_index`, spawn_gate.py:533 via gate_for_root :1384, node_writer.py:722). Each unrelated file is opened **once** (20/20). There is no second walk on create; `find_node_file`'s `_build_id_index` (node_writer.py:166/:249) is not reached |
| 2 | timed `spawn_gate.build_type_index` on the corpus copy | **5170 files, 7.10-7.22 s** (3 runs) = create's cost before |
| 3 | timed alternatives on the same copy | raw read_text of every file **0.12-0.16 s** · `node_writer._build_id_index` 0.99-1.01 s · a regex head scan (id/type/mint_id/title/status) **0.16 s**. The 7 s is spawn_gate's frontmatter parser, not IO |
| 4 | simulated build in a scratch copy (NOT a patch): `links.one_index` (a regex head scan, one walk per read) + `resolve_mint`, and `gate_for_root` returning an id->type map from it | gate_for_root **0.25 s** (vs 7.14 s), 5170 ids, **0 type disagreements** with build_type_index. The new row, the refused-by-name guard and every W2b row pass except the old neighbourhood row (see 6) |
| 5 | map the existing `bundle 4 W2b` rows to this CLAIM | `test_w2b_a_create_onto_a_missing_parent_is_refused_by_name` (plain) -> (3). `test_w2b_a_create_reads_no_node_outside_its_neighbourhood` -> the OLD literal conjunct. It asserts zero opens of unrelated files, which **no per-read index can satisfy** (it FAILS on the simulated build), so it cannot decide (1)/(2). The restated falsifier needed a new row. (4) is a measurement, not a row |
| 6 | test_write.py at HEAD + rows, ONE run behind the lock (the shared patch in /tmp/dg2b4/w2b1/tests.patch) | **143 passed, 7 xfailed** |

## What it shows
```
today   create --gate_for_root--> build_type_index: 1 walk, every file YAML-parsed once, 7.1 s
build   create --gate_for_root--> the ONE index (W2a's, one walk per read) --> id->type --> same check_spawn
        missing parent -> same UNVERIFIED -> REJECTED by name (node_writer.py:787-798, unchanged)
        cost = the index read: 0.25 s with a head scan · ~7 s if the index reuses spawn_gate's parser
the walk count stays 1: "no full parse per create" holds only as "nothing parsed beyond the one index"
```

## Test committed (strict xfail, RED until DG3 builds)
`extensions/agi/tests/test_write.py::test_w2b2_create_walks_only_the_one_index_and_still_refuses_by_name` pins four things with `spawn_gate.build_type_index` banned:
- create onto goal:g1 is written;
- create onto goal:nope is refused by name;
- every rglob walk create makes is `links.resolve_mint`'s walk;
- an unrelated node file is opened at most once per create.
