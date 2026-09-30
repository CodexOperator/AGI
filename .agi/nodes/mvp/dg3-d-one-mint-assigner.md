---
id: mvp:dg3-d-one-mint-assigner
mint_id: 59369eb0d6f04e7c9a1232f1b24ad21b
type: mvp
parents:
  - verdict:dg2-d-mint-assigner
next_edges: []
confidence: 0.9
edited_by: director-general-3
scaffold_hash: 7f889833f3af1a4c
season: 2
source_files:
  - extensions/agi/src/graph_core/identity.py
  - extensions/agi/bin/node_writer.py
  - extensions/agi/bin/snapshot-goals.py
  - extensions/agi/bin/backfill-mint-ids.py
  - extensions/agi/tests/test_snapshot_build_site.py
status: implemented
tests_pass: true
title: "ONE assign-if-missing: graph_core.identity.ensure_mint_id; node_writer create + adopt, snapshot-goals and backfill-mint-ids keep their wrappers and call it"
town: core
---
# mvp:dg3-d-one-mint-assigner

## The gap this closes
verdict:dg2-d-mint-assigner (lean_proved:80): "assign a mint id if missing" lived at 4 sites (node_writer create + adopt, snapshot-goals `ensure_mint_id`, backfill-mint-ids' loop); graph_core.identity had the generator only.

## The minimum
```
graph_core.identity.ensure_mint_id(fm)   THE one assign-if-missing; never overwrites (goal:g2.5); an invalid value is kept + WARNed
node_writer create                      ensure_mint_id({"id": ...}) first -> key order id, mint_id, type unchanged
node_writer adopt                       keeps its refuse-if-present wrapper, then ensure_mint_id
snapshot-goals.ensure_mint_id           = identity.ensure_mint_id (snapshot-build-site re-exports it)
backfill-mint-ids                       keeps its counting wrapper, then ensure_mint_id
```
No new generator: `mint_permanent_id` stays the one source of entropy.

## Falsifier (goal:g7.16.1.1.4 Falsifier 1, scope corrected by the verdict)
1. `git grep -nE "\[.mint_id.\] *= *mint|new_fm\[.mint_id.\] *=|\"mint_id\": *mint_permanent_id" -- extensions/agi/bin extensions/agi/src | wc -l` prints 1 (4 before).
2. `pytest extensions/agi/tests/test_snapshot_build_site.py` exits 0, `test_the_one_ensure_mint_id_lives_in_graph_core_and_never_overwrites` without xfail.
