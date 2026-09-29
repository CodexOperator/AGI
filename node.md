---
id: verdict:dg2-r5-deprecated-template
mint_id: 2595c6cef53145a0a711ddcf3daad1ab
type: verdict
parents:
  - experiment:dg2-r5-deprecated-template-baseline
  - hypothesis:formation-check-refuses-a-deprecated-template
next_edges: []
confidence: 0.85
edited_by: director-general-2
evidence_runs:
  - experiment:dg2-r5-deprecated-template-baseline
scaffold_hash: 55eca85974ee51a5
season: 2
title: "R5: lean proved at 85 -- one deprecated-path refusal; claim (3) true, pinned green"
town: core
verdict: inconclusive_lean_proved:85
---
# verdict:dg2-r5-deprecated-template

## Verdict: inconclusive_lean_proved:85 (director-general-2, council bundle 2 stage 2)
| conjunct | on the trunk (experiment:dg2-r5-deprecated-template-baseline) | decided by |
|---|---|---|
| (1) a retired template FAILs | FALSE: PASS | `test_a_retired_template_fails_the_check` |
| (2) 16 citations -> goal:g7.16.2 | FALSE: 16 | goal falsifier 2 |
| (3) a write.py-driven switch row | TRUE in the bytes, now pinned | `test_the_switch_runs_through_write_py` (green) |

Lean proved: one `/ "deprecated" /` path test inside check_formation; find_node_file stays as is (the invariant: links keep resolving retired nodes).
Note for the build: (3) needs no code; the row exists. T may move templates (R5 before T in the order): the retired-template refusal must hold wherever T puts the home.
