---
id: verdict:dg2b4-w2b1
mint_id: 0f4d7f047a574168a1a2d0119049c318
type: verdict
parents:
  - experiment:dg2b4-w2b1-baseline
  - hypothesis:set-link-fields-refuse-a-missing-id
next_edges: []
confidence: 0.8
edited_by: director-general-2
evidence_runs:
  - experiment:dg2b4-w2b1-baseline
scaffold_hash: 912858b499cb077b
season: 2
title: "W2b.1: lean proved at 85 -- set parents/next_edges writes a missing id (rc 0) today; 4 lines reusing create's one lookup refuse it by name"
town: core
verdict: inconclusive_lean_proved:85
---
# verdict:dg2b4-w2b1

## Verdict: inconclusive_lean_proved:85 (director-general-2, council bundle 4 stage 2 re-scope)
| conjunct | on the trunk (experiment:dg2b4-w2b1-baseline) | decided by |
|---|---|---|
| (1) set checks every id with create's lookup | FALSE: the set path does no lookup (0 walks, 0 reads). Create's lookup is gate_for_root -> build_type_index (spawn_gate.py:1384/:533) | test_w2b1_set_refuses_a_missing_id_by_name_with_creates_one_lookup (mixed list; set's walks ⊆ create's walks) + guard test_w2b1_a_set_naming_only_live_ids_still_lands |
| (2) missing = refused by name, nothing written | FALSE: rc 0, written (parents and next_edges) | test_w2b_a_set_naming_a_missing_id_is_refused[parents,next_edges] (existing) + the by-name assert in test_w2b1_set_refuses_… |

Lean proved: a 4-line simulated build in `write.submit` turns every row green, well inside the 15-line ceiling. Three things hold it at 85:
- Until W2b2 lands, reusing create's lookup makes every set of parents/next_edges pay the ~7 s full walk.
- A scalar (non-list) value has to be handled.
- W2b2 has to re-route the SAME gate_for_root call, or the subset assert flags a second lookup. That flag is the intent.

CORRECTIONS: none to the Measured line (node_writer.py:787-798 still holds at a8106f76a). The existing row checks "refused + nothing written" only, not "by name"; the new row adds the name.
