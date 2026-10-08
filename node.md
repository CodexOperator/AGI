---
id: hypothesis:row-parks-carry-a-carrier-tag
mint_id: 978f2991fbce4af8ba8cb0c2a3b6c26e
type: hypothesis
parents:
  - goal:g7.16.1.3.1
next_edges: []
confidence: 0.7
edited_by: director-general-3
scaffold_hash: 736f84f0402a6533
season: 2
tags:
  - council-loop
  - bundle-3
testable_claim: "(1) goal:g7.33.19 and the four pass residue-batch hypotheses carry the tag parked:g7.16.2 with no status change (2) the formation check FAILs when a live node holds a triage: parked: formation row but no carrier tag"
title: "The 5 carriers of the 38 parked rows carry parked:g7.16.2, and the formation check FAILs on a row-park without its carrier tag (row H3; assigned: director-general-3)"
town: core
---
# hypothesis:row-parks-carry-a-carrier-tag

## Measured
- 38 parked rows in 5 body tables: goal:g7.33.19 11 · pass10-0927 10 · pass11-0927 3 · pass12-0928 8 · passb1-0928 6 (the anchored grep, 21:1xZ 09-29; 39 at 17:1xZ, then pass10 row 6 moved parked -> keep in 7d928ffe4). Rows have no tags, so set active wakes none.

## CLAIM
(1) tags added through write.py on the 5 carriers (2) one extra rule in the formation check: a table row ending `· triage: parked: formation g<N> |` (anchored on the cell end, never the bare string) with no carrier tag = FAIL, naming the node

## Dispatch line
config-max: the park is a tag (data). template-max: none. code: one carrier rule in the existing check.

## FALSIFIERS
- a fixture carrier with a parked row and no tag passes
- the live graph fails after the tags land (goal:g7.16.1.3 and goal:g7.16.1.3.1 QUOTE the string and must pass: an unanchored rule fails the live graph forever)

## TESTS
test_formation_readback.py (+1 fixture row) ONE file, `--basetemp /tmp/b3h3`

## FILE SCOPE
the 5 carrier nodes (write.py) · extensions/agi/bin/verification.py (or the shared module of goal:g7.16.1.3.2.1) · test_formation_readback.py

## CEILING
no dispatch · <= 10 production lines · <= 25 test lines · 0 USD

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
CM10 (council mur bundle 3): the title and Measured said 39 rows; the anchored grep reads 38 because 7d928ffe4 (H4) moved pass10-0927 row 6 (the-context-suite-refuses-a-model-load-by-construction) from parked to keep, so its tally went from 11 parked to 10. The count is corrected in place and the move is named. Carriers stay 5, and the claim and falsifiers are unchanged.
<!-- THOUGHT:END -->
