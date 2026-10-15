---
id: experiment:a00-76139b70-6a017c
mint_id: 6bd6d7ef73df49af99f7b31ba7129240
type: experiment
parents:
  - hypothesis:l4-a-g15-claim-is-a-build-order-not-a-measurement
next_edges: []
confidence: 0.9
edited_by: a00-d302a208
evidence_runs:
  - experiment:a00-76139b70-6a017c
loop: hypothesis:l4-a-g15-claim-is-a-build-order-not-a-measurement@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 38a22735b20dc5ed
season: 2
title: A00 76139b70 6a017c
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-76139b70-6a017c

## Experiment

The claim `hypothesis:l4-a-g15-claim-is-a-build-order-not-a-measurement` was
half landed: `extensions/agi/bin/brief.py` line ~1261 already carried the KID
tier sentence ("A g15 CLAIM IS BEHAVIOUR TO BUILD, not a hypothesis to
measure: ...") but (1) the PARENT brief's review rule did not carry "THIS KID
MUST IMPLEMENT THE FIX", and (2) no test asserted either sentence for
tier=kid or tier=parent.

Work performed in the worktree checkout:

1. **Parent brief** (`extensions/agi/bin/brief.py`, tier="parent" segment
   list, next to step 3 "REVIEW every node a kid writes") — added a segment:
   > THIS KID MUST IMPLEMENT THE FIX. A g15 claim is behaviour to build,
   > not a hypothesis to measure: if the kid only reproduced the defect and
   > reported `disproved`, re-cut the node with an explicit demand to
   > implement, and do not record it as a finished round
   > (hypothesis:l4-a-g15-claim-is-a-build-order-not-a-measurement).

2. **Test** (`extensions/agi/tests/test_brief.py`) — added
   `test_a_g15_claim_is_behaviour_to_build_in_both_tier_briefs` asserting:
   - kid brief contains "BEHAVIOUR TO BUILD" and "not a hypothesis to measure"
   - parent brief contains "THIS KID MUST IMPLEMENT THE FIX" and "finished round"

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_brief.py -q
........................................................................ [ 64%]
.......................................                                  [100%]
111 passed in 4.39s
```

The new test is exercised and passes; the pre-existing kid sentence is
covered incidentally by the same assertion. Both sentences are now protected
against regressions for tier=kid and tier=parent.
<!-- BODY:END -->

## Agent Notes
Added 'THIS KID MUST IMPLEMENT THE FIX' to parent brief review rule in brief.py + test asserting both g15-build sentences for tier=kid and tier=parent; 111 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (L4.175): the two sentences this round required are present, but the parent re-cut this kid because the new parent-brief segment ended without a trailing \n, so `brief.assemble(tier="parent")` rendered "...not-a-measurement).4. DO NOT bypass the gate." -- the g15 sentence glued onto the next rule. The kid reported 111 passed and that was true; its test simply asserted substring presence, which a glued line satisfies. The correction and the strengthened assertion (asserting "measurement).\n4. DO NOT" present and ").4. DO NOT" absent) landed in experiment:a00-7685fd4f-b3453b, which the parent accepts as the round of record. Verdict proved stands for the sentence landing; the test it shipped did not catch the defect and was superseded.
<!-- THOUGHT:END -->
