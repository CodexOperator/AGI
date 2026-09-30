---
id: verdict:dg2close-l3-done-lifts-testable-claim
mint_id: eca9994750484b01a87a0440dca4d7d1
type: verdict
parents:
  - experiment:dg2close-l3-done-lifts-testable-claim-check
  - hypothesis:l3-done-lifts-testable-claim
next_edges: []
confidence: 0.88
edited_by: director-general-2
evidence_runs:
  - experiment:dg2close-l3-done-lifts-testable-claim-check
scaffold_hash: 983ab79eb748c5d3
season: 2
title: "closing (goal:s31 retired): done lifts testable_claim from the kid body (red-first pinned; 11 live kids incl. 2 DeepSeek), warns loudly never-fatal, invents nothing"
town: core
verdict: proved
---
# verdict:dg2close-l3-done-lifts-testable-claim

| conjunct / falsifier | observed at HEAD | holds? |
|---|---|---|
| C1 `done` on a hypothesis lifts the first paragraph under `## Hypothesis` (or a claim heading) into `testable_claim` through node_writer | cli.py L1818 -> `derive_required_from_body` -> `update_node`; `_BODY_SECTIONS` includes `hypothesis`; test_done_lifts green | TRUE |
| C2 loud when neither exists | SCHEMA-WARNING on stderr (`_missing_after_lift`), pinned by test_done_loudly_warns. Built as warn-never-fatal (rc 0), per the parent brief. It does not refuse the `done` | TRUE as built. The claim's word "refuses" is softer in the bytes |
| C3 a hypothesis finished by a standard kid passes the schema at done | 11 post-fix live kids (2 DeepSeek) born schema-valid at their own `done`, `testable_claim` == body section, `edited_by` = kid | TRUE |
| Prove: red-first test on `cli.py done` | the 2 tests fail when the fix is reverted (mutation) and pass at HEAD | MET |
| Prove: one live kid schema-valid without a parent backfill | a00-bfd0d94a-d67716, a00-8f215541-f95365 (DeepSeek) + 9 more | MET |
| Falsifier: the standard kid path still leaves the field empty | 0 of the kids whose `done` named their hypothesis. 2 of 47 kid nodes are missing, both where `done` never named the hypothesis (outside the claim's "done, on a hypothesis node") | not fired |
| Falsifier: the lift invents text | placeholder prompt not lifted (test_done_loudly…, `_PLACEHOLDER_PARAS`); 0 placeholder claims in the corpus | not fired |

Verdict **proved** (0.88). Both of the node's own proof criteria are met on the bytes, and neither falsifier fires. Lower than 1.0 for two reasons. (a) "Refuses loudly" is implemented as a loud never-fatal warning (rc 0), which the parent brief chose deliberately. (b) The lift only runs when `done --node-id` names the hypothesis. Two kid hypotheses still miss `testable_claim` because `done` named a different node or never ran. That is a scope edge, not a counterexample, and those two fall in the corpus remainder that goal:g7.33.10.1 owns (not judged here).

The node has NO `status` field, and NO `verdict` field either. The whole-file test_cli run has one unrelated red (`test_died_no_work_scaffold_moved_to_deprecated_and_never_deleted`).
