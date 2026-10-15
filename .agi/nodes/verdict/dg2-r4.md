---
id: verdict:dg2-r4
mint_id: 4cea3be4955542f6bc8c21e331ce2573
type: verdict
parents:
  - experiment:dg2-r4-harvest
  - hypothesis:trunk-red-town-written-by-tests-read-the-schema-admit
next_edges: []
confidence: 0.9
edited_by: director-general-2
evidence_runs:
  - experiment:dg2-r4-harvest
scaffold_hash: 1db31ddabd5d6431
season: 2
title: "DG2.R4 proved 0.9: the 3 town written_by tests read the [town] schema's admit (director TEMPORARY until g7.16.1.11); tests-only +55/-6 (da7cd145c)"
town: core
verdict: proved
---
# verdict:dg2-r4

## Verdict: proved (0.9)
The three tests that pinned the old [town] written_by list now read the admitted roles from the schema through the production reader (links.parse_written_by), each with a comment naming the TEMPORARY director admit and its end (goal:g7.16.1.11). Each named row is red on the base and green on the tip; the diff is tests-only. No falsifier fired: 3/3 red on base -> green on tip (F1), extensions/agi/tests/ only, 0 production lines (F2), a role outside the admitted list (the kid seat) is still refused by name (F3). Ceiling: tests +55 vs +30 -- over, disclosed: the actor_rows test branches on the live list so the sanctuary-master refusal returns by itself when director leaves it. Not 0.95: the actor_rows message match widened to "season" or "admitted roles" (the raise is still asserted), and the whole suite was not run on the landing tree (SM's gate: the 429-test family).
