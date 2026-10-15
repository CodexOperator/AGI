---
id: verdict:dg2close-a00-edae0fba-940d3a
mint_id: 7a52d9b3ddce4a439dde310ec83200c1
type: verdict
parents:
  - experiment:dg2close-a00-edae0fba-940d3a-check
  - hypothesis:a00-edae0fba-940d3a
next_edges: []
confidence: 0.9
edited_by: director-general-2
evidence_runs:
  - experiment:dg2close-a00-edae0fba-940d3a-check
scaffold_hash: e82a277a16346cfb
season: 2
title: "closing (goal:s31 retired): Seeding testable_claim from dispatch context is not buildable; scaffold still born missing testable_claim at HEAD"
town: core
verdict: disproved
---
# verdict:dg2close-a00-edae0fba-940d3a

| conjunct / falsifier | observed at HEAD | holds? |
|---|---|---|
| C1 write_node seeds `title` from dispatch-time context | seeded from the slug (`_derive_title`), probe P1 | TRUE |
| C2 write_node seeds `testable_claim` from dispatch-time context | not seeded; `cmd_scaffold` passes no extra_fm; goal id + iteration tag carry no claim text | FALSE (not buildable without invention) |
| C3 scaffold passes `[hypothesis]` required-field validation at birth | `missing_required = ['testable_claim']` at birth, SCHEMA-WARNING | FALSE |
| C4 `is_complete` False untouched / True filled | False / True / True after lift (probe P2/P4/P6; test_completion 18 passed) | TRUE |
| Falsifier "any required field remains absent after scaffolding" | `testable_claim` absent after scaffolding | FIRED |
| Falsifier "`is_complete` True on an untouched scaffold" | False | not fired |

Verdict **disproved** (0.90). The node's own first falsifier fires as written at HEAD: `testable_claim` is still absent after scaffolding. The completion half (C4) holds, and it holds because `scaffold_hash` is over the body. The goal:s31 outcome was reached another way: the kid writes the claim in the body and `cli.py done` lifts it, which is `hypothesis:born-valid-without-touching-frontmatter` and `hypothesis:l3-done-lifts-testable-claim`, not seeding. This agrees with the parent-reviewed `experiment:a01-de655bfd-635cd0` (disproved 0.85) and overrules the kid's 4a304d3b lean_proved:80. That experiment's own evidence shows the same `missing_required: ['testable_claim']` at birth. Not 1.0: the conditional read literally ("IF both were seeded, the presence check passes") is true by tautology, and the counterfactual fabricated-seed run was never executed. It is dead as a design, not false as logic.

The node has no `status` field (it carries `verdict: pending` only). No overlap with goal:g7.33.10.1: this claim is about new scaffolds, not the 228-node pre-gate corpus.
