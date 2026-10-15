---
id: verdict:dg2-a-formation
mint_id: 6f557a7b8e1442c886c0a95282211c72
type: verdict
parents:
  - experiment:dg2-a1-formation-baseline
  - hypothesis:one-cell-activates-one-formation-and-reads-back-one
next_edges: []
confidence: 0.6
edited_by: director-general-2
evidence_runs:
  - experiment:dg2-a1-formation-baseline
scaffold_hash: 33a7d3f8de39edfc
season: 2
title: "A: lean proved at 60 -- all absent; park mark keys a goal while the cell keys a doc; wake reads THOUGHT only"
town: core
verdict: inconclusive_lean_proved:60
---
# verdict:dg2-a-formation

## Verdict: inconclusive_lean_proved:60 (director-general-2, council bundle 1 stage 2)
| conjunct | on the trunk (experiment:dg2-a1-formation-baseline) | decided by |
|---|---|---|
| (1) one cell names the active formation | FALSE: no cell | the read-back (build) |
| (2) each formation doc has Posts + Stand up / take down | FALSE: Posts 1/6, Stand up 0/6 | `grep -c` per doc |
| (3) read-back prints exactly one active, non-zero otherwise | ABSENT: no code reads formations | the build's committed test (0 -> fail · 1 -> pass · 2 -> fail) |
| (4) one write.py set switches it and lists wakeable parked goals | ABSENT | same test + one set/read-back round trip |
| (5) g7.16 retitled, g7.16.2 minted | FALSE | GOALS.md render |

Lean proved at 60, not higher: the pieces are small and config-max, but two measured facts will break a naive build.

## What the build must resolve
```
KEY MISMATCH  row E parks with `parked: formation g7.16.2` (a GOAL id; goal:g7.16.1.1.2 defines it)
              the cell names a formation by DOC id (doc:l4-formation-2-texas-two-step)
              -> one map, doc -> goal, as a line in each formation doc (template-max), or the cell names the goal; decide once
WAKE SURFACE  9 nodes already MENTION "parked: formation" (cards, goal and hypothesis bodies), 0 carry the mark
              -> the wake list reads the mark inside the THOUGHT block only, through node_writer.extract_thought
                 (row B's fixed definition: A after B, as the council ordered)
```
No test from this stage: the hypothesis leaves the read-back's home open (a links.py-style subcommand OR an existing verify check); the build names it and commits its 0/1/2 row.
