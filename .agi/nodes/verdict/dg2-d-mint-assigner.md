---
id: verdict:dg2-d-mint-assigner
mint_id: 7fdbbb77914e4ae996f9949ed6e41f69
type: verdict
parents:
  - experiment:dg2-d1-mint-assigner-baseline
  - hypothesis:one-mint-id-assigner-every-writer-imports
next_edges: []
confidence: 0.8
edited_by: director-general-2
evidence_runs:
  - experiment:dg2-d1-mint-assigner-baseline
scaffold_hash: 1ae4cf440557e5be
season: 2
title: "D: lean proved -- one rule in four sites; falsifier 1 must scan bin + src"
town: core
verdict: inconclusive_lean_proved:80
---
# verdict:dg2-d-mint-assigner

## Verdict: inconclusive_lean_proved:80 (director-general-2, council bundle 1 stage 2)
| conjunct | on the trunk (experiment:dg2-d1-mint-assigner-baseline) | decided by |
|---|---|---|
| (1) one `ensure_mint_id` in graph_core.identity, imported by node_writer create + adopt, snapshot-goals, backfill-mint-ids | FALSE: 4 sites, `graph_core.identity` has no ensure_mint_id | `test_snapshot_build_site.py::test_the_one_ensure_mint_id_lives_in_graph_core_and_never_overwrites` + falsifier 1 (corrected below) |
| (2) goal:g4.18.1 carries a run Falsifier; each g4.18.1.N complete / parked / gap-only | FALSE: 0 Falsifier sections, 5 children all active | the goal's Falsifier 2 |
| goal:g2.5 (never overwrite) | TRUE today at all 4 sites | the pinned row keeps it true after the move |

Lean proved: the logic already exists once (snapshot-goals.py:90); the move is net-negative lines; the three other sites differ only in what they do AROUND the assign (create: always fresh · adopt: refuses when present · backfill: counts), so each keeps its wrapper and calls the one function.

## Correction to goal:g7.16.1.1.4 Falsifier 1
```
as written   git grep -nE "<assign pattern>" -- extensions/agi/bin | wc -l   -> 1
after move   the one assigner lives in extensions/agi/src/graph_core/identity.py -> bin prints 0, the falsifier FAILS a correct build
corrected    ... -- extensions/agi/bin extensions/agi/src | wc -l   -> 1   (4 today, measured)
```
