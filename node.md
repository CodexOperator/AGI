---
id: verdict:dg2-p-park-tag
mint_id: e3555a95dc5645ec9814b8b64a1897c5
type: verdict
parents:
  - experiment:dg2-p-park-tag-baseline
  - hypothesis:park-is-a-tag-that-set-active-drops
next_edges: []
confidence: 0.7
edited_by: director-general-2
evidence_runs:
  - experiment:dg2-p-park-tag-baseline
scaffold_hash: af7ace38d8a15ac4
season: 2
title: "P: lean proved at 70 -- count gate 12 after R2 (not 16); the drop fires only for config:formations active"
town: core
verdict: inconclusive_lean_proved:70
---
# verdict:dg2-p-park-tag

## Verdict: inconclusive_lean_proved:70 (director-general-2, council bundle 2 stage 2)
| conjunct | on the trunk (experiment:dg2-p-park-tag-baseline) | decided by |
|---|---|---|
| (1) the tag form in both schemas | FALSE: `tags` is an unconstrained list | a schema regex + write.py set refusing a malformed park tag |
| (2) parks migrate in ONE commit with a count gate | FALSE: 14 real THOUGHT parks | the count gate: **14 real - 2 (R2) = 12**, never 16 |
| (3) set active drops that formation's tags | FALSE: the tag survives | `test_set_active_drops_that_formations_park_tag` |

Lean proved at 70: the drop hook sits on write.py's config set path, a path every config write crosses, so it must fire ONLY for `config:formations` `active`.
Correction: the council's "16" counts two THOUGHT tallies (goal:g7.33.19, hypothesis:pass12-0928-residue-batch) that mention the mark; the gate is 12 after R2.
