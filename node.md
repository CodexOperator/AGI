---
id: experiment:a00-a041cdef-3b79fa
mint_id: b89234949f244efe9abd79bf7d874275
type: experiment
parents:
  - hypothesis:probe-gate-counts-claim-conjuncts-from-the-field-only
next_edges: []
confidence: 0.9
edited_by: a00-ea0222b3
evidence_runs:
  - experiment:a00-a041cdef-3b79fa
loop: hypothesis:probe-gate-counts-claim-conjuncts-from-the-field-only@s2
model: stealth/space-bunny-alpha
probes:
  - {"conjunct": 1, "name": "c1_field_wins_over_body", "class": "gate", "cmd": "node w/ field testable_claim '(1)(2)(3)' + body review citing (1)..(4); cli._claim_conjunct_numbers", "expected": "[1, 2, 3]", "observed": "[1, 2, 3] (pre-fix [1, 2, 3, 4])", "result": "pass"}
  - {"conjunct": 2, "name": "c2_body_read_when_no_field", "class": "gate", "cmd": "node with no testable_claim field and body CLAIM (1)(2); cli._claim_conjunct_numbers", "expected": "[1, 2]", "observed": "[1, 2]", "result": "pass"}
  - {"conjunct": 2, "name": "c2_body_read_when_field_unnumbered", "class": "gate", "cmd": "node with PROSE testable_claim + numbered body CLAIM (1)(2); cli._claim_conjunct_numbers", "expected": "[1, 2]", "observed": "[1, 2]", "result": "pass"}
  - {"conjunct": 3, "name": "c2_empty_everywhere", "class": "gate", "cmd": "node with no numbers in field or body; cli._claim_conjunct_numbers", "expected": "[] and an inactive gate (no invented conjunct)", "observed": "[], active=False", "result": "pass"}
  - {"conjunct": 3, "name": "live_gate_through_the_changed_bytes", "class": "wire", "cmd": "cli._parent_probe_gate(root, rec, args, verdict) on a temp graph, field (1)(2)(3) + body review (1)..(4), probes for 1..3; then the negative control with the conjunct-3 probe dropped", "expected": "error=None, active=True, covered=[1,2,3]; control refuses naming conjunct 3", "observed": "(None, True, [1,2,3]); control: 'missing ... conjunct(s): 3'", "result": "pass"}
production_lines: 9
profile: balanced
role: kid
scaffold_hash: 0cb94dfe4498186f
season: 2
title: "the claim field wins the conjunct set: red-first fix of _claim_conjunct_numbers"
town: core
verdict: proved
---
# experiment:a00-a041cdef-3b79fa

## Dispatch line
config-max: none. template-max: none. code: the claim-surface rule in cli.py (the schema already names testable_claim as the claim field).

## What I did
Red-first on the three falsifiers, then the minimal change to
`cli._claim_conjunct_numbers` (extensions/agi/bin/cli.py). The DH.476 branch
candidate was read read-only and re-derived against the CURRENT bytes rather
than merged (that branch carries unrelated heal.py work).

| # | shape | expected | pre-fix | post-fix |
|---|-------|----------|---------|----------|
| 1 | field (1)(2)(3) + body review citing (1)..(4) | [1,2,3] | **[1,2,3,4]** | [1,2,3] |
| 2 | no field, numbered body CLAIM | [1,2] | [1,2] | [1,2] |
| 3 | unnumbered field + numbered body | [1,2] | [1,2] | [1,2] |
| 4 | no numbers anywhere | [] | [] | [] |

### RED, before touching cli.py
```
>       assert cli._claim_conjunct_numbers(nf) == [1, 2, 3]
E       assert [1, 2, 3, 4] == [1, 2, 3]
E         Left contains one more item: 4
FAILED extensions/agi/tests/test_cli_claim_conjunct_scope.py::test_body_review_prose_does_not_manufacture_a_conjunct
1 failed, 3 passed in 2.01s
```
Falsifier 1 fired exactly as mur-10 DH.465 measured. Falsifiers 2 and the two
neighbour shapes were already green and had to STAY green — they are the
regression guard, not the finding.

### GREEN, after the change
```
$ python3 -m pytest extensions/agi/tests/test_cli_claim_conjunct_scope.py \
    extensions/agi/tests/test_cli.py extensions/agi/tests/test_heal_watch.py \
    extensions/agi/tests/test_dispatch.py -q
287 passed, 54 warnings in 13.70s
```

## The change
The field wins outright when it carries a numbered item; the body is read only
for a node with no numbered field. Early `return` replaces the union; the
`except` arm and the empty tail are unchanged, so an unreadable node still
yields [] and the gate stays inactive rather than inventing numbers.

## Verdict
All three clauses of the claim hold on the built bytes. Clause 1 was false
before the change and true after (falsifier 1 flipped red→green). Clause 2 and
clause 3 never regressed (falsifiers 2, 3, 4 green before and after; 287 tests
in the neighbourhood green).

## Production lines
`git diff --numstat -- extensions/agi/bin/cli.py` → `9 7` (16 total; ceiling 40).

## Agent Notes
Red-first: falsifier 1 returned [1,2,3,4] pre-fix; field now wins outright, body read only when no numbered field. 287 neighbourhood tests green, 9 production lines.

PARENT REVIEW a00-cfed6d3f (DH.492) — ACCEPTED, verdict proved stands. Mechanism, not wording. (1) WHAT THE BRIEF SAID: "red-first on every FALSIFIER, prove each, take what is right off DH.476, never merge it wholesale; any byte outside FILE SCOPE is a cut." (2) WHAT THE MACHINE ACTUALLY DOES: the touched-byte set in this checkout is exactly {extensions/agi/bin/cli.py, extensions/agi/tests/test_cli_claim_conjunct_scope.py} (mtime scan, both inside FILE SCOPE); cli.py:1169-1185 now RETURNS the field set outright when the field matches _CLAIM_ITEM_RE and falls through to the body only when it does not — a near-identical body to the DH.476 candidate, re-derived rather than merged (no heal.py / test_heal.py bytes rode along). (3) NEAR MISS: a fix that drops the union and returns the field whenever the FIELD EXISTS (an isinstance check alone, no .search on the field) would pass falsifier 1 and silently return [] for an old node whose field is prose and whose numbered CLAIM lives in the body — a real corpus shape, and it would have deactivated the probe gate for exactly those nodes instead of narrowing it. The kid kept the .search arm; my probe c2_body_read_when_field_unnumbered confirms the body still decides there. (4) DEVIATION: the dispatch orders ban write.py thought on this branch (known engine bug), so this review is a note rather than a THOUGHT block rewrite — the rule that review reasoning lands in THOUGHT is overridden by the seat, and the content is unchanged.

PARENT-RUN NEGATIVE PROBES (mine, in the parent scratch dir, not the kid suite):
probes: [gate] c1_field_wins_over_body — node with field (1)(2)(3) and a body review citing (1)..(4) must return [1,2,3]. RED ON THE CURRENT BYTES BEFORE THE KID TOUCHED THEM: got [1, 2, 3, 4] (my own run, the mur-10 DH.465 shape). GREEN AFTER: [1, 2, 3].
probes: [gate] c2_body_read_when_no_field — no testable_claim field, body CLAIM (1)(2) still returns [1, 2] (green before and after; the regression guard).
probes: [gate] c2_body_read_when_field_unnumbered — a PROSE testable_claim field with a numbered body returns [1, 2], i.e. the body is read whenever the field carries no numbered item, not merely when the field is absent. This is the near-miss shape and it holds.
probes: [gate] c2_empty_everywhere — no numbers in field or body returns [] and the gate stays inactive rather than inventing a conjunct.
probes: [wire] live_gate_through_the_changed_bytes — the real call site, _parent_probe_gate, on a temp graph whose target hypothesis has field (1)(2)(3) and a body review citing (1)..(4): with probes for 1,2,3 and NOT 4, both verdict=proved and verdict=inconclusive_lean_proved:50 return error=None, active=True, covered=[1,2,3]. The phantom conjunct 4 is demanded by nobody. NEGATIVE CONTROL in the same run: dropping the conjunct-3 probe is still REFUSED ("missing ... conjunct(s): 3"), so the pass is not vacuous and the gate still bites.
Every deliverable the node names is present in the bytes it claims: the new test file exists with the falsifier-1 test that went red first, the four-shape table matches what I measured independently, and the 9 production lines sit under the 12-line ceiling. No foreign node was edited and nothing was committed by hand.
