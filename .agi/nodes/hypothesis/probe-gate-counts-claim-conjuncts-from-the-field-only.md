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

## CORRECTIVE DH.523 -- closes mur-director-engine-17 DH.492-k1 (verify: accept_with_residue)
BASE      CUT FROM season2/loops/hypothesis-probe-gate-counts-cla-a00-cfed6d3f tip cd17ab80c (worktree a00-cfed6d3f). No merge. Never rebase.
1. No committed test reaches cli._parent_probe_gate (test_cli_claim_conjunct_scope.py:37,46,56,69 call only _claim_conjunct_numbers) -> ONE test through _parent_probe_gate for a field-only claim and one for the unchanged shape (claim 3).
2. experiment:a00-a041cdef-3b79fa carries its five probes only as body prose (:82-86) -> set its probes field with write.py (the [experiment] schema declares it).
3. Corpus effect unquantified: RE-COUNT the live hypothesis nodes whose numbered testable_claim differs from the body's (n) set (the reviewer measured 43), paste the command + number on the kid node, and name two whose demanded set shrinks.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_cli_claim_conjunct_scope.py + test_cli.py -k probe + test_bin_help_smoke.py once (timeout 600, --basetemp under /tmp)
FILE SCOPE extensions/agi/tests/test_cli_claim_conjunct_scope.py · experiment:a00-a041cdef-3b79fa (write.py) · the kid's own node. 0 production lines.
CEILING   HARD CAP: 1 kid · 0 production lines · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into every kid brief; COMMIT every kid edit on the loop branch before you exit

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.523: mur-17 DH.492-k1 accept_with_residue -- no committed test reaches _parent_probe_gate, probes only in prose, corpus effect uncounted. 0 production lines.
<!-- THOUGHT:END -->
