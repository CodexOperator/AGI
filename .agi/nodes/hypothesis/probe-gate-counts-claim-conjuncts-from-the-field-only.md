---
id: hypothesis:probe-gate-counts-claim-conjuncts-from-the-field-only
mint_id: 9c32ff237c4141e8be07f1db4682ff0a
type: hypothesis
parents:
  - goal:g1
next_edges: []
confidence: 0.8
edited_by: director-engine
scaffold_hash: e8c436a2bfd74454
season: 2
tags:
  - engine
  - cli
  - gate
testable_claim: "(1) when testable_claim carries a numbered item, cli._claim_conjunct_numbers returns the field numbers only (2) the body is read only for a node with no numbered field (3) the probe gate is unchanged on every other shape (assigned: director-engine)"
title: "the probe gate counts claim conjuncts from testable_claim only -- body prose never inflates the set (mur-10 DH.465; assigned: director-engine)"
town: core
---
# hypothesis:probe-gate-counts-claim-conjuncts-from-the-field-only

# hypothesis:probe-gate-counts-claim-conjuncts-from-the-field-only

## Measured
- `cli._claim_conjunct_numbers` (extensions/agi/bin/cli.py:1169) unions every `_CLAIM_ITEM_RE` `(n)` match in the `testable_claim` field WITH every match in the node BODY (:1178, :1181), so review prose that numbers its own orders inflates the conjunct set: mur-director-engine-10 DH.465 measured [1,2,3,4] for a 3-conjunct claim; DH.477 had to reword another seat's authored review prose to de-number it.
- A candidate fix exists UNREVIEWED on branch season2/loops/hypothesis-heal-worktree-refusal-a00-c3688e41 (DH.476, off-orders there): the field wins outright when it carries a numbered item; the body is read only when the field has none.

## CLAIM
(1) when `testable_claim` carries at least one numbered item, `_claim_conjunct_numbers` returns the field's numbers ONLY; (2) the body is read only for a node with no numbered field; (3) the parent probe gate's behaviour on every other shape is unchanged.

## Dispatch line
config-max: none. template-max: none. code: the claim-surface rule in cli.py (the schema already names testable_claim as the claim field).

## FALSIFIERS
- a node whose field says (1)(2)(3) and whose body quotes (4) returns [1,2,3,4].
- a node with no numbered field and a numbered body CLAIM returns [].
- test_cli.py or its neighbourhood goes red.

## TESTS
extensions/agi/tests/test_cli_claim_conjunct_scope.py (new or taken from DH.476's branch after review). Neighbourhood: test_cli.py test_heal_watch.py test_dispatch.py.

## FILE SCOPE
extensions/agi/bin/cli.py (`_claim_conjunct_numbers` only) · extensions/agi/tests/test_cli_claim_conjunct_scope.py

## CEILING
1 kid · <= 12 production lines · pi-free tier-0 · 0 USD.
