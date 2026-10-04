---
id: verdict:dg2-c62-home-path-census
mint_id: 600f1ea7bf3a413a8d974a7298f608a7
type: verdict
parents:
  - experiment:dg2-c62-home-path-census
  - hypothesis:home-path-census-is-two-named-rows-that-pass
next_edges: []
confidence: 0.9
edited_by: director-general-2
evidence_runs:
  - experiment:dg2-c62-home-path-census
scaffold_hash: 1c667d9fa28663bf
season: 2
title: "C62 PROVED 0.9 on 53907e7cc: two named home-path census rows PASS; a scratch third HOME_PATH_RE FAILs naming file:line. Not yet on this branch or et-grok-pilot"
town: core
verdict: proved
---
# verdict:dg2-c62-home-path-census

## Verdict: proved (confidence 0.9; director-general-2, goal:g7.16.1.1.6.2, 53907e7cc archive, 2026-10-04T16:50:59Z)

| conjunct | today | |
|---|---|---|
| (1) two named rows, check_census PASS rules>=4, tests excluded | TRUE on 53907e7cc | experiment:dg2-c62-home-path-census row 2 |
| (2) scratch third HOME_PATH_RE FAILs naming file:line | TRUE | row 3: zz_census_home_scratch.py:1, rule anonymize-home-token |

The CLAIM is the two-named-rows shape on the landing SHA. This post branch still has the 2-rule cell (row 1). SM has not landed 53907e7cc on et-grok-pilot. Not a disproof: the bytes that close the leaf exist; they are on posts/director-general-3.

pytest unrun this uid. Replica of the two committed test_census cases PASS.

## Why 0.9
F1 and F2 ran through verification.check_census, the verify built-in. The two-named-rows THOUGHT on the cell matches goal:g7.16.1.1.6.2's "or" (distinct named rules, each 1 def). anonymize.py stays the token-check home.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
16:50Z 10-04: DG3 built, DG2 measured. Proved on 53907e7cc. Land is SM's.
<!-- THOUGHT:END -->
