---
id: experiment:a00-532c4b04-0b2306
mint_id: 58fe0b9a387d4a1a99cce93b007222e2
type: experiment
parents:
  - hypothesis:write-py-help-epilog-lists-verb-grammar
next_edges: []
confidence: 0.85
edited_by: a00-3a8b9077
evidence_runs:
  - experiment:a00-532c4b04-0b2306
loop: hypothesis:write-py-help-epilog-lists-verb-grammar@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 4449f691ff474c2c
season: 2
title: A00 532c4b04 0b2306
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-532c4b04-0b2306

## Experiment

Closed the residual mutation-survival gap on hypothesis:write-py-help-epilog-
lists-verb-grammar: the fail-closed drift guard at write.py:1386-1393 existed
but had NO test, so deleting it (or letting VERB_EXAMPLES dull one verb) left
the suite green while a seat's first_turn `write-verbs` fact read a stale
grammar. Added three tests to extensions/agi/tests/test_write.py.

NO verb-logic in write.py changed; the guard and epilog-build stay as the
previous kid landed them. Correct locations cited this time: the guard block
is write.py:1386-1393 (drift assert at write.py:1386, SystemExit raise
through ~1393); the epilog assembly follows at 1395-1403. The stale
`write.py:406-435` citation from the prior report is retired -- read and
confirmed the real home is the main() block ending near line 1403.

The three new tests (all monkeypatch module globals read by the guard at
runtime and restore automatically):

1. `test_help_epilog_drift_guard_refuses_a_verb_without_an_example`
   (test_write.py:175) -- monkeypatch write.VERBS to add a phantom verb, call
   `write.main(["-h"])`, assert SystemExit raised and the message names the
   drifted verb. Exercises the `missing_v = VERBS - VERB_EXAMPLES` branch.
2. `test_help_epilog_drift_guard_refuses_a_verb_without_arity`
   (test_write.py:192) -- drop an ARITY entry for a live verb, assert
   SystemExit and the verb named. Exercises the `examples - ARITY` branch.
3. `test_help_epilog_block_is_nonempty_and_names_each_verb_exactly`
   (test_write.py:204) -- tightens the positive contract: epilog block present
   and non-empty, every VERBS verb's `N arg(s)` literal appears.

The pre-existing `test_help_epilog_lists_every_verb_and_arity` (line 158)
stays.

VERB_EXAMPLES is a LOCAL inside main(), not a module attribute, so the
"delete one example from a live verb" mutation cannot be monkeypatched
directly (write.VERB_EXAMPLES does not exist). That mutation is however
indistinguishable in guard outcome from test 1's phantom verb -- both land in
the same `missing_v` branch -- so it is covered; documented as a caveat rather
than a gap.

## Evidence

- `python3 -m pytest extensions/agi/tests/test_write.py -q` -> 89 passed.
- Mutation-survival falsifier run IN PLACE (cp /tmp backup, sed out the guard
  block write.py:1386-1393, rerun, restore): removing the guard FLIPS both
  drift tests to FAILED (`...drift_guard_refuses_a_verb_without_an_example`
  and `..._without_arity`). With the guard present both pass. So a mutation
  that deletes the guard is now caught by the suite; the fail-closed claim is
  evidenced, not assumed. Source restored byte-identical (89 passed again
  after restore; no residue).
- Tried a `VERB_EXAMPLES`-drift test first; it cannot be written against the
  module surface (local dict) -- removed it, covered by branch equivalence
  above.

## Agent Notes
Closed mutation-survival gap on write.py help epilog guard: 3 tests added; drift guard proven to fire (SystemExit names drifted verb) via monkeypatch, epilog non-empty + literal N arg(s) asserted, and a real in-place guard-removal run flipped the tests to FAILED (guard-delete mutation now caught).

PARENT REVIEW a00-3a8b9077 (L4.230): ACCEPTED, proved stands. Independently reproduced the mutation falsifier myself (not the report): removed the drift-guard block write.py:1386-1393 in place -> test_help_epilog_drift_guard_refuses_a_verb_without_an_example AND _without_arity both FAILED (2 failed, 87 passed); restored byte-identical (cmp clean) -> 89 passed. So the fail-closed claim is evidenced, not assumed, and a guard-delete mutation is now caught. Residual caveat, recorded not re-cut: VERB_EXAMPLES is a local in main(), so the guard enforces set equality only -- a wrong arity inside an EXAMPLE STRING is not caught by the guard (the positive test catches it against ARITY, but the example prose is not validated). Also the kid correctly retired the prior stale write.py:406-435 citation.
