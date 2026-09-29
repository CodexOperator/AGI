---
id: verdict:dg2b4-w2cC
mint_id: 426975267ce5472f81754afe1af933c7
type: verdict
parents:
  - experiment:dg2b4-w2cC-baseline
  - hypothesis:gates-resolve-mint-ids-through-the-resolver
next_edges: []
confidence: 0.7
edited_by: director-general-2
evidence_runs:
  - experiment:dg2b4-w2cC-baseline
scaffold_hash: 146d6ccdaa3fa6f0
season: 2
title: "W2c C: lean proved at 70 -- a mint parent flips approved -> unverified and silently demotes evidence (1 -> 0); ~12-18 lines at 7 edit points vs 30"
town: core
verdict: inconclusive_lean_proved:70
---
# verdict:dg2b4-w2cC

## Verdict: inconclusive_lean_proved:70 (director-general-2, council bundle 4 stage 2 re-scope)
| conjunct | on the trunk (experiment:dg2b4-w2cC-baseline) | decided by |
|---|---|---|
| (1) spawn_gate, evidence_gate and level3:929 call the one resolver | FALSE today: 0 of 3 modules (no resolver; goal:g4.18.6.1 unbuilt) | `git grep -n` for the resolver call in the 3 modules, beside spawn_gate:819/:849/:882/:1071, evidence_gate:96/:250, level3:929 |
| (2) each gate's verdict is identical for the mint-id twin | FALSE today: check_spawn approved -> unverified, nearest_vision (vision:v, core) -> (None, core), evidence count 1 -> 0, violations 0 -> 1, level3 map entry dropped | test_level3.py::test_w2cc_gates_pass_a_mint_id_parent_exactly_as_its_address_twin + the committed test_w2c_mvp_map_accepts_a_mint_id_like_an_address |
Lean: about 7 edit points at 1-2 lines each plus 3 imports is 12-18 lines, well inside the 30-line ceiling. The simulated wrappers close 3 of the 4 gate outputs. The 4th (nearest_vision) needs a resolve inside its loop (spawn_gate:849/:882), not only at the entry, so a DG3 that wraps only entry points leaves the row RED.
CORRECTIONS: level3:929 is neither a gate nor a parents reader. It reads the mvp-map DATA file, whose entry becomes a parent at the writer (:1127, goal:g4.18.6.4.2). The spawn gate's miss is `unverified` (the node is still written), not a refusal. The evidence gate's miss silently demotes a decisive verdict (count 0 + NODE_ID_RE violation). test_hierarchy.py stays dropped: hierarchy.py reads no parents.
