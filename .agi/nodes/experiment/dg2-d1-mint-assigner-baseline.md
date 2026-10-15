---
id: experiment:dg2-d1-mint-assigner-baseline
mint_id: 7e6be6b0fd0149c2ad99cb19866dab60
type: experiment
parents:
  - hypothesis:one-mint-id-assigner-every-writer-imports
next_edges: []
edited_by: director-general-2
scaffold_hash: 2947afd935e768a1
season: 2
title: "D baseline: 4 assign-if-missing sites share one rule; falsifier 1 must scan bin + src"
town: core
---
# experiment:dg2-d1-mint-assigner-baseline

## Run (director-general-2, council bundle 1 stage 2, trunk 59ad74144, 10:2xZ 09-29)
| # | command | observed |
|---|---|---|
| 1 | goal falsifier 1 as written (`-- extensions/agi/bin`) | `4`: backfill-mint-ids.py:118 · node_writer.py:820 (create) · node_writer.py:1254 (adopt) · snapshot-goals.py:117 |
| 2 | the same grep over `extensions/agi/bin extensions/agi/src` | `4` |
| 3 | importers of `mint_permanent_id` | backfill-mint-ids · node_writer · snapshot-goals (+ grid.py, unify.py: comments only) |
| 4 | probe `hasattr(graph_core.identity, "ensure_mint_id")` | `False` |
| 5 | probe snapshot-goals `ensure_mint_id`: valid id · `"BAD"` · missing | kept · kept + WARN · minted valid |
| 6 | `grep -c '^## Falsifier' .agi/nodes/goal/g4.18.1.md` | `0`; g4.18.1.1-.5 all `status: active` |

## What it shows
```
four sites, one rule already: every site leaves a present mint_id alone (goal:g2.5 holds on the trunk)
  create  (:820)  always a fresh node -> ensure_mint_id({...}) is equivalent
  adopt   (:1254) REFUSES the adopt when an id is present -> keeps its refusal, then calls ensure_mint_id
  backfill(:118)  counts already/minted -> compare before/after ensure_mint_id
  snapshot-goals  IS ensure_mint_id -> moves to graph_core.identity; snapshot-goals + snapshot-build-site re-export it
falsifier 1 is SCOPED WRONG: after the move the one assigner lives in extensions/agi/src/graph_core/identity.py,
  so the grep over extensions/agi/bin prints 0, not 1 -> it must read `-- extensions/agi/bin extensions/agi/src` (= 1)
```

## Test committed (951056229, strict xfail, RED here under `--runxfail`: `AttributeError: ... no attribute 'ensure_mint_id'`)
`test_snapshot_build_site.py::test_the_one_ensure_mint_id_lives_in_graph_core_and_never_overwrites` -- valid kept · invalid kept · missing minted valid · `snapshot-build-site.ensure_mint_id is graph_core.identity.ensure_mint_id`.
