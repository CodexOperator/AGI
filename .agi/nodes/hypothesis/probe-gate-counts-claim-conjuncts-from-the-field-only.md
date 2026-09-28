---
id: hypothesis:probe-gate-counts-claim-conjuncts-from-the-field-only
mint_id: 9c32ff237c4141e8be07f1db4682ff0a
type: hypothesis
parents:
  - goal:g1
next_edges: []
confidence: 0.8
edited_by: a00-f1812eb6
evidence_runs:
  - experiment:a00-a041cdef-3b79fa
  - experiment:a00-ea0222b3-4ed78e
  - experiment:a00-7b5520ac-96a290
  - experiment:a00-9f9aaacd-303434
  - experiment:a00-df914bba-114582
  - experiment:a00-9a0bf8cb-864103
  - experiment:a00-f1812eb6-4ade63
scaffold_hash: e8c436a2bfd74454
season: 2
tags:
  - engine
  - cli
  - gate
testable_claim: "(1) when testable_claim carries a numbered item, cli._claim_conjunct_numbers returns the field numbers only (2) the body is read only for a node with no numbered field (3) the probe gate is unchanged on every other shape (assigned: director-engine)"
title: "the probe gate counts claim conjuncts from testable_claim only -- body prose never inflates the set (mur-10 DH.465; assigned: director-engine)"
town: core
verdict: proved
---
# hypothesis:probe-gate-counts-claim-conjuncts-from-the-field-only

# hypothesis:probe-gate-counts-claim-conjuncts-from-the-field-only

## Measured
- (historical, pre-fix -- NOT the live state; see the next bullet) `cli._claim_conjunct_numbers` (extensions/agi/bin/cli.py:1169) unioned every `_CLAIM_ITEM_RE` `(n)` match in the `testable_claim` field WITH every match in the node BODY, so review prose that numbers its own orders inflated the conjunct set: mur-director-engine-10 DH.465 measured [1,2,3,4] for a 3-conjunct claim; DH.477 had to reword another seat's authored review prose to de-number it. Live state (landed by commit e12a57722, experiment:a00-a041cdef-3b79fa; cli.py unchanged from there to fffb284f6; cli.py:1179-1183): the field wins outright when numbered; the body is read only otherwise.
- LANDING (EG.90, measured, not retyped): the fix is commit `e12a57722` -- `git diff --numstat e12a57722^ e12a57722` -> `9 7 extensions/agi/bin/cli.py`, `78 0 extensions/agi/tests/test_cli_claim_conjunct_scope.py`, `77 0 .agi/nodes/experiment/a00-a041cdef-3b79fa.md`; `git diff --numstat e12a57722 fffb284f6 -- extensions/agi/bin/cli.py` -> empty. `8005cdd06` (the only landing provenance this node carried before EG.90) is a node-only merge-up: `git diff --numstat 8005cdd06^ 8005cdd06` -> `110 21 .agi/nodes/experiment/a00-df914bba-114582.md`, zero extensions/ bytes. The candidate originated as DH.476 on branch season2/loops/hypothesis-heal-worktree-refusal-a00-c3688e41 and was re-derived, not merged, by a00-a041cdef (red-first). `grep -n 'def _claim_conjunct_numbers' extensions/agi/bin/cli.py` read `1169:def _claim_conjunct_numbers(node_file: Path) -> list:` at 8005cdd06 (EG.40) and still does at fffb284f6.
- FALSIFIER 3 (EG.90, experiment:a00-f1812eb6-4ade63), at fffb284f6 in a full checkout: `env -u TMUX -u TMUX_PANE timeout 900 python3 -m pytest extensions/agi/tests/test_cli.py extensions/agi/tests/test_heal_watch.py extensions/agi/tests/test_dispatch.py extensions/agi/tests/test_cli_claim_conjunct_scope.py extensions/agi/tests/test_bin_help_smoke.py -q -p no:cacheprovider --basetemp /tmp/eg90-f1812eb6` -> `362 passed, 6 skipped, 55 warnings in 271.51s (0:04:31)`. The neighbourhood is green; falsifier 3 did not fire.

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

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
EG.90 corrective (a00-f1812eb6): the live-state label read EG.63 and the only landing provenance was the node-only commit 8005cdd06; both now name e12a57722, the commit that changed cli.py (numstat pasted). evidence_runs gain the code fix a00-a041cdef-3b79fa and the wire test a00-ea0222b3-4ed78e. Falsifier 3 (test_cli.py + neighbourhood) was never run by the round that set proved; it is run here at fffb284f6 and is green (362 passed, 6 skipped), so verdict proved stands on evidence that now covers every named falsifier.
<!-- THOUGHT:END -->
