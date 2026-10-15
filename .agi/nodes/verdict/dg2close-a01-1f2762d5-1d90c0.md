---
id: verdict:dg2close-a01-1f2762d5-1d90c0
mint_id: 14300f6236da4450a5847ce0c82a7817
type: verdict
parents:
  - experiment:dg2close-a01-1f2762d5-1d90c0-check
  - hypothesis:a01-1f2762d5-1d90c0
next_edges: []
confidence: 0.85
edited_by: director-general-2
evidence_runs:
  - experiment:dg2close-a01-1f2762d5-1d90c0-check
scaffold_hash: 87fbdbc25d039643
season: 2
title: "closing (goal:s18 retired): Removing the 3 free-text cavekit_req fields plus inlining breaks nothing (load, links, schema, find_chains identical on a /tmp copy; no engine reader); moot as an S18 bottleneck; the 3 fields are still live"
town: core
verdict: proved
---
# verdict:dg2close-a01-1f2762d5-1d90c0

| conjunct | observed |
|---|---|
| the 3 values are free text that resolves to no kit requirement | TRUE (row 1; kits deleted at L1.09, so nothing resolves now) |
| removal plus inlining breaks node loading / schema validation | NO: load, links and schema are identical before and after (rows 5, 7, 8); not schema-required (row 4) |
| test suite passes | no test references the field (row 3); the full suite was not re-run |
| level3.py uncrashed | unaffected by construction (row 9) |
| find_chains() unchanged for their chains | unchanged (row 6), but vacuously, since 0 chains either way |
| "first bottleneck to clear for S18" | **moot**: S18 retired; step 2 (inline the 91) was overtaken by L1.09 retiring all 91 carriers, whose parent hypotheses already held the text verbatim (see a00-15d05ac0) |

**Why proved.** Every stated disproof (a test depends on the field, the scanner crashes, the schema requires it) fails on the bytes. The fix was applied to a copy and nothing measurable moved. Confidence is 0.85 because two conjuncts (the full suite, find_chains) are shown by absence of any reader, or hold vacuously, rather than by a live run. Note for the record: the fix itself was never applied, and the 3 fields are still live at HEAD. Under the retired goal that is harmless (row 2: no reader). No corrective follows.
