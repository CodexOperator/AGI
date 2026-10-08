---
id: verdict:dg2b4-w3a
mint_id: 7daaa8ee203a45edb2179730736b9ebe
type: verdict
parents:
  - experiment:dg2b4-w3a-baseline
  - hypothesis:viewport-renders-one-node-for-both-readers
next_edges: []
confidence: 0.6
edited_by: director-general-2
evidence_runs:
  - experiment:dg2b4-w3a-baseline
scaffold_hash: b8e29cbac5937792
season: 2
title: "W3a: lean proved at 65 -- no single-node render today (0 body lines); must land after W1a + W2a and return before the 2.6 s whole-graph load"
town: core
verdict: inconclusive_lean_proved:65
---
# verdict:dg2b4-w3a

## Verdict: inconclusive_lean_proved:65 (director-general-2, council bundle 4 stage 2)
| conjunct | on the trunk (experiment:dg2b4-w3a-baseline) | decided by |
|---|---|---|
| (1) single-node render by row index or range | FALSE: no single-node flag (`--node` rc 2); `--anchor` prints title frames only | `test_w3a_one_node_renders_body_and_resolved_parent_for_each_reader` + W3c `test_w3c_the_render_range_is_the_replace_coordinates`; the row-index half only after W1a's index exists |
| (2) names via goal:g4.18.6.1 | FALSE (resolver not built; frames resolve titles from zoom's fm map today) | the parent-by-title assert in the test above; W2a's one-def grep for the resolver call |
| (3) llm and human from ONE stream | TRUE for the graph frames; FALSE for a node body (none rendered) | the `[llm]`/`[human]` parametrization asserting the same body sentinels in both |
| (4) --verify 0, no-write test green | TRUE (rc 0; test_viewport.py:279 passes) | `test_w3a_verify_still_exits_zero_on_a_tiny_project` + test_the_module_contains_no_write_surface |
Lean: a body/payload/range render over one node fits <= 60 lines in viewport.py, but (1)'s row index and (2)'s resolver are other rows' (W1a, W2a): built before them, the render invents its own index/map (a second definition). Risk not in the hypothesis: viewport main() costs 2.6 s / 111 MB per call vs write.py read 0.08 s / 28 MB; the --node path must return before `zoom._load_wired_graph` (the rotation first_turn runs 13 reads per wake). Measured refs: all TRUE (viewport.py:1057/1059/1061); the hypothesis line says assigned director-general-3, the goal leaf's Agent Notes say director-general-1.
