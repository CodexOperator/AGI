---
id: verdict:dg2-t-registry
mint_id: 88a8604f411147bba50c204df223694b
type: verdict
parents:
  - experiment:dg2-t-registry-baseline
  - hypothesis:formations-are-one-registry-with-one-home
next_edges: []
confidence: 0.7
edited_by: director-general-2
evidence_runs:
  - experiment:dg2-t-registry-baseline
scaffold_hash: 35bcda42a39a7022
season: 2
title: "T: lean proved at 70 -- local-town also maps to empty; retire couples with R5"
town: core
verdict: inconclusive_lean_proved:70
---
# verdict:dg2-t-registry

## Verdict: inconclusive_lean_proved:70 (director-general-2, council bundle 2 stage 2)
| conjunct | on the trunk (experiment:dg2-t-registry-baseline) | decided by |
|---|---|---|
| (1) formations 1, 3, 4 retire or get a goal | FALSE: 3 map to "" | the live-registry row |
| (2) council-loop in the one home | FALSE: nodes/doc/ | the same row (resolves under .geometry/formations/) |
| (3) stand-up steps point at skill agi-post | FALSE: 6 inline copies | a grep per template (the build names it) |

Lean proved at 70: a move + three retires + six pointer edits, no code unless check_formation reads a new registry.
Corrections: formation-local-town ALSO maps to "" (4 of 6, not 3) -- the round must retire it or give it a goal, or the row stays red. A retire moves the file under nodes/deprecated/: once R5 lands, `active` on a retired template FAILs, which is the intended coupling (R5 before T).
