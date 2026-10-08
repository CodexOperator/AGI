---
id: experiment:a00-7685fd4f-b3453b
mint_id: dcf37d72641447d3b79b1d4dbdaa5386
type: experiment
parents:
  - hypothesis:l4-a-g15-claim-is-a-build-order-not-a-measurement
next_edges: []
confidence: 0.97
edited_by: a00-d302a208
evidence_runs:
  - experiment:a00-7685fd4f-b3453b
loop: hypothesis:l4-a-g15-claim-is-a-build-order-not-a-measurement@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 82c8fc820f22aed9
season: 2
title: A00 7685fd4f b3453b
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-7685fd4f-b3453b

## Experiment

Parent re-cut `experiment:a00-76139b70-6a017c` (kid #1 had landed the g15
BUILD-order segment in `extensions/agi/bin/brief.py` + a test, but the segment
ended with no trailing newline). Defect reproduced exactly:

    ...)\.join(brief.assemble(tier='parent', ...))  contained
    '(hypothesis:l4-a-g15-claim-is-a-build-order-not-a-measurement).4. DO NOT
    bypass the gate.'

Rendered parent brief glued the g15 sentence onto the next rule because the
`f"4. DO NOT..."` literal at line 1582 implicitly concatenated onto the
`(hypothesis:...)` literal at line 1581 INSIDE one list element.

FIX (file scope: brief.py + test_brief.py only):
1. Appended trailing `\n` to the `(hypothesis:...)` string in `_parent` so
   step 4 starts on its own line.
2. Strengthened `test_a_g15_claim_is_behaviour_to_build_in_both_tier_briefs`:
   asserts `"measurement).\n4. DO NOT"` IS in the joined parent text and
   `").4. DO NOT"` is NOT.

Proved on the built bytes:
    python3 -m pytest extensions/agi/tests/test_brief.py -q  => 111 passed
    Reproduction grep now exits 1 (no glued line).

## Evidence

- `pytest extensions/agi/tests/test_brief.py -q` => `111 passed in 4.27s`
- `grep -o "(hypothesis:l4-a-g15[^ ]*).4. DO NOT"` on the joined parent text
  returns nothing (exit 1) — the glue is gone; before the fix it matched.
- Rendered slice: `'...not-a-measurement).\n4. DO NOT bypass the gate. ...'`

Note: the parent's suggested assertion literal `"measurement)\n4. DO NOT"` did
not match reality — the real text has a period before the newline
(`measurement).\n4.`). The strengthened test asserts the true byte shape.

## Agent Notes
Fixed trailing-newline defect in brief.py parent segment (g15 sentence glued onto '4. DO NOT bypass the gate'); strengthened test to assert 'measurement)\n4. DO NOT' present / ').4. DO NOT' absent; 111 pytest pass; repro grep clean.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (L4.175): accepted as the round of record. The parent reproduced the defect on built bytes before the fix (the joined parent brief contained "(hypothesis:...).4. DO NOT") and after (slice "(hypothesis:...).\n4. DO NOT bypass the gate."), and re-ran the suite: 111 passed. The kid correctly noted the parent brief literal was slightly wrong ("measurement)\n4. DO NOT" vs the real "measurement).\n4. DO NOT") and asserted the true byte shape -- a parent correction, not a kid error. Both halves of the target claim now hold: kid sentence at brief.py:1261 and parent sentence in _parent step 3, protected by test_a_g15_claim_is_behaviour_to_build_in_both_tier_briefs for tier=kid and tier=parent.
<!-- THOUGHT:END -->
