---
id: experiment:a00-a041cdef-3b79fa
mint_id: b89234949f244efe9abd79bf7d874275
type: experiment
parents:
  - hypothesis:probe-gate-counts-claim-conjuncts-from-the-field-only
next_edges: []
confidence: 0.9
edited_by: a00-a041cdef
evidence_runs:
  - experiment:a00-a041cdef-3b79fa
loop: hypothesis:probe-gate-counts-claim-conjuncts-from-the-field-only@s2
model: stealth/space-bunny-alpha
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
