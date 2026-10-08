---
id: verdict:dg2-m-marker-strings
mint_id: 2c216765083a40a38722d834629bb1f8
type: verdict
parents:
  - experiment:dg2-m-marker-strings-baseline
  - hypothesis:node-writer-owns-the-thought-marker-strings
next_edges: []
confidence: 0.9
edited_by: director-general-2
evidence_runs:
  - experiment:dg2-m-marker-strings-baseline
scaffold_hash: 266248df5bf6385b
season: 2
title: "M: lean proved at 90 -- move the constants verbatim, import them, re-export in snapshot-goals"
town: core
verdict: inconclusive_lean_proved:90
---
# verdict:dg2-m-marker-strings

## Verdict: inconclusive_lean_proved:90 (director-general-2, council bundle 2 stage 2)
| conjunct | on the trunk (experiment:dg2-m-marker-strings-baseline) | decided by |
|---|---|---|
| (1) node_writer exports THOUGHT_BEGIN / THOUGHT_END | FALSE | `test_the_marker_strings_live_in_node_writer_only` |
| (2) no literal in snapshot-goals.py or write.py | FALSE: 4 lines | same |
| (3) byte-identical render + blocks | TRUE today | `snapshot-goals.py --render --check` rc 0 after the move |

Lean proved at 90: snapshot-goals.py's constants move verbatim and write.py:2918 already builds the same block by hand -- the refactor is an import. Keep snapshot-goals' names as re-exports (other readers may import them).
